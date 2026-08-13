"""世界管理：平台、金币、障碍物、坑洞、浮空平台、掉落层切换"""

import pygame as pg
import random
from config import *
from data import Data


class World:
    def __init__(self):
        self.platforms = []
        self.coins = []
        self.obstacles = []

        self.ground_y = PLAYER_START_Y + PLAYER_SIZE
        self.scroll_speed = float(SCROLL_SPEED_INIT)
        self.speed_penalty = 0.0

        self.series_ground = True
        self.series_float = True
        self.find_coin = False
        self.falling = False
        self.falling_timer = 0.0

        self._rightmost = 1000
        self.total_scroll = 0.0

        # 初始连续地面
        for i in range(10):
            self.platforms.append(pg.Rect(i * SCROLL_W, self.ground_y, SCROLL_W + 3, SCROLL_H))

    def update_speed(self, move_A: bool, move_D: bool, dt: float):
        """A 减速 / D 加速 / 松手恢复；惩罚期间强制慢速"""
        if self.speed_penalty > 0:
            self.speed_penalty -= dt
            self.scroll_speed = SPEED_OBS
            return

        if move_A:
            target = float(SCROLL_SPEED_MIN)
        elif move_D:
            target = float(SCROLL_SPEED_MAX)
        else:
            target = float(SCROLL_SPEED_NORMAL)

        if self.scroll_speed < target:
            self.scroll_speed += SPEED_CHANGE * dt
            if self.scroll_speed > target:
                self.scroll_speed = target
        elif self.scroll_speed > target:
            self.scroll_speed -= SPEED_CHANGE * dt
            if self.scroll_speed < target:
                self.scroll_speed = target

    def scroll_all(self, dt: float):
        """所有物体向左滚动，移出左边界后删除"""
        for plat in self.platforms:
            plat.x -= self.scroll_speed * dt
        for coin in self.coins:
            coin.x -= self.scroll_speed * dt
        for obs in self.obstacles:
            obs.x -= self.scroll_speed * dt

        self.total_scroll += self.scroll_speed * dt

        self.platforms = [p for p in self.platforms if p.right > 0]
        self.coins = [c for c in self.coins if c.right > 0]
        self.obstacles = [o for o in self.obstacles if o.right > 0]

    def generate_ground(self, screen_w: int):
        """生成地面平台、金币、浮空平台、障碍物"""
        ground_plat = [p for p in self.platforms if p.y == self.ground_y]
        if ground_plat:
            self._rightmost = max(p.right for p in ground_plat)
        else:
            self._rightmost = PLAYER_START_X + 600

        if self._rightmost >= screen_w + 100:
            return

        dice = random.random()
        if dice < PIT_SMALL_PROB and self.series_ground:
            if dice < PIT_LARGE_PROB:
                newx = self._rightmost + random.randint(*PIT_LARGE_RANGE)
            else:
                newx = self._rightmost + random.randint(*PIT_SMALL_RANGE)
            self.series_ground = False
        else:
            newx = self._rightmost
            self.series_ground = True

        newx = int(newx)
        self.platforms.append(pg.Rect(newx - 3, self.ground_y, SCROLL_W, SCROLL_H))

        if random.random() < COIN_PROB and self.series_ground and not self.find_coin:
            coin_x = newx + random.randint(10, 80)
            coin_y = random.choice([self.ground_y - 30, self.ground_y - 120])
            self.coins.append(pg.Rect(coin_x, coin_y, 12, 12))
            self.find_coin = True
        else:
            self.find_coin = False

        if random.random() < FLOAT_PROB and self.series_ground and self.series_float:
            float_y = self.ground_y - 150
            float_x = newx + random.randint(20, 60)
            float_w = random.choice([300, 600])
            self.platforms.append(pg.Rect(float_x, float_y, float_w, SCROLL_H))
            self.series_float = False
        else:
            self.series_float = True

        if random.random() < OBSTACLE_PROB and self.series_ground and not self.find_coin:
            obs_x = newx + random.randint(30, 70)
            obs_y = self.ground_y - OBSTRUCTION_H
            self.obstacles.append(pg.Rect(obs_x, obs_y, OBSTRUCTION_W, OBSTRUCTION_H))
            # 障碍物上方有概率放金币作为跳过奖励
            if random.random() < COIN_ABOVE_OBS_PROB:
                self.coins.append(pg.Rect(obs_x, self.ground_y - 120, 12, 12))
                self.find_coin = True

    def check_collectibles(self, player_rect) -> tuple[int, int]:
        """检测金币/障碍物碰撞。返回 (加距离, 减距离)"""
        add_dist = 0
        sub_dist = 0

        for coin in self.coins[:]:
            if player_rect.colliderect(coin):
                self.coins.remove(coin)
                add_dist += COIN_SCORE

        for obs in self.obstacles[:]:
            if player_rect.colliderect(obs):
                self.obstacles.remove(obs)
                sub_dist += OBSTACLE_PENALTY
                self.speed_penalty = SPEED_PENALTY_DURATION

        return add_dist, sub_dist

    def update_falling(self, player_y: float, player_vy: float,
                       on_ground: bool, dt: float, player_x: float):
        """坠落检测 + 生成下层平台。返回 (falling, 是否生成了新层)"""
        self.falling = player_y >= self.ground_y and not on_ground

        if not on_ground and player_vy > 0 and player_y > self.ground_y:
            self.falling_timer += dt
        else:
            self.falling_timer = 0

        new_layer = False
        if self.falling_timer > FALL_DURATION and player_y > self.ground_y:
            # 掉出当前层 → 脚下生成新一层（掉落不死）
            self.ground_y = int(player_y + SCREEN_HEIGHT)
            self.obstacles.clear()
            self.coins.clear()
            for i in range(12):
                self.platforms.append(
                    pg.Rect(int(player_x) - 400 + i * SCROLL_W, self.ground_y, SCROLL_W + 3, SCROLL_H))
            self.falling_timer = 0
            new_layer = True

        return self.falling, new_layer

    def draw(self, screen, camera_y: float, scale):
        for plat in self.platforms:
            pg.draw.rect(screen, WORLD_COLOR,
                         (plat.x * scale, (plat.y - camera_y) * scale,
                          plat.width * scale, plat.height * scale))
        for coin in self.coins:
            pg.draw.rect(screen, (255, 200, 60),
                         (coin.x * scale, (coin.y - camera_y) * scale,
                          coin.width * scale, coin.height * scale))
        for obs in self.obstacles:
            pg.draw.rect(screen, (100, 100, 100),
                         (obs.x * scale, (obs.y - camera_y) * scale,
                          obs.width * scale, obs.height * scale))
