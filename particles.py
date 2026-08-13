"""粒子系统"""

import pygame as pg
import random
import math
from config import *
from data import Data


class Particle:
    def __init__(self, x, y, vx, vy, life, color, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size

    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    @property
    def alive(self) -> bool:
        return self.life > 0

    @property
    def alpha(self) -> int:
        return max(0, int(255 * self.life / self.max_life))

    def draw(self, screen, camera_y: float, scale):
        size = self.size + 2
        surf = pg.Surface((size * 2, size * 2), pg.SRCALPHA)
        pg.draw.circle(surf, (*self.color, self.alpha), (size, size),
                       int(self.size * (0.3 + 0.7 * (self.life / self.max_life))))
        screen.blit(surf, (int(self.x - size) * scale,
                           int(self.y - size - camera_y) * scale))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, count, x, y, speed_range, angle_range, life_range, color, size_range):
        for _ in range(count):
            angle = random.uniform(*angle_range)
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.uniform(*life_range)
            size = random.randint(*size_range)
            self.particles.append(Particle(x, y, vx, vy, life, color, size))

    def fade_color(self, base_rgb: list, scale: float) -> list:
        r = max(0, int(base_rgb[0] * scale))
        g = max(0, int(base_rgb[1] * scale))
        b = max(0, int(base_rgb[2] * scale))
        return [r, g, b]

    def spawn_friction(self, x, bottom_y, block_width):
        half = block_width / 2
        for _ in range(12):
            offset = random.uniform(-half, half)
            x_pos = x + offset
            if offset < -half / 3:
                self.emit(
                    count=2,
                    x=x_pos, y=bottom_y,
                    speed_range=(10, 40),
                    angle_range=(-math.pi * 37 / 36, -math.pi * 35 / 36),
                    life_range=(0.15, 0.3),
                    color=self.fade_color(WORLD_COLOR, 0.6),
                    size_range=(1, 2)
                )
            elif offset < half / 3:
                self.emit(
                    count=3,
                    x=x_pos, y=bottom_y,
                    speed_range=(35, 80),
                    angle_range=(-math.pi * 35 / 36, -math.pi * 33 / 36),
                    life_range=(0.3, 0.4),
                    color=self.fade_color(WORLD_COLOR, 0.8),
                    size_range=(1, 2)
                )
            else:
                self.emit(
                    count=4,
                    x=x_pos, y=bottom_y,
                    speed_range=(40, 100),
                    angle_range=(-math.pi * 33 / 36, -math.pi * 5 / 6),
                    life_range=(0.3, 0.6),
                    color=self.fade_color(WORLD_COLOR, 1),
                    size_range=(1, 3)
                )

    def spawn_landing(self, x, y):
        self.emit(
            count=10,
            x=x, y=y,
            speed_range=(30, 120),
            angle_range=(0, 2 * math.pi),
            life_range=(0.3, 0.7),
            color=(180, 180, 180),
            size_range=(2, 5)
        )

    def spawn_coin_sparkle(self, x, y):
        self.emit(
            count=6,
            x=x, y=y,
            speed_range=(60, 150),
            angle_range=(-0.5 - math.pi / 2, 0.5 - math.pi / 2),
            life_range=(0.2, 0.5),
            color=(255, 215, 0),
            size_range=(2, 4)
        )

    def update(self, dt: float):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, screen, camera_y: float, scale):
        for p in self.particles:
            p.draw(screen, camera_y, scale)
