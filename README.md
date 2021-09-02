# audio-stream installation

---

### Step 1

- Clone this repository to both of your machines

`git clone https://github.com/hmaier-ipb/audio-stream.git`

### Step 2

- Get the PyAudio-module installed

##### Windows
`pip install pipwin`

`pipwin install pyaudio`

You need `pipwin` to automatically install `portaudio` which is an C-Library that PyAudio uses to record/play audio. 

##### Linux


### Step 3

- Enable a loopback audio interface. This is needed to record internal system audio. This loopback-interface is seen as a internals microphone.

##### Pulseaudio on Linux
`pactl load-module module-loopback`

- You should get returned a number, which is the index number of the loopback-interface
- Btw: this is just temporary, for more info visit [USB Audio Device Loopback Through Speakers](https://askubuntu.com/questions/19894/usb-audio-device-loopback-through-speakers) or [How to route pulse audio device into alsa loopback (virtual microphone)?](https://askubuntu.com/questions/895216/how-to-route-pulse-audio-device-into-alsa-loopback-virtual-microphone)
- check `pavucontrol` to see if a new interface has appeared
- move to the input-devices tab and set the loopback-interface as fallback

##### Sound on Windows

- activate your soundcard as default audio-input devices
- here is a good article on how to do it [How to Record the Sound Coming From Your PC](https://www.howtogeek.com/217348/how-to-record-the-sound-coming-from-your-pc-even-without-stereo-mix/)