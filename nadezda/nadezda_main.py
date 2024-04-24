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
delay = 0  # 至多 9
eps = 13
button_refresh = button_support.FeedbackButton((50, 30), (10, 15), '刷新', 20, screen, (255, 255, 255),
                                               (255, 255, 255))
button_up = button_support.FeedbackButton((30, 30), (300, 480), '↑', 20, screen, (255, 255, 255),
                                          (255, 255, 255))
button_down = button_support.FeedbackButton((30, 30), (300, 520), '↓', 20, screen, (255, 255, 255),
                                            (255, 255, 255))
class_bar = []  # [班级名称, 最后活动时间, 版本] -1 表示 无
start_pos = 0


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
    global last_state_br, last_state_bru, start_pos, last_state_brd, delay
    top_pos = 60 + start_pos
    font_topic = pygame.font.SysFont('SimHei', 20)
    font_annotation = pygame.font.SysFont('SimHei', 10)
    if not refreshing:
        screen.fill((0, 0, 0), (0, top_pos, 350, 1))
        for item in class_bar:
            screen.blit(font_topic.render(item[0], True, (0, 0, 0)), (10, top_pos + 3))
            screen.blit(font_annotation.render(item[2], True, (0, 0, 0)), (10, top_pos + 25))
            screen.blit(font_annotation.render('最后活动于' + str((int(time.time()) - int(item[1]))) + '秒前', True,
                                               (0, 0, 0)), (10, 36 + top_pos))
            screen.fill((0, 0, 0), (0, top_pos + 50, 350, 1))
            top_pos += 50
    screen.fill((255, 255, 255), (0, 0, 350, 60))
    button_refresh.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    if not last_state_br and button_refresh.state and not refreshing:
        threading.Thread(target=refresh).start()
    last_state_br = button_refresh.state

    if refreshing:
        text_remind_refresh = pygame.font.SysFont('SimHei', 20).render('刷新中...', True, (130, 130, 130))
        screen.blit(text_remind_refresh, (70, 20))

    button_up.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    if not last_state_bru and button_up.state:
        delay = eps
    last_state_bru = button_up.state
    button_down.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    if not last_state_brd and button_down.state:
        delay = -eps
    last_state_brd = button_down.state


def main():
    global start_pos, delay
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        screen.fill((255, 255, 255))
        screen.blit(bgi, (0, 0))
        screen.fill((0, 0, 0), (350, 0, 2, 578))
        screen.fill((0, 0, 0), (700, 0, 2, 578))
        active_div1()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
