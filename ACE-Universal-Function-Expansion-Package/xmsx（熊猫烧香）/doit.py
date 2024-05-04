import os, pygame, random
import ctypes
from ctypes import wintypes

# os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(random.randint(0, 1920), random.randint(0, 1080))
size = random.randint(400, 600)
screen = pygame.display.set_mode((size, size), pygame.NOFRAME)

user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = wintypes.HWND
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
user32.SetWindowPos(pygame.display.get_wm_info()['window'], -1, random.randint(0, 1600), random.randint(0, 900), 0, 0, 0x0001)

img = pygame.image.load('xmsx - 副本 ({}).jpg'.format(random.randint(2, 28)))
img = pygame.transform.scale(img, (size, size))
screen.blit(img, (0, 0))

pygame.display.flip()
clock = pygame.time.Clock()
for _ in range(180):

    for _ in pygame.event.get():
        pass
    # windll.user32.SetWindowPos(pygame.display.get_wm_info()['window'], -1, random.randint(0, 1920), random.randint(0, 1080), 0, 0, 0x0001)
    clock.tick(30)
pygame.display.quit()
