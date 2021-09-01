#!/bin/python3

# Client receiving audio

import socket
import struct
import pickle

import wave
import pyaudio


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "client_temp.wav"



def receive_audio():
    # server_name = socket.gethostname()
    server_name = "hmaier-debian"
    port = 5656  # port of the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4 and TCP
    print("Trying to connect to {}:{}".format(server_name, port))
    client_socket.connect((server_name, port))
    print("Success!")
    print("Starting PyAudio...")
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
    payload_size = struct.calcsize("Q") # 8 bytes

    while True:

        try:
            while len(data) < payload_size: #receiving 1016 bytes
                # this while loop could be missed (because it iterates jsut once),
                # but for checking if theres a packet, I leave it there
                packet = client_socket.recv(1024) #receive the first part of the data to unpack the data
                if not packet: break
                data+=packet

            packed_msg_size = data[:payload_size] # var for calculation of the message size
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0] # calc how big the message will be
            #msg_size = 4106
            while len(data) < msg_size: #receive 3090 bytes
                data += client_socket.recv(1024)

            frame_data = data[:msg_size] # deconstructing the packet, to get the actual audio data
            data = data[msg_size:] # deconstructing the packet (maybe I don't need this?!)
            frame = pickle.loads(frame_data) # convert byte stream into audio
            frames.append(frame) # write the audio to a array which will create the client_temp.wav
            stream.write(frame) #output the audio to the pc
        except KeyboardInterrupt:
            client_socket.close()
            break

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    receive_audio()
