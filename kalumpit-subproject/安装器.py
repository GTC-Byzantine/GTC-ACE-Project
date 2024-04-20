import requests
import os
from shutil import copy, copytree
from subprocess import run

print(os.getcwd())
class_name = input("班级名称？")
source_path = os.path.join(input('程序位置？【D:或E:】'), '.ace')
store_path = source_path[:2] + '\\.dir'

try:
    os.makedirs(store_path)
except FileExistsError:
    pass
copytree('Kalumpit_main', source_path)
os.popen('attrib +h %s' % source_path)
with open(os.path.join(source_path, 'storage.txt'), 'w') as f:
    f.write(store_path)
with open(os.path.join(source_path, 'version.txt'), 'w') as f:
    f.write('I don\'t know!!!')
with open(os.path.join(source_path, 'url.txt'), 'w') as f:
    f.write('https://aceproj.gtcsst.org.cn/contents/file_de_class/%s/' % class_name)
r = requests.post('https://aceproj.gtcsst.org.cn/Processer.php', data={'Req': 'New_Class_Register', 'Cont': class_name})
print(r.content.decode())
os.system('start %s' % os.path.join(source_path, 'updater.exe'))
print(os.path.join(source_path, 'kalumpit_main.exe'))
os.startfile(source_path)
run('explorer shell:startup', shell=True)
input('程序已启动，按回车退出')
