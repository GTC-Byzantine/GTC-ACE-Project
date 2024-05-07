import json
import sys
import requests
import time
import os
import shutil
import psutil
import zipfile

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


def support_gbk(zip_file: zipfile.ZipFile):
    name_to_info = zip_file.NameToInfo
    # copy map first
    for name, info in name_to_info.copy().items():
        real_name = name.encode('cp437').decode('gbk')
        if real_name != name:
            info.filename = real_name
            del name_to_info[name]
            name_to_info[real_name] = info
    return zip_file


def upload_pack(pack_name_e):
    try:
        zip_addr = 'packages/{}/{}.zip'.format(pack_name_e, pack_name_e)
        p = requests.get(
            'https://aceproj.gtcsst.org.cn/contents/packages/{}/{}.zip'.format(pack_name_e, pack_name_e))
        if str(p) == '<Response [404]>':
            return
        with open(zip_addr, 'wb') as f:
            f.write(p.content)
        with support_gbk(zipfile.ZipFile(zip_addr)) as zf:
            zf.extractall('packages/{}/{}'.format(pack_name_e, pack_name_e))
        ver = requests.get('https://aceproj.gtcsst.org.cn/'
                           'contents/packages/{}/config.txt'.format(pack_name_e))
        with open('packages/{}/config.txt'.format(pack_name_e), 'wb') as f:
            f.write(ver.content)
        os.remove(zip_addr)
    except requests.exceptions.ConnectionError:
        return


while True:
    try:
        r = requests.post(req_url + 'overall.php', data={'VALIDATE': 'GTC contre project'})
    except requests.exceptions.ConnectionError:
        if req_url.count('kc') >= 1:
            os.system('rundll32.exe user32.dll LockWorkStation')
            time.sleep(30)
        else:
            time.sleep(5)
        continue
    command = r.text.split('\n')
    print(command)
    for one in command:
        single = one.split(' ')
        if single[0] == 'redownload':
            os.system('start updater.exe')
        elif single[0] == 'clear':
            dirs = os.listdir(storage_path)
            for item in dirs:
                if os.path.isfile(os.path.join(storage_path, item)):
                    os.remove(os.path.join(storage_path, item))
                else:
                    shutil.rmtree(os.path.join(storage_path, item), ignore_errors=True)
        elif single[0] == 'upload':
            target_path = one[7:]
            if not os.path.isdir(os.path.join(storage_path, target_path)):
                try:
                    temp_file = open(os.path.join(storage_path, target_path), 'rb')
                    file_object = {
                        'type': (None, '6', None),
                        'orgType': (None, 'B', None),
                        'file': (os.path.basename(target_path), temp_file, 'unknown')
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

            else:
                try:
                    zipf = zipfile.ZipFile(os.path.basename(target_path) + '.zip', 'w', zipfile.ZIP_DEFLATED)
                    path = os.path.join(storage_path, target_path)
                    for root, dirs, files in os.walk(path):
                        relative_root = '' if root == path else root.replace(path, '') + os.sep
                        for filename in files:
                            zipf.write(os.path.join(root, filename), relative_root + filename)
                    zipf.close()
                    temp_file = open(os.path.basename(target_path) + '.zip', 'rb')
                    file_object = {
                        'type': (None, '6', None),
                        'orgType': (None, 'B', None),
                        'file': (os.path.basename(target_path) + '.zip', temp_file, 'unknown')
                    }
                except:
                    continue
            requests.post(req_url + 'upload.php', headers=header, files=file_object)
            time.sleep(1)
            temp_file.close()

        elif single[0] == 'shutdown':
            os.system('shutdown -s -t 0')
        elif single[0] == 'lock':
            os.system('rundll32.exe user32.dll LockWorkStation')
        elif single[0] == 'pack':
            if len(single) <= 1:
                continue
            pack_name = single[1]
            if not os.path.exists('packages'):
                os.mkdir('packages')
            if not os.path.exists(os.path.join('packages', pack_name)):
                os.makedirs(os.path.join('packages', pack_name, pack_name))
                upload_pack(pack_name)
            with open(f'packages/{pack_name}/config.txt') as f:
                config = f.readlines()[0]
            config = json.loads(config)
            try:
                r = requests.get(f'https://aceproj.gtcsst.org.cn/contents/packages/{pack_name}/config.txt')
                config_cloud = json.loads(r.text)
                if config_cloud['version'] != config['version']:
                    shutil.rmtree(f'packages/{pack_name}')
                    os.makedirs(os.path.join('packages', pack_name, pack_name))
                    upload_pack(pack_name)
            except requests.exceptions.ConnectionError:
                pass
            cwd = os.getcwd()
            os.chdir(f'packages/{pack_name}/{pack_name}')
            os.system(f'start {config["exe"]}')
            os.chdir(cwd)
    time.sleep(9)
