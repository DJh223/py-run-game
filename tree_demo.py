import time
import pygame



score = 0
v = 100 
offset = 0                     # 控制所有竖线左右移动
lines = 70                     # 竖线之间的像素间隔
background_Y = 120
background_hight = 80



speed = 180

pygame.init()
ziti = pygame.font.Font(None, 36) 
screen = pygame.display.set_mode((800,300))
clock = pygame.time.Clock()
running = True

#树
def draw_tree(screen, x, top_y, bottom_y):
    tree_h = bottom_y - top_y
    #树干
    trunk = bottom_y - (tree_h * 0.25)
    pygame.draw.line(screen,(101, 67, 33),(x,trunk),(x,bottom_y),6)    #树干

    #树叶
    leaf_h = (trunk - top_y) / 3

    leaf_w = [22,17,12] 
    for i in range(3):
        leaf_bot = trunk - leaf_h * i
        leaf_top = trunk - leaf_h * (i+1)
        leaf_xl   = x - leaf_w[i]
        leaf_xr   = x + leaf_w[i]
        pygame.draw.polygon(screen,(34, 139, 34),[(x,leaf_top),(leaf_xl,leaf_bot),(leaf_xr,leaf_bot)])

dtime = 0
while running:
    dt = clock.tick(120) / 1000
    dtime += dt
    score = int(dtime * v)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.QUIT:
            running = False
    
    # === 更新矩形位置 ===


    offset -= speed * dt
    offset = round(offset, 1)
    if offset < -lines:
        offset += lines

    # === 绘制 ===
    screen.fill((255,255,255))

    pygame.draw.polygon(screen,(100,100,100),[(380,150),(420,150),(420,190),(380,190)])

    # 背景矩形
    x = offset
    while x<800:
        draw_tree(screen,x,20,background_Y)
        x += lines

    #分数
    figure = ziti.render(str(score),True,(255, 223, 127))
    screen.blit(figure,(screen.get_width() - figure.get_width() - 10,10))

    pygame.display.flip()
    

pygame.quit()











