"""弹簧摄像机：正常跳锁死，掉落时弹簧跟随"""

from config import *


class Camera:
    def __init__(self):
        self.y = 0.0
        self.vel_y = 0.0

    def follow(self, player_y: float, player_vy: float, falling: bool, dt: float):
        if falling:
            lead = player_vy * 0.15
            target_y = player_y + lead - 250
            current_dead = 0           # 空中无死区
        else:
            lead = 0
            target_y = player_y - 250
            current_dead = DEAD_ZONE

        if abs(player_y + lead - self.y) <= current_dead:
            target_y = self.y          # 死区内锁住
        else:
            stiffness_use = STIFFNESS * 3 if falling else STIFFNESS
            force = (target_y - self.y) * stiffness_use - self.vel_y * DAMPING
            self.vel_y += force * dt
            self.y += self.vel_y * dt
