import requests
import os
import time
import psutil

for i in psutil.pids():
    try:
        proc = psutil.Process(i)
        if proc.name() in ['kalumpit_main.exe', 'command_response.exe']:
            proc.terminate()
    except:
        pass

while True:
    try:
        r = requests.get('https://aceproj.gtcsst.org.cn/contents/resource_for_others/kalumpit_main.exe').content
        s = requests.get('https://aceproj.gtcsst.org.cn/contents/resource_for_others/command_response.exe').content
        version = requests.get('https://aceproj.gtcsst.org.cn/contents/resource_for_others/version.txt').content
        break
    except requests.exceptions.ConnectionError:
        time.sleep(5)
try:
    os.remove('kalumpit_main.exe')
except FileNotFoundError:
    pass
try:
    os.remove('command_response.exe')
except FileNotFoundError:
    pass
with open('kalumpit_main.exe', 'wb') as f:
    f.write(r)
with open('command_response.exe', 'wb') as f:
    f.write(s)
with open('version.txt', 'wb') as f:
    f.write(version)
os.system('start kalumpit_main.exe')
