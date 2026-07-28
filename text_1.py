"""跑酷肉鸽游戏 — 主入口"""

import pygame as pg
import ctypes

from config import *
from player import Player
from camera import Camera
from world import World


# ============================================================
# 初始化
# ============================================================
pg.init()

# 锁定中文输入法，防止字母键被拦截
try:
    ctypes.windll.imm32.ImmDisableIME(-1)
except Exception:
    pass

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
font = pg.font.Font(None, 36)                              # 分数字体

player = Player()
camera = Camera()
world = World()

dtime = 0.0                                                 # 总运行时间
distance = 0.0                                              # 累计移动距离
move_A = False                                              # A 键是否按住
move_D = False                                              # D 键是否按住

running = True                                              # 主循环开关

# ============================================================
# 主循环
# ============================================================
while running:
    dt = clock.tick(120) / 1000
    dtime += dt

    # ---- 更新 ----
    player.apply_gravity(dt)
    world.update_speed(move_A, move_D, dt)
    world.scroll_all(dt)
    world.generate_ground(screen.get_width())

    player.update_and_land(world.platforms, dt)
    falling, _ = world.update_falling(
        player.y, player.vy, player.on_ground, dt, player.x)

    keys = pg.key.get_pressed()
    player.update_long_press(keys, dt)
    camera.follow(player.y, player.vy, falling, dt)

    add_d, sub_d = world.check_collectibles(player.rect)
    distance += add_d - sub_d
    if distance < 0:
        distance = 0
    distance += world.scroll_speed * dt
    score = int(distance / PIXEL_PER_SCORE)

    # ---- 事件 ----
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_SPACE and player.on_ground:
                player.jump()
            elif event.key == pg.K_a:
                move_A = True
            elif event.key == pg.K_d:
                move_D = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                move_A = False
            elif event.key == pg.K_d:
                move_D = False

    # ---- 绘制 ----
    screen.fill((255, 255, 255))

    player.draw(screen, camera.y)
    world.draw(screen, camera.y)

    # 分数（右上角）
    figure = font.render(str(score), True, (255, 223, 127))
    screen.blit(figure, (screen.get_width() - figure.get_width() - 10, 10))

    pg.display.flip()

pg.quit()
