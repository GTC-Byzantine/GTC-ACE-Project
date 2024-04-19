import pygame
import requests
import button_support
import threading

screen = pygame.display.set_mode((1024, 578))

clock = pygame.time.Clock()

bgi = pygame.image.load('image/KILLSWITCH-IMG-2-1024x578.jpg').convert_alpha()
bgi.set_alpha(120)
last_state_br = False
refreshing = False
button_refresh = button_support.FeedbackButton((50, 30), (200, 15), '刷新', 20, screen, (255, 255, 255),
                                               (255, 255, 255), font_type='image/13111.ttf')
class_bar = []  # [班级名称, 最后活动时间, 版本] -1 表示 无


def refresh():
    global class_bar, refreshing
    refreshing = True
    class_list = requests.get('https://aceproj.gtcsst.org.cn/config.txt').text.split('\n')
    class_bar.clear()
    class_pos = 'https://aceproj.gtcsst.org.cn/contents/file_de_class/{}/'
    for class_name in class_list:
        current_class = class_pos.format(class_name)
        a1 = requests.get(current_class + 'last_active_time.txt').text
        a2 = requests.get(current_class + 'version.txt').text
        if a1.count('404 Not Found') >= 1:
            a1 = '-1'
        if a2.count('404 Not Found') >= 1:
            a2 = 'UNKNOWN'
        class_bar.append([class_name, a1, a2])
    refreshing = False
    print(class_bar)


def active_div1():
    global last_state_br
    button_refresh.operate(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3)[0])
    if not last_state_br and button_refresh.state:
        threading.Thread(target=refresh).start()
    last_state_br = button_refresh.state

    if refreshing:
        text_remind_refresh = pygame.font.Font('image/13111.ttf', 20).render('刷新中...', True, (0, 0, 0))
        screen.blit(text_remind_refresh, (270, 15))


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((255, 255, 255))
        screen.blit(bgi, (0, 0))
        screen.fill((0, 0, 0), (350, 0, 2, 578))
        screen.fill((0, 0, 0), (700, 0, 2, 578))

        active_div1()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
