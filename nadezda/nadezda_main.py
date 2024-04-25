import time
import pygame
import requests
import button_support
import threading

screen = pygame.display.set_mode((1024, 578))

clock = pygame.time.Clock()

bgi = pygame.image.load('image/KILLSWITCH-IMG-2-1024x578.jpg').convert_alpha()
bgi.set_alpha(120)
last_state_br = False
last_state_bru = False
last_state_brd = False
refreshing = False
locked = False
last_state_controlling = 0
blank_pos = 0
delay = 0  # 至多 9
eps = 18
button_refresh = button_support.FeedbackButton((50, 30), (10, 15), '刷新', 20, screen, (255, 255, 255),
                                               (255, 255, 255))
button_up = button_support.FeedbackButton((30, 30), (300, 480), '↑', 20, screen, (255, 255, 255),
                                          (255, 255, 255))
button_down = button_support.FeedbackButton((30, 30), (300, 520), '↓', 20, screen, (255, 255, 255),
                                            (255, 255, 255))
button_getinfo = button_support.FeedbackButton((50, 30), (500, 274), '拉取', 20, screen, (255, 255, 255),
                                               (255, 255, 255))
button_upload_command = button_support.FeedbackButton((150, 34), (375, 70), '命令控制器 =>', 20, screen, (255, 255, 255),
                                               (255, 255, 255))
class_bar = []  # [班级名称, 最后活动时间, 版本] -1 表示 无
start_pos = 0
controlling = 0
disk_usage = 0


def load_info(class_name):
    global disk_usage
    url = 'https://aceproj.gtcsst.org.cn/contents/file_de_class/{}/'
    res = requests.get(url.format(class_name) + 'usage.txt').text
    if res.count('404 Not Found') >= 1:
        disk_usage = '未找到文件'
        return
    disk_usage = round(float(res), 3)


def refresh():
    global class_bar, refreshing
    refreshing = True
    class_list = requests.get('https://aceproj.gtcsst.org.cn/config.txt').text.split('\n')
    class_bar.clear()
    class_bar = [[] for _ in class_list]
    threads = []
    for cur in range(len(class_list)):
        threads.append(threading.Thread(target=refresh_each, args=[cur, class_list[cur]]))
        threads[cur].start()
    for cur in range(len(threads)):
        threads[cur].join()
    refreshing = False
    if class_bar[-1][0] == '':
        class_bar.pop(-1)
    class_bar.sort(key=lambda x: x[0])


def refresh_each(cur, class_name):
    global class_bar
    class_pos = 'https://aceproj.gtcsst.org.cn/contents/file_de_class/{}/'
    current_class = class_pos.format(class_name)
    a1 = requests.get(current_class + 'last_active_time.txt').text
    a2 = requests.get(current_class + 'version.txt').text
    if a1.count('404 Not Found') >= 1:
        a1 = '-1'
    if a2.count('404 Not Found') >= 1:
        a2 = 'UNKNOWN'
    class_bar[cur] = [class_name, a1, a2]


def active_div1():
    global last_state_br, last_state_bru, start_pos, last_state_brd, delay, blank_pos, controlling
    top_pos = 60 + start_pos
    font_topic = pygame.font.SysFont('consolas', 20)
    font_annotation = pygame.font.SysFont('consolas', 10)
    if not refreshing:
        for item in class_bar:
            screen.blit(font_topic.render(item[0], True, (0, 0, 0)), (10, top_pos + 3))
            screen.blit(font_annotation.render(item[2], True, (0, 0, 0)), (10, top_pos + 25))
            screen.blit(
                font_annotation.render('Last active ' + str((int(time.time()) - int(item[1]))) + ' seconds ago', True,
                                       (0, 0, 0)), (10, 36 + top_pos))
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
    if mouse_pos[0] <= 350 and mouse_pos[1] >= 60:
        controlling = (mouse_pos[1] - start_pos - 60) // 50
        if controlling < len(class_bar):
            blank_pos = (mouse_pos[1] - start_pos - 60) // 50 * 50 + 60 + start_pos
        else:
            blank_pos = 0
    pygame.draw.rect(screen, (30, 30, 255), (0, blank_pos, 350, 50), 4, 5)

    screen.fill((255, 255, 255), (0, 0, 350, 60))
    button_refresh.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    if not last_state_br and button_refresh.state and not refreshing:
        threading.Thread(target=refresh).start()
    last_state_br = button_refresh.state
    if refreshing:
        text_remind_refresh = pygame.font.SysFont('microsoftyahei', 20).render('刷新中...', True, (130, 130, 130))
        screen.blit(text_remind_refresh, (70, 15))


def active_div2():
    global locked, last_state_controlling
    if controlling < len(class_bar) and not refreshing and not locked:
        font_sc = pygame.font.SysFont('consolas', 20)
        text_class_notice = font_sc.render(class_bar[controlling][0], True, (0, 0, 0))
        ls_rect = pygame.Rect(text_class_notice.get_rect())
        ls_rect.center = (525, 259)
        screen.blit(text_class_notice, ls_rect)
        button_getinfo.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
        if button_getinfo.state:
            locked = True
            load_info(class_bar[controlling][0])

    elif controlling < len(class_bar) and not refreshing:
        if last_state_controlling != controlling:
            locked = False
        font = pygame.font.SysFont('microsoftyahei', 25, bold=True)
        screen.blit(font.render('磁盘空间剩余：{}G'.format(disk_usage), True, (0, 0, 0)), (375, 30))
        button_upload_command.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])


    else:
        if last_state_controlling != controlling:
            locked = False

    last_state_controlling = controlling


def main():
    global start_pos, delay
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
        start_pos += delay
        if delay > 0:
            delay -= 1
        elif delay < 0:
            delay += 1
        start_pos = min(start_pos, 0)
        start_pos = max((max(len(class_bar) - 8, 0) * -50, start_pos))
        screen.fill((255, 255, 255))
        screen.blit(bgi, (0, 0))
        screen.fill((0, 0, 0), (350, 0, 2, 578))
        screen.fill((0, 0, 0), (700, 0, 2, 578))
        active_div1()
        active_div2()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
