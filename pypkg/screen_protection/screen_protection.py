#! /usr/bin/python3

import sys
import random
import string

import pygame

def main_interface():

    mid_text = input("请输入显示的信息：")
    main(mid_text)

    
def main(mid_text):
    pygame.init()

    infoObject = pygame.display.Info()
    panel_width = infoObject.current_w
    panel_height = infoObject.current_h
    font_px = 15

    # 创建一个可视窗口
    winSur = pygame.display.set_mode(
        (panel_width, panel_height), pygame.FULLSCREEN | pygame.NOFRAME | pygame.RESIZABLE)
    winSur.fill((0, 0, 0))

    # 设置背景图片
    bg_surface = pygame.Surface(
        (panel_width, panel_height), flags=pygame.SRCALPHA)
    pygame.Surface.convert(bg_surface)
    bg_surface.fill(pygame.Color(0, 0, 0, 28))

    # 设置掉落的文字
    font = pygame.font.SysFont('arial', 25)
    texts = [font.render(c, True, (0, 255, 0)) for c in string.ascii_lowercase]

    # 设置中间文字的属性
    mid_font = pygame.font.SysFont("microsoftyaheimicrosoftyaheiui", 50)  # 微软雅黑，兼容中英输入
    mid_text = mid_font.render(mid_text, True, (255, 255, 255))
    mid_pos = ((panel_width-mid_text.get_width())//2,
            (panel_height-mid_text.get_height())//2)

    # 按屏幕的宽带计算可以在画板上放几列坐标并生成一个列表
    drops = [0 for _ in range(int(panel_width / font_px))]

    running_flag = True
    while running_flag:
        # 从队列中获取事件，任意键盘事件都可以退出程序
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                running_flag = False

        # 将暂停一段给定的毫秒数
        pygame.time.delay(30)

        # 编辑背景
        winSur.blit(bg_surface, (0, 0))
        
        # 编辑掉落的文字
        for i in range(len(drops)):
            text = random.choice(texts)
            # 重新编辑每个坐标点的图像
            winSur.blit(text, (i * font_px, drops[i] * font_px))
            drops[i] += 1
            if drops[i] * 10 > panel_height or random.random() > 0.95:
                drops[i] = 0

        # 编辑中间的文字
        winSur.blit(mid_text, mid_pos)

        pygame.display.flip()
    
    pygame.quit()

def __main__():
    import argparse

    if len(sys.argv) == 1:
        main_interface()
    else:
        parser = argparse.ArgumentParser("带可编辑信息的屏幕保护程序")
        parser.add_argument('text', type=str, help="显示的信息")
        args = parser.parse_args()

        main(args.text)
    
    sys.exit(0)

if __name__ == '__main__':
    __main__()
