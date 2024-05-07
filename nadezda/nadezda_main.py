import json
import os.path
import time
import pygame
import requests
import button_support
import threading
import easygui

screen = pygame.display.set_mode((1024, 578))

clock = pygame.time.Clock()

bgi = pygame.image.load('image/KILLSWITCH-IMG-2-1024x578.jpg').convert_alpha()
bgi.set_alpha(120)
last_state_br = False
last_state_bru = False
last_state_brd = False
last_state_rff = False
last_state_bru_f = False
last_state_brd_f = False
last_state_del = False
last_state_open = False
last_state_add = False
last_state_clear = False
last_state_type = False
refreshing = False
locked = False
last_state_controlling = 0
blank_pos = 0
delay = 0
eps = 18
eps2 = 16
file_list = []
file_show_surface = pygame.Surface((340, 380))
button_refresh = button_support.FeedbackButton((50, 30), (10, 15), '刷新', 20, screen, (255, 255, 255),
                                               (255, 255, 255), font_type='image/fzcq.ttf')
button_up = button_support.FeedbackButton((30, 30), (300, 480), '↑', 20, screen, (255, 255, 255),
                                          (255, 255, 255))
button_down = button_support.FeedbackButton((30, 30), (300, 520), '↓', 20, screen, (255, 255, 255),
                                            (255, 255, 255))
button_getinfo = button_support.FeedbackButton((50, 30), (500, 274), '拉取', 20, screen, (255, 255, 255),
                                               (255, 255, 255), font_type='image/fzcq.ttf')
button_upload_command = button_support.FeedbackButton((150, 34), (375, 80), '命令控制器 =>', 20, screen,
                                                      (255, 255, 255),
                                                      (255, 255, 255), font_type='image/fzcq.ttf')
button_load_file = button_support.FeedbackButton((140, 34), (375, 134), '拉取文件列表', 20, screen, (255, 255, 255),
                                                 (255, 255, 255), font_type='image/fzcq.ttf')
button_delete = button_support.FeedbackButton((45, 28), (315, -50), '删除', 15, screen, (255, 255, 255),
                                              (0, 0, 0), font_type='image/fzcq.ttf')
button_open = button_support.FeedbackButton((45, 28), (315, -50), '打开', 15, screen, (255, 255, 255),
                                            (0, 0, 0), font_type='image/fzcq.ttf')
button_up_file = button_support.FeedbackButton((30, 30), (620, 133), '↑', 20, screen, (255, 255, 255),
                                               (255, 255, 255))
button_down_file = button_support.FeedbackButton((30, 30), (660, 133), '↓', 20, screen, (255, 255, 255),
                                                 (255, 255, 255))
button_add = button_support.FeedbackButton((45, 30), (315, -50), '添加', 15, screen, (255, 255, 255),
                                           (0, 0, 0), font_type='image/fzcq.ttf')
button_clear = button_support.FeedbackButton((45, 30), (969, 200), '清除', 15, screen, (255, 255, 255),
                                             (0, 0, 0), font_type='image/fzcq.ttf')
button_type = button_support.FeedbackButton((45, 30), (710, 200), '键入', 15, screen, (255, 255, 255),
                                            (0, 0, 0), font_type='image/fzcq.ttf')
class_bar = []  # [班级名称, 最后活动时间, 版本] -1 表示 无
start_pos = 0
controlling = 0
disk_usage = 0
delay_file = 0
start_pos_file = 0
blank_pos_file = 0
cmd = ['shutdown', 'lock', 'redownload', 'clear']
current_command = []
timer_cmd = 0


def load_file_list(class_name):
    return requests.post('https://aceproj.gtcsst.org.cn/contents/file_de_class/scanf.php',
                         data={'class_name': class_name}).text


def download(class_name, file_name):
    if os.path.exists(os.path.join('downloads', file_name)):
        return os.path.join('downloads', file_name)
    with open(os.path.join('downloads', file_name), 'wb') as f:
        content = requests.get('https://aceproj.gtcsst.org.cn/contents/file_de_class/{}/upload/{}'.
                               format(class_name, file_name)).content
        if content.count(b'404 Not Found'):
            return 0
        f.write(content)
    return os.path.join('downloads', file_name)


def input_command():
    return easygui.enterbox('输入指令')


def clear_command_list(class_name):
    return requests.post('https://aceproj.gtcsst.org.cn/contents/file_de_class/{}/overall.php'.format(class_name),
                         data={'VALIDATE': 'GTC contre project'})


def open_file(filename):
    os.system('"{}"'.format(filename))


def load_command(class_name):
    return requests.get(
        'https://aceproj.gtcsst.org.cn/contents/file_de_class/{}/wonder_list.txt'.format(class_name)).text


def delete_file(file_path):
    requests.post('https://aceproj.gtcsst.org.cn/contents/file_de_class/delete.php', data={'path': file_path})


