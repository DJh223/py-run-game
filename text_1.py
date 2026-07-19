import pygame as pg



pg.init()
screen = pg.display.set_mode((800,400))
clock  = pg.time.Clock()

dtime = 0

running = True
on_ground = True

player_y = 310.0                                        #浮点坐标
player_rect = pg.Rect(200, int(player_y), 40, 40)       #角色的 y 坐标
player_vy = 0                                           #垂直速度
g_current = 1500                                        #当前实际重力，初始等于正常值
g_normal = 1500                                         #重力加速度
g_min = 600                                             #长按最低降到这个值
g_fade = 3000                                           #每秒重力减少 3000
hold_threshold = 0.08                                   #过了这个时间才减重力
base_jump = -550                                        #跳跃力度
hold_triggered = False                                  #这一跳是否已经触发过长按
hold_threshold = 0.08                                   #按住0.08秒后才触发长按
hold_time   = 0                                         #当前已按住多少秒
platforms = []                                          #平台列表
can_hold = True                                         #跳跃跳是否还允许长按


#初始生成几个平台铺满地面
for i in range (10):
    x = i * 100
    rect = pg.Rect(x,350, 100,20) 
    platforms.append(rect)

while running:
    #时间
    dt = clock.tick(120) / 1000
    dtime += dt

    #重力
    if not on_ground:
    # 长按轻重力
        if hold_triggered:
            g_current -= g_fade * dt
            if g_current < g_min:
                g_current = g_min
        else:
            g_current = g_normal

        player_vy += g_current * dt



    #位置
    old_bottom = player_rect.bottom

    player_y += player_vy * dt
    player_rect.y = int(player_y)

    on_ground = False
    for plat in platforms:
        if old_bottom <= plat.top and player_rect.bottom >= plat.top and player_vy >= 0:
            player_vy = 0
            player_rect.bottom = plat.top
            player_y = player_rect.y
            on_ground = True
            break
        



    #跳跃
    #长按
    keys = pg.key.get_pressed()
    if not on_ground and keys[pg.K_SPACE] and can_hold:
        hold_time += dt
        if hold_time >= hold_threshold and not hold_triggered:
            hold_triggered = True

    else:
        hold_time = 0
        g_current = g_normal
        if not keys[pg.K_SPACE]:
            can_hold = False
        





    #ESC 退出
    for event in pg.event.get():
        # 系统级：退出、暂停等
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

        # 游戏级：跳跃等
            elif event.key == pg.K_SPACE and on_ground:
                player_vy = base_jump
                on_ground = False
                can_hold  = True
                hold_time  = 0
                hold_triggered = False

    #绘制
    screen.fill((0,0,0))
    pg.draw.rect(screen, (255, 255, 255), (200, int(player_rect.y), 40, 40))
    for plat in platforms:
        pg.draw.rect(screen, (100, 100, 100), plat) 


    pg.display.flip()

pg.quit()