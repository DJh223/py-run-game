"""弹簧摄像机：正常跳锁死，掉落时弹簧跟随"""

from config import *


class Camera:
    def __init__(self):
        self.y = 0.0
        self.vel_y = 0.0

    def follow(self, player_y: float, player_vy: float, falling: bool, dt: float):
        if falling:
            # 预测落点，空中无死区
            lead = player_vy * 0.15
            target_y = player_y + lead - int(SCREEN_HEIGHT * 0.55)
            current_dead = 0
        else:
            lead = 0
            target_y = player_y - int(SCREEN_HEIGHT * 0.63)
            current_dead = DEAD_ZONE

        if abs(player_y + lead - self.y) <= current_dead:
            target_y = self.y
        else:
            stiffness_use = STIFFNESS * 3 if falling else STIFFNESS
            force = (target_y - self.y) * stiffness_use - self.vel_y * DAMPING
            self.vel_y += force * dt
            self.y += self.vel_y * dt
