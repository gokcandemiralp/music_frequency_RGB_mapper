import cv2
import numpy as np
import math
import pyaudio
# import time
import threading
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 40960
RECORD_MS = 25

continueDisplay = True
Red = 0
Green = 0
Blue = 0

QUEUESIZE = 5
OUTLIERFREQS = 2
SAMPLEFREQS = QUEUESIZE - OUTLIERFREQS
queueHead = 0
freqQueue = [25.96,25.96,25.96,25.96,25.96]

def pushQueue(freq):
    global freqQueue, queueHead
    freqQueue[queueHead] = freq
    queueHead = (queueHead + 1) % QUEUESIZE

def purifyFreq():
    global freqQueue, queueHead
    purestDiff = RATE
    purestIndex = 0
    for currentIndex in range(QUEUESIZE):
        total = 0
        for groupIndex in range(SAMPLEFREQS):
            cmprPairIndx_0 = (groupIndex + currentIndex)%QUEUESIZE
            cmprPairIndx_1 = (((groupIndex+1)%SAMPLEFREQS + currentIndex))%QUEUESIZE
            #print(cmprPairIndx_0,"-",cmprPairIndx_1)
            total += abs(freqQueue[cmprPairIndx_0]-freqQueue[cmprPairIndx_1])
            if(total/SAMPLEFREQS < purestDiff):
                purestDiff = total/SAMPLEFREQS
                purestIndex = currentIndex
    ansTotal = 0
    for i in range(SAMPLEFREQS):
        ansTotal += freqQueue[(i+purestIndex)%QUEUESIZE]
    return ansTotal/SAMPLEFREQS

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
    global continueDisplay
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if (dev['name'] == 'MacBook Pro Speakers' and dev['hostApi'] == 0):
            dev_index = dev['index'] # Find device index
    
    stream = p.open(format=FORMAT,
                    channels=dev_index,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    while continueDisplay: 
        frames = []
        for i in range(0, int(RATE / CHUNK * (RECORD_MS/1000))):
            data = stream.read(CHUNK)
            frames.append(data)

        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        audio_fft = np.fft.fft(audio_data)
        # frequencies = np.fft.fftfreq(len(audio_data))

        magnitude = np.abs(audio_fft)
        max_index = np.argmax(magnitude)
        pushQueue(RATE * max_index / len(audio_fft))

    stream.stop_stream()
    stream.close()

def displayColorRoutine():
    global continueDisplay, Red, Green, Blue
    width = 400
    height = 400
    x = 0
    y = 0
    image = np.zeros((width, height, 3), dtype=np.uint8)

    while continueDisplay:
        freq = purifyFreq()
        if(freq > 0):
            frequency_mapper(freq)
        print(freq , "Hz")
        color = (Red, Green, Blue)
        cv2.rectangle(image, (x, y), (x + width, y + height), color, -1)
        cv2.imshow("Image", image)
        if(cv2.waitKey(RECORD_MS) != -1):
            continueDisplay = 0

    cv2.destroyAllWindows()

listenThread = threading.Thread(target=listenRoutine)
listenThread.start()
displayColorRoutine()
listenThread.join()
listenRoutine()
