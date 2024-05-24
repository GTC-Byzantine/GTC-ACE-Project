import socket

connect_state = False


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.100.55.185', 25566))
    s.send(b'controller')
    lis = s.recv(1024).decode()
    if lis == 'none':
        print('无可用')
        s.close()
        return
    print('你被编号为:', lis.split('/')[0])
    for i in lis.split('/')[1:]:
        print(i, end=' ')
    order = input('选择一个连接 (0 ~ n):')
    s.send(order.encode())
    s.close()


if __name__ == "__main__":
    while True:
        cmd = input('>>> ').split(' ')
        if cmd[0] == 'connect':
            connect()
        elif cmd[0] == 'exit':
            break
