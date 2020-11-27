MID_TEXT = str(input("请输入信息："))

import random
import pygame

PANEL_width = 1920
PANEL_height = 1080
FONT_PX = 15

pygame.init()

# 创建一个可是窗口

winSur = pygame.display.set_mode((PANEL_width, PANEL_height), pygame.FULLSCREEN|pygame.NOFRAME|pygame.RESIZABLE)

font = pygame.font.SysFont("123.ttf", 25)
mid_font = pygame.font.SysFont("microsoftyaheimicrosoftyaheiui", 50)

bg_surface = pygame.Surface((PANEL_width, PANEL_height), flags=pygame.SRCALPHA)

pygame.Surface.convert(bg_surface)

bg_surface.fill(pygame.Color(0, 0, 0, 28))

winSur.fill((0, 0, 0))

# 数字版

# texts = [font.render(str(i), True, (0, 255, 0)) for i in range(10)]


# 字母版

letter = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c',

          'v', 'b', 'n', 'm']

texts = [
    font.render(str(letter[i]), True, (0, 255, 0)) for i in range(26)
]

mid_text = mid_font.render(MID_TEXT, True, (255, 255, 255))
mid_pos = ((PANEL_width-mid_text.get_width())//2, (PANEL_height-mid_text.get_height())//2)

# 按屏幕的宽带计算可以在画板上放几列坐标并生成一个列表

column = int(PANEL_width / FONT_PX)

drops = [0 for i in range(column)]

while True:
    # 从队列中获取事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_ESCAPE]):
                exit()

    # 将暂停一段给定的毫秒数
    pygame.time.delay(30)

    # 重新编辑图像第二个参数是坐上角坐标
    winSur.blit(bg_surface, (0, 0))
    for i in range(len(drops)):
        text = random.choice(texts)
        # 重新编辑每个坐标点的图像
        winSur.blit(text, (i * FONT_PX, drops[i] * FONT_PX))
        drops[i] += 1
        if drops[i] * 10 > PANEL_height or random.random() > 0.95:
            drops[i] = 0

    winSur.blit(mid_text, mid_pos)


    pygame.display.flip()
