"""背景风格 Demo — 视口渐变 + 终端元素 + 建模软件网格线"""

import pygame as pg

pg.init()
W, H = 800, 400
screen = pg.display.set_mode((W, H))
pg.display.set_caption("背景风格 Demo — ESC 退出")
clock = pg.time.Clock()
font_small = pg.font.Font(None, 20)
font_big = pg.font.Font(None, 36)

# ---- 预渲染：纯色背景 + 网格线 ----
bg_surf = pg.Surface((W, H))
bg_surf.fill((63, 63, 63))            # #636363

grid_surf = pg.Surface((W, H), pg.SRCALPHA)
# 细网格（4px间距，几乎看不见）
for gx in range(0, W, 4):
    pg.draw.line(grid_surf, (80, 80, 80, 40), (gx, 0), (gx, H), 1)
for gy in range(0, H, 4):
    pg.draw.line(grid_surf, (80, 80, 80, 40), (0, gy), (W, gy), 1)
for gx in range(0, W, 40):
    pg.draw.line(grid_surf, (80, 80, 80), (gx, 0), (gx, H), 1)   # #808080
for gy in range(0, H, 40):
    pg.draw.line(grid_surf, (80, 80, 80), (0, gy), (W, gy), 1)
    # 细网格线（10px，半透明）



# ---- 预渲染：顶部状态栏 ----
bar_surf = pg.Surface((W, 30), pg.SRCALPHA)
pg.draw.rect(bar_surf, (25, 28, 35, 200), (0, 0, W, 30))

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

    # ---- 绘制 ----
    screen.blit(bg_surf, (0, 0))

    # 网格线（极淡）
    screen.blit(grid_surf, (0, 0))

    # 顶部状态栏
    screen.blit(bar_surf, (0, 0))

    # 左侧提示符
    txt1 = font_small.render("$> process_runner.exe --mode=escape", True, (80, 200, 120))
    txt2 = font_small.render("   PID: 8472  |  STATUS: RUNNING  |  ERR: 0x3F2A", True, (60, 150, 90))
    txt3 = font_small.render("   WARNING: system integrity compromised", True, (180, 140, 60))
    screen.blit(txt1, (12, 38))
    screen.blit(txt2, (12, 58))
    screen.blit(txt3, (12, 78))

    # 右侧面板边框
    pg.draw.rect(screen, (50, 55, 65), (W - 160, 45, 145, 120), 1)
    title = font_small.render("PROPERTIES", True, (100, 110, 120))
    screen.blit(title, (W - 155, 50))
    prop_lines = [
        "X: 200.0  Y: 310.0",
        "VX: 200  VY: 0",
        "GRAVITY: 1500",
        "MODE: ESCAPE",
    ]
    for i, line in enumerate(prop_lines):
        t = font_small.render(line, True, (80, 200, 120))
        screen.blit(t, (W - 150, 72 + i * 18))

    # 右下角闪烁光标
    if (frame // 40) % 2 == 0:        # 每 40 帧切换一次
        cursor = font_small.render("_", True, (80, 200, 120))
        screen.blit(cursor, (W - 25, H - 25))

    # 地面粗线（地平线，在 y=350）
    pg.draw.line(screen, (60, 65, 75), (0, 350), (W, 350), 2)

    # 演示平台
    demo_platforms = [
        (50, 350, 120, 16),
        (220, 350, 100, 16),
        (360, 350, 80, 16),
        (500, 350, 200, 16),
    ]
    for px, py, pw, ph in demo_platforms:
        pg.draw.rect(screen, (40, 45, 55), (px, py, pw, ph))
        pg.draw.line(screen, (70, 80, 95), (px, py), (px + pw, py), 1)

    # 演示方块
    pg.draw.rect(screen, (80, 200, 120), (200, 310, 40, 40), 3)

    # 辅助说明文字
    hint = font_big.render("视口背景 + 终端信息 + 网格线 + 平台", True, (180, 180, 180))
    screen.blit(hint, (W // 2 - hint.get_width() // 2, H - 40))

    pg.display.flip()

pg.quit()
