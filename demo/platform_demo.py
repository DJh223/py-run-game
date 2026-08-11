"""平台纹理 Demo — 代码编辑器风格（缩进线 + 括号 + 行号）"""

import pygame as pg

pg.init()
W, H = 800, 400
screen = pg.display.set_mode((W, H))
pg.display.set_caption("平台纹理 Demo — ESC 退出")
clock = pg.time.Clock()

# 背景
bg = pg.Surface((W, H))
bg.fill((63, 63, 63))
grid = pg.Surface((W, H), pg.SRCALPHA)
for x in range(0, W, 80):
    pg.draw.line(grid, (80, 80, 80), (x, 0), (x, H), 1)
for y in range(0, H, 80):
    pg.draw.line(grid, (80, 80, 80), (0, y), (W, y), 1)
for x in range(0, W, 8):
    pg.draw.line(grid, (80, 80, 80, 30), (x, 0), (x, H), 1)
for y in range(0, H, 8):
    pg.draw.line(grid, (80, 80, 80, 30), (0, y), (W, y), 1)

font = pg.font.Font(None, 18)

running = True
frame = 0

while running:
    dt = clock.tick(120) / 1000
    frame += 1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    screen.blit(bg, (0, 0))
    screen.blit(grid, (0, 0))

    # ---- 方案 A：代码缩进线 ----
    py = 100
    plat = pg.Rect(100, py, 120, 20)
    pg.draw.rect(screen, (75, 78, 82), plat)                    # 平台底色
    pg.draw.line(screen, (110, 160, 120), (plat.left, py),      # 顶面亮线
                 (plat.right, py), 2)
    # 缩进竖线
    for dx in range(20, plat.width, 20):
        pg.draw.line(screen, (60, 65, 70),
                     (plat.left + dx, py + 2),
                     (plat.left + dx, py + 18), 1)
    label_a = font.render("A: 缩进线", True, (140, 145, 150))
    screen.blit(label_a, (plat.right + 12, py))

    # ---- 方案 B：括号边缘 ----
    py = 160
    plat = pg.Rect(100, py, 120, 20)
    pg.draw.rect(screen, (75, 78, 82), plat)
    pg.draw.line(screen, (110, 160, 120), (plat.left, py),
                 (plat.right, py), 2)
    # 左括号
    pg.draw.line(screen, (180, 180, 100), (plat.left + 2, py + 2),
                 (plat.left + 6, py + 10), 1)
    pg.draw.line(screen, (180, 180, 100), (plat.left + 2, py + 18),
                 (plat.left + 6, py + 10), 1)
    # 右括号
    pg.draw.line(screen, (180, 180, 100), (plat.right - 2, py + 2),
                 (plat.right - 6, py + 10), 1)
    pg.draw.line(screen, (180, 180, 100), (plat.right - 2, py + 18),
                 (plat.right - 6, py + 10), 1)
    label_b = font.render("B: 括号边缘", True, (140, 145, 150))
    screen.blit(label_b, (plat.right + 12, py))

    # ---- 方案 C：行号 ----
    py = 220
    plat = pg.Rect(100, py, 120, 20)
    pg.draw.rect(screen, (75, 78, 82), plat)
    pg.draw.line(screen, (110, 160, 120), (plat.left, py),
                 (plat.right, py), 2)
    # 行号
    for i, dx in enumerate(range(5, plat.width, 20)):
        num = font.render(str(i + 1), True, (55, 60, 65))
        screen.blit(num, (plat.left + dx, py + 3))
    label_c = font.render("C: 行号", True, (140, 145, 150))
    screen.blit(label_c, (plat.right + 12, py))

    # ---- 方案 D：混合（缩进 + 行号 + 括号） ----
    py = 280
    plat = pg.Rect(100, py, 180, 20)
    pg.draw.rect(screen, (75, 78, 82), plat)
    pg.draw.line(screen, (110, 160, 120), (plat.left, py),
                 (plat.right, py), 2)
    # 左括号
    pg.draw.line(screen, (180, 180, 100, 120), (plat.left + 2, py + 2),
                 (plat.left + 7, py + 10), 1)
    pg.draw.line(screen, (180, 180, 100, 120), (plat.left + 2, py + 18),
                 (plat.left + 7, py + 10), 1)
    # 缩进线
    for dx in range(20, plat.width, 10):
        pg.draw.line(screen, (60, 65, 70, 80),
                     (plat.left + dx, py + 2),
                     (plat.left + dx, py + 18), 1)
    # 行号
    for i, dx in enumerate(range(15, plat.width, 25)):
        num = font.render(str(i + 12), True, (50, 55, 60))
        screen.blit(num, (plat.left + dx, py + 3))
    label_d = font.render("D: 混合", True, (160, 200, 130))
    screen.blit(label_d, (plat.right + 12, py))

    # 方块
    pg.draw.rect(screen, (162, 164, 165), (350, py + 10, 30, 30), 2)

    # 顶部说明
    title = font.render("平台纹理方案 (灰色区域 = 平台)", True, (160, 160, 160))
    screen.blit(title, (15, 15))

    pg.display.flip()

pg.quit()
