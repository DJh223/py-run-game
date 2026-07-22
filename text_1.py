import pygame as pg
import random
import ctypes



pg.init()


#锁定输入法
try:
    ctypes.windll.imm32.ImmDisableIME(-1)
except Exception:
    pass   # 非 Windows 系统忽略


screen = pg.display.set_mode((800,400))
clock  = pg.time.Clock()



dtime = 0                                               #总时间



running = True                                          #运行



on_ground = True                                        #是否在地面 
player_y = 310.0                                        #角色的 y 坐标
player_x = 200.0                                        #角色的 x 坐标
player_vy = 0                                           #垂直速度
g_current = 1500                                        #当前实际重力，初始等于正常值
g_normal = 1500                                         #重力加速度
g_min = 600                                             #长按最低降到这个值
g_fade = 3000                                           #每秒重力减少 3000
base_jump = -600                                        #跳跃力度
hold_triggered = False                                  #这一跳是否已经触发过长按
hold_threshold = 0.08                                   #按住0.08秒后才触发长按
hold_time   = 0                                         #当前已按住多少秒
can_hold = True                                         #跳跃跳是否还允许长按



pit_p = 0.2                                             #小坑概率
pit_P = 0.03                                            #大坑概率
pit_w = (80,150)                                        #小坑范围
pit_W = (300,480)                                       #大坑范围
series_ground = True                                    #防连续坑的标记



platforms = []                                          #平台列表
series_float = True                                     #防连续出现平台的标记
scroll_speed = 200                                      #当前滚动速度，会渐变
speed_normal = 200                                      #松手后平台的默认滚动速度
speed_min = 80                                          #A按到底的最低速度
speed_max = 400                                         #D按到底的最高速度
speed_change = 200                                      #每秒速度变化量（控制渐变快慢）
speed_penalty = 0.0                                     # 减速惩罚剩余时间
speed_obs = 60                                          #减速惩罚速度

move_A = False                                          #A键是否按住
move_D = False                                          #D键是否按住



distance = 0                                            #移动距离
pixel_score = 10                                        #每跑 100 像素得 1 分
score = 0                                               #得分



coins = []                                              #存所有金币
find_coin = False                                       #是否生成金币



camera_y = 0.0                                          #摄像机坐标
cam_vel_y = 0.0                                         #相机自身竖直速度
stiffness = 4                                           # 刚度
damping = 5                                             # 阻尼
dead_zone = 250                                         # 死区（玩家在范围内不拉动相机）



falling_timer = 0                                       # 累计掉落时间
fall_duration = 0.3                                     # 掉多久才生成新层（秒）
ground_y = 350                                          # 当前地面层 y 坐标


obstacles = []                                          # 障碍物列表

falling = False                                         #是否掉落

collision_ground = True                                 #是否与地面有支撑





player_rect = pg.Rect(int(player_x), int(player_y), 40, 40) #方块的初始位置



font = pg.font.Font(None,36)                            #字体






