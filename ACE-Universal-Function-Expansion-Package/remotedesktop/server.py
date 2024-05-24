# coding: utf8

import socket
import random
import threading
import os
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.100.55.185', 25565))
s.listen(128)
s_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_c.bind(('10.100.55.185', 25566))
s_c.listen(128)
name_seed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
control_available = []
command = [[] for _ in range(128)]
state = [[] for _ in range(128)]
controller = {}


def ee(sock, addr):
    global control_available
    register_name = sock.recv(1024).decode()
    st = time.time()
    print(register_name)
    control_available.append(register_name)
    # sock.send(b'start')
    # ts, ta = s.accept()
    # threading.Thread(target=file_recv, args=[ts, ta, register_name, ]).start()
    time.sleep(10)
    # state[control_available.index(register_name)] = 'stop'
    sock.send(b'exit')
    print(time.time() - st)
    time.sleep(1)
    control_available.remove(register_name)
    sock.close()


def er(sock: socket.socket, addr):
    global control_available
    if len(control_available) == 0:
        sock.send(b'none')
        sock.close()
        return
    cnt = ''
    for _ in range(20):
        if random.randint(0, 1):
            cnt = cnt + name_seed[random.randint(0, 35)]
        else:
            cnt = cnt + name_seed[random.randint(0, 35)].upper()
    output = '{}/'.format(cnt)
    for item in control_available:
        output = output + item + '/'
    sock.send(output.encode())
    order = int(sock.recv(1024))
    controller[cnt] = order
    sock.close()
    controller.pop(cnt)


def file_recv(ts: socket.socket, ta, register_name):
    file_name = ''
    while True:
        global state
        if state[control_available.index(register_name)] == 'stop':
            state[control_available.index(register_name)] = ''
            ts.close()
            if not file_name == '':
                os.remove("upload/{}.jpeg".format(file_name))
            return
        recved = int(ts.recv(1024))
        if recved == -1:
            break
        ts.send(b'6')
        if not file_name == '':
            os.remove("upload/{}.jpeg".format(file_name))
        file_name = ''
        for _ in range(20):
            if random.randint(0, 1):
                file_name = file_name + name_seed[random.randint(0, 35)]
            else:
                file_name = file_name + name_seed[random.randint(0, 35)].upper()
        with open("upload/{}.jpeg".format(file_name), 'wb') as f:
            while recved > 0:
                c = ts.recv(524288)
                f.write(c)
                recved -= len(c)
        ts.send(b'ok')


while True:
    cs, ca = s_c.accept()
    cs.settimeout(10)
    type_ = cs.recv(1024)
    if type_ == b'controlled':
        print('一个被操控者上线')
        threading.Thread(target=ee, args=[cs, ca, ]).start()
    elif type_ == b'controller':
        print('一个操控者上线')
        threading.Thread(target=er, args=[cs, ca, ]).start()