def refresh():
    global class_bar, refreshing
    refreshing = True
    user, password = ['SU', '998244353']
    res = requests.post("https://aceproj.gtcsst.org.cn/contents/allocate/res.php",
                        data={'user': str(user), 'password': str(password)})
    lis = json.loads(res.text)
    class_bar = []
    for cl in lis:
        for item in cl:
            if item == 'state' and cl[item] != 'Success':
                easygui.msgbox('登录失败')
            elif item != 'state':
                if item == 'class':
                    class_bar.append([cl[item]])
                else:
                    class_bar[-1].append(cl[item])
    refreshing = False
    class_bar.sort(key=lambda x: x[0])


def active_div1():
    global last_state_br, last_state_bru, start_pos, last_state_brd, delay, blank_pos, controlling
    top_pos = 60 + start_pos
    font_topic = pygame.font.Font('image/fzcq.ttf', 20)
    font_annotation = pygame.font.Font('image/fzcq.ttf', 10)
    if not refreshing:
        for item in class_bar:
            screen.blit(font_topic.render(item[0], True, (0, 0, 0)), (10, top_pos + 3))
            screen.blit(font_annotation.render(item[2], True, (0, 0, 0)), (10, top_pos + 25))
            screen.blit(
                font_annotation.render('Last active ' + str((int(time.time()) - int(item[1]))) + ' seconds ago', True,
                                       (0, 0, 0)), (10, 36 + top_pos))
            screen.blit(font_annotation.render('Remains {} G'.format(round(float(item[3])), 3), True, (0, 0, 0)),
                        (250, 36 + top_pos))
            pygame.draw.rect(screen, (0, 0, 0), (0, top_pos, 350, 50), 2, 9)
            top_pos += 50

    button_up.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    if not last_state_bru and button_up.state:
        delay = eps
    last_state_bru = button_up.state
    button_down.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    if not last_state_brd and button_down.state:
        delay = -eps
    last_state_brd = button_down.state

    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] <= 350 and mouse_pos[1] >= 60 and pygame.mouse.get_pressed(3)[0]:
        controlling = (mouse_pos[1] - start_pos - 60) // 50
        if controlling < len(class_bar):
            blank_pos = controlling * 50 + 60 + start_pos
        else:
            blank_pos = 0
    blank_pos = controlling * 50 + 60 + start_pos
    pygame.draw.rect(screen, (30, 30, 255), (0, blank_pos, 350, 50), 4, 5)

    screen.fill((255, 255, 255), (0, 0, 350, 60))
    button_refresh.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    if not last_state_br and button_refresh.state and not refreshing:
        threading.Thread(target=refresh).start()
    last_state_br = button_refresh.state
    if refreshing:
        text_remind_refresh = pygame.font.Font('image/fzcq.ttf', 20).render('刷新中...', True, (130, 130, 130))
        screen.blit(text_remind_refresh, (70, 20))


def active_div2():
    global locked, last_state_controlling, last_state_rff, file_list, blank_pos_file, last_state_brd_f, \
        last_state_bru_f, delay_file, last_state_del, current_con, timer_cmd
    locked = True

    if controlling < len(class_bar) and not refreshing:
        if last_state_controlling != controlling:
            locked = False
        font = pygame.font.Font('image/fzcq.ttf', 25)
        screen.blit(
            font.render('磁盘空间剩余：{} G'.format(round(float(class_bar[controlling][3])), 3), True, (0, 0, 0)),
            (375, 30))
        button_load_file.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        if (not last_state_rff and button_load_file.state) or (timer_cmd >= 59):
            file_list = load_file_list(class_bar[controlling][0]).split('\n')
            file_list.remove('.')
            file_list.remove('..')
            timer_cmd = 0
        last_state_rff = button_load_file.state

        file_show_surface.fill((255, 255, 255))
        button_up_file.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        if not last_state_bru_f and button_up_file.state:
            delay_file = eps2
        last_state_bru_f = button_up.state
        button_down_file.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        if not last_state_brd_f and button_down_file.state:
            delay_file = -eps2
        last_state_brd_f = button_down.state
        mouse_pos = list(pygame.mouse.get_pos())
        mouse_pos[1] -= 183
        mouse_pos[0] -= 356
        if 0 <= mouse_pos[0] <= 340 and 0 <= mouse_pos[1] <= 380:
            if len(file_list) > 0:
                current_con = (mouse_pos[1] - start_pos_file) // 20
                if current_con < len(file_list):
                    blank_pos_file = (mouse_pos[1] - start_pos_file) // 20 * 20 + start_pos_file
                    button_delete.change_pos((650, blank_pos_file + 183 - 4))
                    button_open.change_pos((605, blank_pos_file + 183 - 4))
                else:
                    blank_pos_file = -50
                    button_delete.change_pos((650, -50))
                    button_open.change_pos((605, -50))
                file_show_surface.fill((137, 137, 137), (0, blank_pos_file, 340, 20))
            else:
                button_delete.change_pos((650, -50))
        pos = start_pos_file
        font = pygame.font.Font('image/fzcq.ttf', 15)
        for file in file_list:
            file_show_surface.blit(font.render(file, True, (0, 0, 0)), (5, 2 + pos))
            pos += 20
        screen.blit(file_show_surface, (356, 183))
        if len(file_list) > 0 and 0 <= mouse_pos[0] <= 340 and 0 <= mouse_pos[1] <= 380:
            button_delete.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
            button_open.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
            if not last_state_del and button_delete.state:
                path = class_bar[controlling][0] + '/upload/' + file_list[current_con]
                delete_file(path)
            elif last_state_del and not button_delete.state:
                file_list = load_file_list(class_bar[controlling][0]).split('\n')
                file_list.remove('.')
                file_list.remove('..')
            if not last_state_open and button_open.state:
                feedback = download(class_bar[controlling][0], file_list[current_con])
                if feedback != 0:
                    # threading.Thread(target=open_file, args=[feedback]).start()
                    open_file(feedback)
            last_state_del = button_delete.state
    else:
        if last_state_controlling != controlling:
            locked = False

    last_state_controlling = controlling


