"""玩家：物理、跳跃、碰撞"""

import pygame as pg
from config import *


class Player:
    def __init__(self, x=PLAYER_START_X, y=PLAYER_START_Y):
        self.x = float(x)                                   # 浮点 x 坐标
        self.y = float(y)                                   # 浮点 y 坐标
        self.vy = 0.0                                       # 垂直速度（负 = 向上）
        self.rect = pg.Rect(int(self.x), int(self.y), 40, 40)  # 碰撞/绘制用 Rect
        self.old_bottom = self.rect.bottom                  # 上一帧脚底位置（穿越检测用）

        self.g_current = float(GRAVITY_NORMAL)              # 当前重力（可变，长按时渐变降低）
        self.on_ground = True                               # 是否站在平台上
        self.can_hold = True                                # 这一跳是否还允许长按
        self.hold_time = 0.0                                # 当前按住累计时长（秒）
        self.hold_triggered = False                         # 这一跳是否已经开启了轻重力

    def apply_gravity(self, dt: float):
        """空中时累加重力，长按触发后重力渐变降低"""
        if self.on_ground:
            return

        if self.hold_triggered:
            self.g_current -= GRAVITY_FADE * dt
            if self.g_current < GRAVITY_MIN:
                self.g_current = GRAVITY_MIN
        else:
            self.g_current = float(GRAVITY_NORMAL)

        self.vy += self.g_current * dt
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
        self.hold_triggered = False

    def update_long_press(self, keys, dt: float):
        """空中按住空格超过阈值 → 开启轻重力"""
        if not self.on_ground and keys[pg.K_SPACE] and self.can_hold:
            self.hold_time += dt
            if self.hold_time >= HOLD_THRESHOLD and not self.hold_triggered:
                self.hold_triggered = True
        else:
            self.hold_time = 0.0
            self.g_current = float(GRAVITY_NORMAL)
            if not keys[pg.K_SPACE]:
                self.can_hold = False               # 空中松手，这一跳不能再长按

    def draw(self, screen, camera_y: float):
        """绘制玩家方块（屏幕坐标 = 世界坐标 - 摄像机偏移）"""
        pg.draw.rect(screen, (178, 139, 213),
                     (int(self.x), int(self.y - camera_y), 40, 40))
