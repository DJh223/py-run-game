"""粒子系统 Demo — 鼠标点击生成粒子，观察粒子的一生"""

import pygame as pg
import random
import math


# ============================================================
# 粒子类
# ============================================================
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
        """每帧移动 + 衰减生命"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    @property
    def alive(self) -> bool:
        return self.life > 0

    @property
    def alpha(self) -> int:
        """根据剩余生命比例返回 0~255 的透明度"""
        return max(0, int(255 * self.life / self.max_life))

    def draw(self, screen):
        # pg.draw.circle 不支持透明度 → 画在独立透明 Surface 上再贴到屏幕
        size = self.size + 2
        surf = pg.Surface((size * 2, size * 2), pg.SRCALPHA)
        pg.draw.circle(surf, (*self.color, self.alpha),
                       (size, size), int(self.size * (0.3 + 0.7 * self.life / self.max_life)))
        screen.blit(surf, (int(self.x - size), int(self.y - size)))


# ============================================================
# 粒子系统
# ============================================================
class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, count, x, y, speed_range, angle_range, life_range, color, size_range):
        """通用发射器"""
        for _ in range(count):
            angle = random.uniform(*angle_range)
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.uniform(*life_range)
            size = random.randint(*size_range)
            self.particles.append(Particle(x, y, vx, vy, life, color, size))

    def burst(self, x, y):
        """圆形爆发 — 所有方向均匀散开"""
        self.emit(20, x, y,
                  speed_range=(80, 250),
                  angle_range=(0, 2 * math.pi),
                  life_range=(0.5, 1.2),
                  color=(255, 180, 50),
                  size_range=(3, 7))

    def fountain(self, x, y):
        """喷泉 — 向上喷出，左右散开，受重力下落"""
        for _ in range(8):
            angle = random.uniform(-0.5, 0.5) - math.pi / 2   # 大致向上
            speed = random.uniform(150, 350)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.uniform(1.0, 2.0)
            size = random.randint(3, 6)
            p = Particle(x, y, vx, vy, life, (100, 180, 255), size)
            p._gravity = 300                                   # 自定义重力
            self.particles.append(p)

    def spark_line(self, x, y):
        """火花线 — 细长粒子朝左右飞"""
        for _ in range(12):
            vx = random.uniform(-200, 200)
            vy = random.uniform(-50, 50)
            life = random.uniform(0.3, 0.6)
            self.particles.append(
                Particle(x, y, vx, vy, life, (255, 255, 200), 2))

    def update(self, dt: float):
        for p in self.particles:
            p.update(dt)
            # 喷泉粒子有自定义重力
            if hasattr(p, '_gravity'):
                p.vy += p._gravity * dt
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)


# ============================================================
# 主程序
# ============================================================
def main():
    pg.init()
    screen = pg.display.set_mode((800, 500))
    pg.display.set_caption("粒子系统 Demo — 左键爆发 | 右键喷泉 | 中键火花 | ESC退出")
    clock = pg.time.Clock()
    font = pg.font.Font(None, 28)

    ps = ParticleSystem()
    running = True

    while running:
        dt = clock.tick(120) / 1000

        # ---- 事件 ----
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if event.button == 1:         # 左键
                    ps.burst(mx, my)
                elif event.button == 3:       # 右键
                    ps.fountain(mx, my)
                elif event.button == 2:       # 中键
                    ps.spark_line(mx, my)

        # ---- 更新 ----
        ps.update(dt)

        # ---- 绘制 ----
        screen.fill((20, 20, 30))

        ps.draw(screen)

        # 提示文字
        txt1 = font.render("左键=爆发  右键=喷泉  中键=火花", True, (180, 180, 180))
        txt2 = font.render(f"粒子数: {len(ps.particles)}", True, (150, 150, 150))
        screen.blit(txt1, (15, 15))
        screen.blit(txt2, (15, 45))

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