#初始生成几个平台铺满地面
for i in range (10):
    x = i * 100
    rect = pg.Rect(x, ground_y, 100, 20) 
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

        if player_vy > 900:
            player_vy = 900

    #平台速度控制
    # 受到减速惩罚时，强制慢速
    if speed_penalty > 0:
        speed_penalty -= dt
        scroll_speed = speed_obs
    else:
        #正常控制速度
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
    ground_plat = [p for p in platforms if p.y == ground_y]
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
        
        newplat = pg.Rect(newx, ground_y, 100, 20)
        platforms.append(newplat)


        # 25% 概率在平台上放一个金币
        if random.random() < 0.40 and series_ground and not find_coin:
            coin_x = newx + random.randint(10, 80)
            coin_y = random.choice([ground_y - 20, ground_y - 100])
            coins.append(pg.Rect(coin_x, coin_y, 12, 12))
            find_coin = True
        else:
            find_coin = False


        #生成浮空平台
        if random.random() < 0.05 and series_ground and series_float:
            float_y = ground_y - 140
            float_x = newx + random.randint(20,60)
            new_float = pg.Rect(float_x, float_y, random.choice([300,600]), 20)
            platforms.append(new_float)
            series_float = False
        else:
            series_float = True


        # 15% 概率在平台上放一个障碍物
        if random.random() < 0.1 and series_ground and not find_coin:
            obs_x = newx + random.randint(30,70)
            obs_y = ground_y - 30
            obstacles.append(pg.Rect(obs_x, obs_y, 15, 30))
            #在障碍物上方有概率生成金币
            if random.random() < 0.5:
                coins.append(pg.Rect(obs_x, ground_y - 100, 12, 12))
                find_coin = True




    #金币随平台滚动
    for coin in coins:
        coin.x -= scroll_speed * dt

    # 移出屏幕的金币删掉
    coins = [c for c in coins if c.right > 0]

    #拾取金币
    for coin in coins[:]:      # [:] 拷贝遍历，允许原地删除
        if player_rect.colliderect(coin):
            coins.remove(coin)
            distance += 500


    #障碍物移动
    for obstacle in obstacles:
        obstacle.x -= scroll_speed * dt 

    #障碍物清除
    obstacles = [o for o in obstacles if o.right > 0]

    #障碍物碰撞
    for obstacle in obstacles[:]:
        if player_rect.colliderect(obstacle):
            obstacles.remove(obstacle)
            distance -= 500
            speed_penalty = 0.5
            if distance < 0:
                distance = 0
                


    #位置
    old_bottom = player_rect.bottom

    player_y += player_vy * dt
    player_rect.y = int(player_y)

    #碰撞检测
    on_ground = False
    for plat in platforms:
        if old_bottom <= plat.top and player_rect.bottom >= plat.top and player_vy >= 0 and player_rect.right > plat.left and player_rect.left < plat.right:
            player_vy = 0
            player_rect.bottom = plat.top
            player_y = player_rect.y
            on_ground = True
            collision_ground = True
            break
        else:
            collision_ground = False


    #检测是否在向下坠落
    if player_y >= ground_y and not collision_ground:
        falling = True
    else:
        falling = False



    #生成下层平台
    if not on_ground and player_vy > 0 and player_y > ground_y:      # 在空中下落
        falling_timer += dt
    else:
        falling_timer = 0                    # 在平台上就归零

    # 到了时限，在脚下生成新地面
    if falling_timer > fall_duration and player_y > ground_y:
        ground_y = int(player_y + 300)
        obstacles.clear()     # ← 清障碍物
        coins.clear()         # ← 清金币

        for i in range(12):
            platforms.append(pg.Rect(int(player_x) - 400 + i * 100, ground_y, 100, 20))
        falling_timer = 0

    

    # 摄像机跟随
    if falling:
        lead = player_vy * 0.15          # 提前 0.15 秒预测落点
        target_y = player_y + lead - 250
        current_dead = 0                  # 空中无死区，即刻跟
    else:
        lead = 0
        target_y = player_y - 250
        current_dead = dead_zone

    if abs(player_y + lead - camera_y) <= current_dead:
        target_y = camera_y
    else:
        thl = (target_y - camera_y) * (stiffness * 3 if falling else stiffness) - cam_vel_y * damping
        cam_vel_y += thl * dt
        camera_y += cam_vel_y * dt


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
        


    #分数
    distance += scroll_speed * dt
    score = int(distance / pixel_score)

    

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

    #摄像机移动
    #玩家
    pg.draw.rect(screen,(178,139,213),(int(player_x),int(player_y - camera_y),40,40))
    #平台
    for plat in platforms:
        pg.draw.rect(screen, (0, 0, 0), (plat.x, plat.y - camera_y, plat.width, plat.height))

    #金币
    for coin in coins:
        pg.draw.rect(screen, (255, 215, 0), (coin.x, coin.y - camera_y, coin.width, coin.height))

    #分数
    figure = font.render(str(score),True,(255, 223, 127))
    screen.blit(figure,(screen.get_width() - figure.get_width() - 10,10))

    #障碍物
    for obstacle in obstacles:
        pg.draw.rect(screen,(100, 100, 100),(obstacle.x, obstacle.y - camera_y, obstacle.width, obstacle.height))


    pg.display.flip()

pg.quit()