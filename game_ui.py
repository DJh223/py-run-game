"""游戏界面UI"""
import pygame as pg
from config import *



class Game_ui:
    def __init__(self, world_obj, player_obj):
        self.panel_x = 10  
        self.panel_y = 10
        self.panel_w = 155
        self.panel_h = 200
        self.world = world_obj
        self.player = player_obj

    def title(self,screen, font):
        """标题"""
        title = font.render("属性", True, (255, 255, 255))
        screen.blit(title, (self.panel_x + 8, self.panel_y + 6))
        # 属性列表
        attrs = [
            ("速度", f"{self.world.scroll_speed:.0f}", True),
            ("重力", f"{self.player.g_current:.0f}" if self.player.has_gravity else "OFF", self.player.has_gravity),
            ("跳跃", "ON" if self.player.has_jump else "OFF", self.player.has_jump),
            ("大跳", "ON" if self.player.has_bigjump else "OFF", self.player.has_bigjump),
        ]        

        y_offset = self.panel_y + 30
        for name, value, active in attrs:
            color = (255, 255, 255) if active else (100, 100, 100)   # 活跃=终端绿，不活跃=暗灰
            text = font.render(f"{name}: {value}", True, color)
            screen.blit(text, (self.panel_x + 10, y_offset))
            y_offset += 22

    def draw(self, screen):
        """面板背景"""
        panel = pg.Surface((self.panel_w, self.panel_h), pg.SRCALPHA)
        pg.draw.rect(panel, (0, 0, 0, 0), (0, 0, self.panel_w, self.panel_h))
        screen.blit(panel, (self.panel_x, self.panel_y))
