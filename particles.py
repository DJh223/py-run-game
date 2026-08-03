"""粒子系统"""

import pygame as pg
import random
import math



class Particle:
    def __init__(self, x, y, vx, vy, life, color, size):
        self.x = x              # 世界坐标 x
        self.y = y              # 世界坐标 y
        self.vx = vx            # 水平速度（像素/秒）
        self.vy = vy            # 垂直速度（像素/秒）
        self.life = life        # 剩余生命（秒）
        self.max_life = life    # 总生命（用于计算透明度）
        self.color = color      # RGB 颜色元组
        self.size = size        # 半径（像素）

    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt


    @property
    def alive(self) -> bool:
        """判断是否死亡"""
        return self.life > 0

    @property
    def alpha(self) -> int:
        """透明度"""
        return max(0, int(255 * self.life / self.max_life))

    def draw(self, screen, camera_y: float):
        size = self.size + 2
        surf = pg.Surface((size * 2,size * 2),pg.SRCALPHA)
        pg.draw.circle(surf, (*self.color, self.alpha), (size,size),
                        int(self.size * (0.3 + 0.7 * (self.life / self.max_life))))
        screen.blit(surf, (int(self.x - size), int(self.y - size - camera_y)))


class ParticleSystem :
    def __init__(self):
        self.particles = []                                 # 存所有活着的粒子

    def emit(self, count, x, y, speed_range, angle_range, life_range, color, size_range):
        for _ in range(count):
            angle = random.uniform(*angle_range)      # 2. 随机一个角度
            speed = random.uniform(*speed_range)      # 3. 随机一个速度
            vx = math.cos(angle) * speed              # 4. 三角算出水平分速度
            vy = math.sin(angle) * speed              # 5. 三角算出垂直分速度
            life = random.uniform(*life_range)        # 6. 随机一个生命值
            size = random.randint(*size_range)        # 7. 随机一个大小
            self.particles.append(                    # 8. 造一个粒子放进列表
                Particle(x, y, vx, vy, life, color, size)
            )

    def spawn_friction(self, x, bottom_y, block_width = 40):
        '''地面摩擦粒子特效'''
        half = block_width // 2 
        for _ in range(12):
            offset = random.uniform(-half, half)
            x_pos = x + offset
            if offset < -12:
                self.emit(
                    count = 2,
                    x = x_pos,
                    y = bottom_y,
                    speed_range = (10,40),
                    angle_range = (-math.pi * 37/36, -math.pi * 35/36),
                    life_range=(0.15, 0.3),
                    color=(180, 160, 140),
                    size_range=(1, 2)
                )
            elif offset < 8:
                self.emit(
                    count=3,
                    x=x_pos,
                    y=bottom_y,
                    speed_range=(35, 80),
                    angle_range=(-math.pi * 35/36, -math.pi * 33/36),
                    life_range=(0.3, 0.4),
                    color=(180, 160, 140),
                    size_range=(1, 2)
                )    

            else:
                self.emit(
                    count=4, 
                    x=x_pos, 
                    y=bottom_y,
                    speed_range=(40, 100),
                    angle_range=(-math.pi * 33/36, -math.pi * 5/6),   
                    life_range=(0.3, 0.6),
                    color=(180, 160, 140),
                    size_range=(1, 3)
                )

        

    def spawn_landing(self, x, y):
        """落地爆发粒子特效"""
        self.emit(
            count=10,
            x=x, y=y,
            speed_range=(30, 120),
            angle_range=(0, 2 * math.pi),      # 所有方向
            life_range=(0.3, 0.7),
            color=(180, 180, 180),             # 灰白灰尘
            size_range=(2, 5)
        )

    def spawn_coin_sparkle(self, x, y):
        """金币粒子特效"""
        self.emit(
            count=6,
            x=x, y=y,
            speed_range=(60, 150),
            angle_range=(-0.5 - math.pi/2, 0.5 - math.pi/2),   # 大致向上
            life_range=(0.2, 0.5),
            color=(255, 215, 0),             # 金色
            size_range=(2, 4)
        )

    def update(self, dt: float):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, screen, camera_y: float):
        for p in self.particles:
            p.draw(screen,camera_y)