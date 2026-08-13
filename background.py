"""背景：建模软件视口风格，预渲染网格 + 无缝滚动"""

import pygame as pg

GRID_FINE = 8                       # 细网格间距
GRID_MAJOR = 80                     # 粗网格间距（方块 40 的两倍）


class Background:
    def __init__(self, w, h):
        self.resize(w, h)

    def resize(self, w, h):
        """全屏切换时重建预渲染画布"""
        self.bg_surf = pg.Surface((w, h))
        self.bg_surf.fill((63, 63, 63))

        self.grid_surf = pg.Surface((w, h), pg.SRCALPHA)
        for gx in range(0, w, GRID_FINE):
            pg.draw.line(self.grid_surf, (80, 80, 80, 40), (gx, 0), (gx, h), 1)
        for gy in range(0, h, GRID_FINE):
            pg.draw.line(self.grid_surf, (80, 80, 80, 40), (0, gy), (w, gy), 1)
        for gx in range(0, w, GRID_MAJOR):
            pg.draw.line(self.grid_surf, (80, 80, 80), (gx, 0), (gx, h), 1)
        for gy in range(0, h, GRID_MAJOR):
            pg.draw.line(self.grid_surf, (80, 80, 80), (0, gy), (w, gy), 1)

    def draw(self, screen, scroll_offset=0):
        ox = scroll_offset % GRID_MAJOR
        screen.blit(self.bg_surf, (0, 0))
        # 双图补位实现无缝横向滚动
        screen.blit(self.grid_surf, (-ox, 0))
        screen.blit(self.grid_surf, (screen.get_width() - ox, 0))
