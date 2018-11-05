from pynput.keyboard import Key, Listener
import signal, os
import threading
import time
import mixer

ignore_keys = [Key.enter, Key.alt, Key.ctrl, Key.shift, Key.tab]

countdown = 0
silenced = False
fadingOut = False

max_volume = mixer.get_mixer('Master')['volumes'][0]
print("Max Volume: %s" % max_volume)

def fadeOut(fadeOutSpeed = 5):
    global silenced, fadingOut
    if fadingOut: return

    def worker():
        global fadingOut, silenced

        while fadingOut:
            current_volume = mixer.get_mixer('Master')['volumes'][0]
            if current_volume == 0:
                silenced = True
                fadingOut = False
            else:
                mixer.set_mixer('Master', str(max(current_volume - fadeOutSpeed, 0)))
                time.sleep(0.1)

    fadingOut = True
    t = threading.Thread(target=worker)
    t.start()


def worker():
    global countdown, silenced, fadingOut

    while True:
        if countdown == 0 and not silenced:
            fadeOut()
        elif countdown > 0 and silenced:
            mixer.set_mixer('Master', str(max_volume))
            silenced = False
        elif countdown > 0:
            if fadingOut:
                fadingOut = False
                mixer.set_mixer('Master', str(max_volume))
            countdown -= 100
        
        if countdown < 0:
            countdown = 0

        time.sleep(0.1)

t = threading.Thread(target=worker)
t.start()

def signal_handler(sig, frame):
    mixer.set_mixer('Master', str(max_volume))
    print("Bye!")
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

def on_press(key):
    if key in ignore_keys:
        return

    global countdown
    countdown += 3 * 1000
    if countdown > 30000:
        countdown = 30000
    print("Charging up! %s" % countdown)

with Listener(on_press=on_press) as listener:
    listener.join()