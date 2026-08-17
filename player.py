"""玩家：物理、跳跃、碰撞"""

import pygame as pg
from config import *

class Player:
    def __init__(self, x=PLAYER_START_X, y=PLAYER_START_Y):
        self.x = float(x)                                   # 浮点 x 坐标
        self.y = float(y)                                   # 浮点 y 坐标
        self.vy = 0.0                                       # 垂直速度（负 = 向上）
        self.rect = pg.Rect(int(self.x), int(self.y), PLAYER_SIZE, PLAYER_SIZE)  # 碰撞/绘制用 Rect
        self.old_bottom = self.rect.bottom                  # 上一帧脚底位置（穿越检测用）

        self.on_ground = True                               # 是否站在平台上
        self.can_hold = True                                # 这一跳是否还允许长按
        self.hold_time = 0.0                                # 当前按住累计时长（秒）





    def apply_gravity(self, dt: float):
        """空中时加重力"""
        if self.on_ground:
            return
        self.vy += GRAVITY_NORMAL * dt
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

    def update_and_land(self, platforms: list, dt: float):
        """更新 y 位置，用穿越法检测落地。返回 (on_ground, collision_ground)"""
        self.old_bottom = self.rect.bottom
        self.y += self.vy * dt
        self.rect.y = int(self.y)

        self.on_ground = False
        collision_ground = False

        for plat in platforms:
            # 穿越法：脚底从平台上方穿到了下方，且 x 方向有重叠
            if (self.old_bottom <= plat.top
                    and self.rect.bottom >= plat.top
                    and self.vy >= 0
                    and self.rect.right > plat.left
                    and self.rect.left < plat.right):
                self.vy = 0
                self.rect.bottom = plat.top
                self.y = float(self.rect.y)
                self.on_ground = True
                collision_ground = True
                break
            else:
                collision_ground = False

        return self.on_ground, collision_ground

    def jump(self):
        """点按起跳，重置长按状态"""
        self.vy = BASE_JUMP
        self.on_ground = False
        self.can_hold = True
        self.hold_time = 0.0

    def update_long_press(self, keys, dt: float):
        """长按持续跳跃"""
        if not self.on_ground and keys[pg.K_SPACE] and self.can_hold :
            
            if self.hold_time <= HOLD_THRESHOLD:
                self.hold_time += dt
                self.vy += HOLD_BOOST * dt
        else:
            self.hold_time = 0.0
            if not keys[pg.K_SPACE]:
                self.can_hold = False               # 空中松手，这一跳不能再长按

    def draw(self, screen, camera_y: float, scale):
        """绘制玩家方块（屏幕坐标 = 世界坐标 - 摄像机偏移）"""
        pg.draw.rect(screen, (162, 164, 165),
                     (int(self.x) * scale, int(self.y - camera_y) * scale, 40 * scale, 40 * scale))
