"""玩家：物理、跳跃、碰撞"""

import pygame as pg
from config import *


class Player:
    def __init__(self, x=PLAYER_START_X, y=PLAYER_START_Y):
        self.x = float(x)
        self.y = float(y)
        self.vy = 0.0
        self.rect = pg.Rect(int(self.x), int(self.y), 40, 40)
        self.old_bottom = self.rect.bottom   # 上一帧的底部，穿越检测用

        # 重力
        self.g_current = float(GRAVITY_NORMAL)

        # 状态
        self.on_ground = True
        self.can_hold = True
        self.hold_time = 0.0
        self.hold_triggered = False

    # ---- 重力 ----
    def apply_gravity(self, dt: float):
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

    # ---- 移动 + 穿越检测 ----
    def update_and_land(self, platforms: list, dt: float):
        """更新 y 位置，用穿越法检测落地。返回 (on_ground, collision_ground)"""
        self.old_bottom = self.rect.bottom
        self.y += self.vy * dt
        self.rect.y = int(self.y)

        self.on_ground = False
        collision_ground = False

        for plat in platforms:
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

    # ---- 起跳 ----
    def jump(self):
        self.vy = BASE_JUMP
        self.on_ground = False
        self.can_hold = True
        self.hold_time = 0.0
        self.hold_triggered = False

    # ---- 长按 ----
    def update_long_press(self, keys, dt: float):
        if not self.on_ground and keys[pg.K_SPACE] and self.can_hold:
            self.hold_time += dt
            if self.hold_time >= HOLD_THRESHOLD and not self.hold_triggered:
                self.hold_triggered = True
        else:
            self.hold_time = 0.0
            self.g_current = float(GRAVITY_NORMAL)
            if not keys[pg.K_SPACE]:
                self.can_hold = False

    # ---- 绘制 ----
    def draw(self, screen, camera_y: float):
        pg.draw.rect(screen, (178, 139, 213),
                     (int(self.x), int(self.y - camera_y), 40, 40))