def active_div3():
    global last_state_add, current_command, timer_cmd, last_state_clear, last_state_type
    if controlling < len(class_bar) and not refreshing:
        timer_cmd += 1
        mouse_pos = pygame.mouse.get_pos()
        if 700 <= mouse_pos[0] <= 1024 and 65 <= mouse_pos[1] <= 185:
            selected = (mouse_pos[1] - 65) // 30
            blank = selected * 30 + 65
            screen.fill((137, 137, 137), (705, blank, 314, 30))
            button_add.change_pos((969, blank))
            button_add.operate(mouse_pos, pygame.mouse.get_pressed(3)[0])
            if not last_state_add and button_add.state:
                if selected <= 3:
                    requests.post('https://aceproj.gtcsst.org.cn/contents/file_de_class/{}/iwonder.php'.format(
                        class_bar[controlling][0]), data={'cmd': cmd[selected]})
            if last_state_add and not button_add.state:
                current_command = load_command(class_bar[controlling][0]).split('\n')
            last_state_add = button_add.state
        if timer_cmd >= 60:
            current_command = load_command(class_bar[controlling][0]).split('\n')
        button_type.operate(mouse_pos, pygame.mouse.get_pressed(3)[0])
        if not last_state_type and button_type.state:
            command = input_command()
            if command is not None:
                requests.post('https://aceproj.gtcsst.org.cn/contents/file_de_class/{}/iwonder.php'.format(
                    class_bar[controlling][0]), data={'cmd': command})
                current_command = load_command(class_bar[controlling][0]).split('\n')
        last_state_type = button_type.state
        button_clear.operate(mouse_pos, pygame.mouse.get_pressed(3)[0])
        if not last_state_clear and button_clear.state:
            print(clear_command_list(class_bar[controlling][0]).text)
            current_command = load_command(class_bar[controlling][0]).split('\n')
        last_state_clear = button_clear.state
        screen.fill((255, 255, 255), (710, 240, 304, 368))
        font_cmd = pygame.font.Font('image/fzcq.ttf', 15)
        pos = 240
        for cmds in current_command:
            screen.blit(font_cmd.render(cmds, True, (0, 0, 0)), (715, pos))
            pos += 15
        timer_cmd %= 60
        font = pygame.font.Font('image/fzcq.ttf', 20)
        screen.blit(font.render('快速指令', True, (0, 0, 0)), (710, 10))
        font_russia = pygame.font.Font('image/21-font.otf', 20)
        screen.blit(font_russia.render('Что-то удивительное...', True, (0, 0, 0)), (710, 40))
        screen.blit(font_russia.render('выключать', True, (30, 30, 255)), (710, 70))
        screen.blit(font_russia.render('блокировка', True, (30, 30, 255)), (710, 100))
        screen.blit(font_russia.render('перезакачать', True, (30, 30, 255)), (710, 130))
        screen.blit(font.render('删库跑路', True, (30, 30, 255)), (710, 160))


def main():
    global start_pos, delay, delay_file, start_pos_file
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] <= 350:
                    if event.button == 5:
                        delay = -eps
                    elif event.button == 4:
                        delay = eps
                elif 356 <= pygame.mouse.get_pos()[0] <= 696 and 183 <= pygame.mouse.get_pos()[1] <= 563:
                    if event.button == 5:
                        delay_file = -eps2
                    elif event.button == 4:
                        delay_file = eps2
        start_pos += delay
        start_pos_file += delay_file
        if delay > 0:
            delay -= 1
        elif delay < 0:
            delay += 1
        if delay_file > 0:
            delay_file -= 1
        elif delay_file < 0:
            delay_file += 1
        start_pos = min(start_pos, 0)
        start_pos_file = min(start_pos_file, 0)
        start_pos = max((max(len(class_bar) - 8, 0) * -50, start_pos))
        start_pos_file = max((max(len(file_list) - 20, 0) * -20, start_pos_file))
        screen.fill((255, 255, 255))
        screen.blit(bgi, (0, 0))
        screen.fill((0, 0, 0), (350, 0, 2, 578))
        screen.fill((0, 0, 0), (700, 0, 2, 578))
        active_div1()
        active_div2()
        active_div3()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
