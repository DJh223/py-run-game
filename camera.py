"""弹簧摄像机：正常跳锁死，掉落时弹簧跟随"""

from config import *


class Camera:
    def __init__(self):
        self.y = 0.0                                        # 摄像机 y 偏移
        self.vel_y = 0.0                                    # 摄像机自身垂直速度

    def follow(self, player_y: float, player_vy: float, falling: bool, dt: float):
        """根据 falling 状态决定跟随强度，弹簧力驱动摄像机"""
        if falling:
            lead = player_vy * 0.15                         # 预测 0.15 秒后的落点
            target_y = player_y + lead - 250                # 目标：把玩家放在屏幕 y=250
            current_dead = 0                                # 空中无死区
        else:
            lead = 0
            target_y = player_y - 250
            current_dead = DEAD_ZONE                        # 站地时小跳不跟

        if abs(player_y + lead - self.y) <= current_dead:
            target_y = self.y                               # 死区内锁住
        else:
            stiffness_use = STIFFNESS * 3 if falling else STIFFNESS
            force = (target_y - self.y) * stiffness_use - self.vel_y * DAMPING
            self.vel_y += force * dt
            self.y += self.vel_y * dt
