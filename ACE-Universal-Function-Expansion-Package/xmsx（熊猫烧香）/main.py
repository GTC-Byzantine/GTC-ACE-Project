import os, time, subprocess, threading

for _ in range(50):
    threading.Thread(target=subprocess.run, args=['start doit.exe'], kwargs={'shell': True}).start()
    time.sleep(0.4)
