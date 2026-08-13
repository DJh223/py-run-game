"""缩放数据管理"""

import pygame as pg
from config import *


class Data:
    def __init__(self):
        info = pg.display.Info()
        self.native_w, self.native_h = info.current_w, info.current_h

    def zoom(self, screen_h) -> float:
        """当前屏幕高度相对基准高度的缩放比例"""
        return screen_h / SCREEN_HEIGHT
