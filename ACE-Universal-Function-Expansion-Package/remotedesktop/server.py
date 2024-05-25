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
filenames = ['' for _ in range(128)]
controller = {}


def ee(sock, addr):
    global control_available, state
    register_name = sock.recv(1024).decode()
    st = time.time()
    print(register_name)
    control_available.append(register_name)
    state[control_available.index(register_name)] = ''
    # sock.send(b'start')
    # ts, ta = s.accept()
    # threading.Thread(target=file_recv, args=[ts, ta, register_name, ]).start()
    do_exit = False
    while True:
        for c in command[control_available.index(register_name)]:
            if c == 'start':
                sock.send(b'start')
                ts, ta = s.accept()
                threading.Thread(target=file_recv, args=[ts, ta, register_name, ]).start()
            elif c == 'stop':
                state[control_available.index(register_name)] = 'stop'
            elif c == 'exit':
                sock.send(b'exit')
                time.sleep(3)
                state[control_available.index(register_name)] = 'stop'
                do_exit = True
                command[control_available.index(register_name)].remove(c)
                break
            command[control_available.index(register_name)].remove(c)
        if do_exit:
            break
    # state[control_available.index(register_name)] = 'stop'
    print(time.time() - st)
    time.sleep(1)
    control_available.remove(register_name)
    sock.close()


def er(sock: socket.socket, addr):
    global control_available, command
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
    while True:
        cmd = sock.recv(1024).decode().split(' ')
        if cmd[0] == 'break':
            break
        for c in cmd:
            if c == 'start':
                command[order].append('start')
            elif c == 'stop':
                command[order].append('stop')
            elif c == 'exit':
                command[order].append('exit')
    sock.close()
    controller.pop(cnt)


def file_recv(ts: socket.socket, ta, register_name: str):
    global state, filenames
    i = control_available.index(register_name)
    filenames[i] = ''
    while True:
        global state
        if state[i] == 'stop':
            state[i] = ''
            time.sleep(2)
            ts.close()
            if not filenames[i] == '':
                os.remove("upload/{}.jpeg".format(filenames[i]))
            return
        recved = int(ts.recv(1024))
        if recved == -1:
            break
        ts.send(b'6')
        if not filenames[i] == '':
            os.remove("upload/{}.jpeg".format(filenames[i]))
        filenames[i] = ''
        for _ in range(20):
            if random.randint(0, 1):
                filenames[i] = filenames[i] + name_seed[random.randint(0, 35)]
            else:
                filenames[i] = filenames[i] + name_seed[random.randint(0, 35)].upper()
        with open("upload/{}.jpeg".format(filenames[i]), 'wb') as f:
            while recved > 0:
                c = ts.recv(524288)
                f.write(c)
                recved -= len(c)
        ts.send(b'ok')


while True:
    cs, ca = s_c.accept()
    type_ = cs.recv(1024)
    if type_ == b'controlled':
        print('一个被操控者上线')
        threading.Thread(target=ee, args=[cs, ca, ]).start()
    elif type_ == b'controller':
        print('一个操控者上线')
        threading.Thread(target=er, args=[cs, ca, ]).start()
