import cv2
import numpy as np
import math
import pyaudio
# import time
# import threading
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 40960
RECORD_SECONDS = 0.025

freq = 25.96
continueDisplay = True
Red = 0
Green = 0
Blue = 0

def saturate(temp_color):
    if(temp_color<0):
        return  0
    elif(temp_color>1):
        return 255
    else:
        return 255*temp_color

def frequency_mapper(freq):
    global Red, Green, Blue
    temp_log = 2*math.pi*(math.log2(freq/30.87))    # measuring relative to B note

    temp_R = 0.5+math.sin(11*(math.pi/3)+ temp_log) # 120 degrees out of faze from each other
    Red = saturate(temp_R) # for G# note

    temp_G = 0.5+math.sin(7*(math.pi/3)+ temp_log)  # 120 degrees out of faze from each other
    Green = saturate(temp_G) # for C note

    temp_B = 0.5+math.sin(math.pi + temp_log)       # 120 degrees out of faze from each other
    Blue = saturate(temp_B) # for E note

def listenRoutine():
    global freq, continueDisplay
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    while continueDisplay: 
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        audio_fft = np.fft.fft(audio_data)
        # frequencies = np.fft.fftfreq(len(audio_data))

        magnitude = np.abs(audio_fft)
        max_index = np.argmax(magnitude)
        freq = RATE * max_index / len(audio_fft)

        print(freq , "Hz")

    stream.stop_stream()
    stream.close()

def displayColorRoutine():
    global freq, continueDisplay, Red, Green, Blue
    width = 400
    height = 400
    x = 0
    y = 0
    image = np.zeros((width, height, 3), dtype=np.uint8)

    while continueDisplay: 
        frequency_mapper(freq)
        color = (Red, Green, Blue)
        cv2.rectangle(image, (x, y), (x + width, y + height), color, -1)
        cv2.imshow("Image", image)
        if(cv2.waitKey(25) != -1):
            continueDisplay = 0

    cv2.destroyAllWindows()
    
displayColorRoutine()
# listenRoutine()
