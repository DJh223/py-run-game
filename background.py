import pygame as pg


class Background:
    def __init__(self, w, h):
        self.bg_surf = pg.Surface((w,h))
        self.bg_surf.fill((63, 63, 63))

        self.grid_surf = pg.Surface((w, h), pg.SRCALPHA)
        # 细网格（8px = 大格子80 ÷ 10）
        for gx in range(0, w, 8):
            pg.draw.line(self.grid_surf, (80, 80, 80, 40), (gx, 0), (gx, h), 1)
        for gy in range(0, h, 8):
            pg.draw.line(self.grid_surf, (80, 80, 80, 40), (0, gy), (w, gy), 1)
        # 粗网格（80px = 方块40×2）
        for gx in range(0, w, 80):
            pg.draw.line(self.grid_surf, (80, 80, 80), (gx, 0), (gx, h), 1)
        for gy in range(0, h, 80):
            pg.draw.line(self.grid_surf, (80, 80, 80), (0, gy), (w, gy), 1)
    def draw(self, screen, scroll_offset = 0):
        ox = scroll_offset % 80                     # 偏移量在 0~79 之间循环
        screen.blit(self.bg_surf, (0, 0))
        screen.blit(self.grid_surf, (-ox, 0))       # 左边部分
        screen.blit(self.grid_surf, (screen.get_width() - ox, 0))   # 右边补位

        

    