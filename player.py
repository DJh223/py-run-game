"""玩家：物理、跳跃、碰撞"""

import pygame as pg
from config import *
from data import Data


class Player:
    def __init__(self, x=PLAYER_START_X, y=PLAYER_START_Y):
        self.x = float(x)
        self.y = float(y)
        self.vy = 0.0
        self.rect = pg.Rect(int(self.x), int(self.y), PLAYER_SIZE, PLAYER_SIZE)
        self.old_bottom = self.rect.bottom

        self.g_current = float(GRAVITY_NORMAL)
        self.on_ground = True
        self.can_hold = True
        self.hold_time = 0.0
        self.hold_triggered = False

        self.has_gravity = True
        self.has_jump = True
        self.has_bigjump = True

    def apply_gravity(self, dt: float):
        """空中累加重力；长按触发后重力渐变降低"""
        if not self.has_gravity or self.on_ground:
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
        """更新 y 位置，穿越法检测落地。返回 (on_ground, collision_ground)"""
        self.old_bottom = self.rect.bottom
        self.y += self.vy * dt
        self.rect.y = int(self.y)

        self.on_ground = False
        collision_ground = False

        for plat in platforms:
            # 穿越法：本帧脚底从平台表面上方穿到下方 = 落地
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
        self.vy = BASE_JUMP
        self.on_ground = False
        self.can_hold = True
        self.hold_time = 0.0
        self.hold_triggered = False

    def update_long_press(self, keys, dt: float):
        """空中按住空格超过阈值 → 开启轻重力"""
        if not self.on_ground and keys[pg.K_SPACE] and self.can_hold and self.has_bigjump:
            self.hold_time += dt
            if self.hold_time >= HOLD_THRESHOLD and not self.hold_triggered:
                self.hold_triggered = True
        else:
            self.hold_time = 0.0
            self.g_current = float(GRAVITY_NORMAL)
            if not keys[pg.K_SPACE]:
                self.can_hold = False

    def draw(self, screen, camera_y: float, scale):
        """屏幕坐标 = 世界坐标 × scale - 摄像机偏移"""
        pg.draw.rect(screen, (162, 164, 165),
                     (int(self.x) * scale, int(self.y - camera_y) * scale,
                      PLAYER_SIZE * scale, PLAYER_SIZE * scale))
