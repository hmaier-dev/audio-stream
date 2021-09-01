#!/bin/python

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "out.wav"

p = pyaudio.PyAudio()

# pactl load-module module-loopback
print("please load loopback interface")

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

frames = []
loop = True

print("Start recording!")

while loop:
    try:
        data = stream.read(CHUNK) # read audio data
        frames.append(data) # append to buffer
    except KeyboardInterrupt:
        break

print("Finished Recordings!")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
