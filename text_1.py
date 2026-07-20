import pygame as pg
import random
import ctypes



pg.init()
try:
    ctypes.windll.imm32.ImmDisableIME(-1)
except Exception:
    pass   # 非 Windows 系统忽略
screen = pg.display.set_mode((800,400))
clock  = pg.time.Clock()



dtime = 0                                               #帧时间



running = True                                          #运行



on_ground = True                                        #是否在地面 
player_y = 310.0                                        #角色的 y 坐标
player_x = 200.0                                        #角色的 x 坐标
player_vy = 0                                           #垂直速度
g_current = 1500                                        #当前实际重力，初始等于正常值
g_normal = 1500                                         #重力加速度
g_min = 600                                             #长按最低降到这个值
g_fade = 3000                                           #每秒重力减少 3000
base_jump = -550                                        #跳跃力度
hold_triggered = False                                  #这一跳是否已经触发过长按
hold_threshold = 0.08                                   #按住0.08秒后才触发长按
hold_time   = 0                                         #当前已按住多少秒
can_hold = True                                         #跳跃跳是否还允许长按



pit_p = 0.2                                             #小坑概率
pit_P = 0.07                                            #大坑概率
pit_w = (70,120)                                        #小坑范围
pit_W = (140,250)                                       #大坑范围
series_ground = True                                    #防连续坑的标记



platforms = []                                          #平台列表
series_float = True                                     #防连续出现平台的标记
scroll_speed = 200                                      #当前滚动速度，会渐变
speed_normal = 200                                      #松手后平台的默认滚动速度
speed_min = 80                                          #A按到底的最低速度
speed_max = 400                                         #D按到底的最高速度
speed_change = 200                                      #每秒速度变化量（控制渐变快慢）



move_A = False                                         #A键是否按住
move_D = False                                         #D键是否按住


player_rect = pg.Rect(int(player_x), int(player_y), 40, 40) #方块的初始位置

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
    #长按轻重力
        if hold_triggered:
            g_current -= g_fade * dt
            if g_current < g_min:
                g_current = g_min
        else:
            g_current = g_normal

        player_vy += g_current * dt

    #平台速度控制
    if move_A:
        target = speed_min
    elif move_D:
        target = speed_max
    else:
        target = speed_normal

    if scroll_speed < target:
        scroll_speed += speed_change * dt
        if scroll_speed > target:
            scroll_speed = target
    elif scroll_speed > target:
        scroll_speed -= speed_change * dt
        if scroll_speed < target:
            scroll_speed = target


    #平台滚动
    for plat in platforms:
        plat.x -= scroll_speed * dt
    

    #生成新的平台
    platforms = [p for p in platforms if p.right > 0]      #检测平台是否在左边消失
    ground_plat = [p for p in platforms if p.y == 350]
    rightmost = max(p.right for p in ground_plat)
    screen_w = screen.get_width()
    if rightmost < screen_w + 100:
        i = random.random()
        if i < pit_p and series_ground:
            if i < pit_P:
                newx = rightmost + random.randint(*pit_W)   #生成大坑
                series_ground = False
            else:
                newx = rightmost + random.randint(*pit_w)   #生成小坑
                series_ground = False
        else:
            newx = rightmost
            series_ground = True
        
        newplat = pg.Rect(newx, 350, 100, 20)
        platforms.append(newplat)

        #生成浮空平台
        if random.random() < 0.08 and series_ground and series_float:
            float_y = 230
            float_x = newx + random.randint(20,60)
            new_float = pg.Rect(float_x, float_y, 60, 20)
            platforms.append(new_float)
            series_float = False
        else:
            series_float = True



            

    #位置
    old_bottom = player_rect.bottom

    player_y += player_vy * dt
    player_rect.y = int(player_y)

    #穿越检测
    on_ground = False
    for plat in platforms:
        if old_bottom <= plat.top and player_rect.bottom >= plat.top and player_vy >= 0 and player_rect.right > plat.left and player_rect.left < plat.right:
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
        



    print(f"\r A:{keys[pg.K_a]} D:{keys[pg.K_d]} x:{player_rect.x:.0f} scroll:{scroll_speed:.0f}", end="")

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

            elif event.key == pg.K_a:
                move_A = True
            elif event.key == pg.K_d:
                move_D = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a:
                move_A = False
            elif event.key == pg.K_d:
                move_D = False

    #绘制
    screen.fill((255,255,255))
    pg.draw.rect(screen, (178, 139, 213), (int(player_rect.x), int(player_rect.y), 40, 40))
    for plat in platforms:
        pg.draw.rect(screen, (0, 0, 0), plat) 


    pg.display.flip()

pg.quit()