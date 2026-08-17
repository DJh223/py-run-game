"""主菜单UI"""
import pygame as pg
from config import *

class Menu_ui:
    def __init__(self, scale):
        # 按钮参数（放在初始化部分，或单独一个函数里）
        self.button_rect = pg.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 30, 150, 60)
        self.button_color = (255, 255, 255, 200)     
        self.button_hover_color = (245, 245, 245, 200) 
        self.button_text = "开始游戏"
    def draw(self, screen, font):
        """开始按钮"""
        panel = pg.Surface((150, 60), pg.SRCALPHA)
        mouse_pos = pg.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            pg.draw.rect(panel, self.button_hover_color, (0, 0, 150, 60), border_radius=10)
            screen.blit(panel, self.button_rect.topleft)
        else:
            pg.draw.rect(panel, self.button_color, (0, 0, 150, 60), border_radius=10)
            screen.blit(panel, self.button_rect.topleft)
        
        # 画按钮文字
        text_surface = font.render(self.button_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        screen.blit(text_surface, text_rect)