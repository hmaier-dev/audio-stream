#!/bin/python3

# Server transmitting audio
import socket
import pyaudio
import pickle
import struct
import platform


CHUNK = 1024*64
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# if pyaudio does not find an interface, please load the loopback-interface
# $ pactl load-module module-loopback


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    s.close()


def send_audio():
    print("Starting PyAudio")
    p = pyaudio.PyAudio()  # starting pyaudio
    print("You can ignore the previous error messages")
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    # get your ip address in the local network
    # LINUX: ip addr
    # WINDOWS: ipconfig

    # host = "192.168.0.79"  # change this to your ip addres
    host = get_host_ip()

    port = 61234

    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM)  # ipv4 and UDP

    socket_address = (host, port)
    server_socket.bind(socket_address)
    server_socket.listen(2)

    print("Server Listening at: {}".format(socket_address))

    conn, address = server_socket.accept()
    print("Connection from {}".format(address))

    print("Close connection with CTRL+C")
    while True:  # client is connected, start sending audio
        try:

            data = stream.read(CHUNK)  # read audio data
            x = pickle.dumps(data)  # converting into byte stream
            # create packet, the "+x" contains the audio
            message = struct.pack("Q", len(x))+x
            # add a buffer
            conn.sendall(message)  # send the packet
            # frames.append(data)
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            p.terminate()
            server_socket.detach()
            conn.close()
            break

    # wf = wave.open(file_name, 'wb')
    # wf.setnchannels(CHANNELS)
    # wf.setsampwidth(p.get_sample_size(FORMAT))
    # wf.setframerate(RATE)
    # wf.writeframes(b''.join(frames))
    # wf.close()
    # print("Audio has been saved as: {}".format(file_name))


if __name__ == "__main__":
    send_audio()
