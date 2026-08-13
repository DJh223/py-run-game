import pygame as pg
from config import *


class Data:
    def __init__(self):
        # 获取显示器原生分辨率
        info = pg.display.Info()
        native_w, native_h = info.current_w, info.current_h



    def zoom(self, screen_h) -> float:
        scale =  screen_h / SCREEN_HEIGHT               #缩放比例







