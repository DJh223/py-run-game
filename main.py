"""跑酷肉鸽游戏 — 主入口"""

import pygame as pg
import ctypes
import win32gui
import win32con

from config import *
from player import Player
from camera import Camera
from world import World
from particles import ParticleSystem
from background import Background
from game_ui import Game_ui
from data import Data

pg.init()

try:
    ctypes.windll.imm32.ImmDisableIME(-1)
except Exception:
    pass

info = pg.display.Info()
native_w, native_h = info.current_w, info.current_h

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
font = pg.font.Font("C:/Windows/Fonts/msyh.ttc", 14)

player = Player()
camera = Camera()
world = World()
particles = ParticleSystem()
bg = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
gu = Game_ui(world, player)

was_grounded = True
dust_timer = 0.0
dtime = 0.0
distance = 0.0
move_A = False
move_D = False

running = True

scale = SCREEN_HEIGHT / SCREEN_HEIGHT

while running:
    dt = clock.tick(120) / 1000
    dtime += dt

    player.apply_gravity(dt)
    world.update_speed(move_A, move_D, dt)
    world.scroll_all(dt)
    world.generate_ground(screen.get_width())
    was_grounded = player.on_ground

    player.update_and_land(world.platforms, dt)

    if player.on_ground and not was_grounded:
        particles.spawn_landing(player.rect.centerx, player.rect.bottom)

    if player.on_ground:
        dust_timer += dt
        if dust_timer > 0.06:
            particles.spawn_friction(player.rect.centerx, player.rect.bottom, PLAYER_SIZE)
            dust_timer = 0.0
    else:
        dust_timer = 0

    falling, _ = world.update_falling(
        player.y, player.vy, player.on_ground, dt, player.x)

    keys = pg.key.get_pressed()
    player.update_long_press(keys, dt)
    camera.follow(player.y, player.vy, falling, dt)

    particles.update(dt)

    add_d, sub_d = world.check_collectibles(player.rect)
    if add_d > 0:
        particles.spawn_coin_sparkle(player.rect.centerx, player.y)

    distance += add_d - sub_d
    if distance < 0:
        distance = 0
    distance += world.scroll_speed * dt
    score = int(distance / PIXEL_PER_SCORE)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_SPACE and player.on_ground and player.has_jump:
                player.jump()
            elif event.key == pg.K_a:
                move_A = True
            elif event.key == pg.K_d:
                move_D = True
            elif event.key == pg.K_F11:
                if screen.get_flags() & pg.NOFRAME:
                    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    hwnd = pg.display.get_wm_info()["window"]
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP,
                                          (native_w - SCREEN_WIDTH) // 2,
                                          (native_h - SCREEN_HEIGHT) // 2,
                                          0, 0, win32con.SWP_NOSIZE)
                    bg.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
                else:
                    screen = pg.display.set_mode((native_w, native_h), pg.NOFRAME)
                    hwnd = pg.display.get_wm_info()["window"]
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0,
                                          native_w, native_h, 0)
                    bg.resize(native_w, native_h)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                move_A = False
            elif event.key == pg.K_d:
                move_D = False

    screen_w, screen_h = screen.get_size()
    scale = screen_h / SCREEN_HEIGHT

    bg.draw(screen, world.total_scroll)

    player.draw(screen, camera.y, scale)
    world.draw(screen, camera.y, scale)
    particles.draw(screen, camera.y, scale)
    gu.draw(screen)
    gu.title(screen, font)

    figure = font.render(str(score), True, (255, 255, 255))
    screen.blit(figure, (screen.get_width() - figure.get_width() - 10, 10))

    pg.display.flip()

pg.quit()
