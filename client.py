#!/bin/python3

# Client receiving audio

import socket
import struct
import pickle

import threading

import wave
import pyaudio


CHUNK = 1024*64
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
# WAVE_OUTPUT_FILENAME = "client_temp.wav"


def receive_audio():
    # server_name = socket.gethostname()

    server_name = "192.168.0.224"
    port = 61234  # port of the server

    client_socket = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM)  # Using IPv4 and UDP
    print("Trying to connect to {}:{}".format(server_name, port))
    client_socket.connect((server_name, port))
    print("Success!")
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    # client_socket.send(data.encode())# initial connection to the server
    data = b""
    payload_size = struct.calcsize("Q")  # 8 bytes

    while True:

        try:
            while len(data) < payload_size:  # receiving 1016 bytes
                # this while loop could be missed (because it iterates jsut once),
                # but for checking if theres a packet, I leave it there
                # receive the first part of the data to unpack the data
                packet = client_socket.recv(CHUNK)
                if not packet:
                    break
                data += packet

            # var for calculation of the message size
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            # calc how big the message will be
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            # msg_size = 4106
            while len(data) < msg_size:  # receive 3090 bytes
                data += client_socket.recv(CHUNK)

            # deconstructing the packet, to get the actual audio data
            frame_data = data[:msg_size]
            # deconstructing the packet (maybe I don't need this?!)
            data = data[msg_size:]
            frame = pickle.loads(frame_data)  # convert byte stream into audio
            # write the audio to a array which will create the client_temp.wav
            frames.append(frame)
            stream.write(frame)  # output the audio to the pc
            stream.get_write_available()
        except KeyboardInterrupt:
            client_socket.close()
            stream.stop_stream()
            stream.close()
            break

    # wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    # wf.setnchannels(CHANNELS)
    # wf.setsampwidth(p.get_sample_size(FORMAT))
    # wf.setframerate(RATE)
    # wf.writeframes(b''.join(frames))
    # wf.close()


if __name__ == "__main__":
    t1 = threading.Thread(target=receive_audio, args=())
    t1.start()
    receive_audio()
