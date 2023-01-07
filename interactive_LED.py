import cv2
import numpy as np
import math
import pyaudio
# import time
# import threading
import numpy as np

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 40960
RECORD_SECONDS = 0.1

width = 400
height = 400
x = 0
y = 0
image = np.zeros((400, 400, 3), dtype=np.uint8)

freq = 130.81
R = 0
G = 0
B = 0
continueDisplay = True

def saturate(temp_color):
    if(temp_color<0):
        return  0
    elif(temp_color>1):
        return 255
    else:
        return 255*temp_color

def frequency_mapper(freq):
    global R, G, B
    temp_log = 2*math.pi*(math.log2(freq/20.6025))    # measuring relative to E note

    temp_R = 0.5+math.sin(11*(math.pi/3)+ temp_log) # 120 degrees out of faze from each other
    R = saturate(temp_R) # for C note

    temp_G = 0.5+math.sin(7*(math.pi/3)+ temp_log)  # 120 degrees out of faze from each other
    G = saturate(temp_G) # for G# note

    temp_B = 0.5+math.sin(math.pi + temp_log)       # 120 degrees out of faze from each other
    B = saturate(temp_B) # for E note

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
    frequencies = np.fft.fftfreq(len(audio_data))

    magnitude = np.abs(audio_fft)
    max_index = np.argmax(magnitude)
    freq = RATE * max_index / len(audio_fft)

    print(freq , "Hz")

    # frequency_mapper(freq)
    # color = (R, G, B)
    # cv2.rectangle(image, (x, y), (x + width, y + height), color, -1)
    # cv2.imshow("Image", image)
    # cv2.waitKey(1000)

cv2.destroyAllWindows()
stream.stop_stream()
stream.close()




