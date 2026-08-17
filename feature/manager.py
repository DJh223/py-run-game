import json
import os
import random



class SkillsManager:
    """技能管理"""
    def __init__(self, json_path = "data/skills.json"):
        #加载数据
        self.db = self._load_json(json_path)

        self.unlocked = set()
        self.values = {}

    def _load_json(self, path):
        """读取 JSON 文件"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__ )))
        full_path = os.path.join(base_dir, path)

        try:
            with open (full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("skills",{})
        except FileNotFoundError:           #没找到文件，返回空
            return {}                       
        except json.JSONDecodeError:        #格式有问题
            return {}


    def pickup(self, skill_id):
        """玩家碰到碎片时调用，返回 True 表示拾取成功"""
        if skill_id not in self.db:
            return False    #该技能不存在

        if skill_id in self.unlocked:
            return False    #拥有该技能

        # 检查前置依赖
        prere = self.db[skill_id].get("prerequisite")
        if prere is not None:
            if prere not in self.unlocked:
                return False

        self.unlocked.add(skill_id)

        default_val = self.db[skill_id].get("default_value")
        if default_val is not None:
            self.values[skill_id] = default_val

        return True

    # 判断是否激活
    def is_active(self, skill_id):
        return skill_id in self.unlocked

    # 获取数值（带默认值保护）
    def get_value(self, skill_id, default=0):
        return self.values.get(skill_id, default)

    # 覆盖逻辑（处理“捡到新碎片替换旧碎片”）
    def override_value(self, skill_id, new_value):
        if skill_id in self.unlocked:
            self.values[skill_id] = new_value
            return True
        return False

    # 从玩家已经拥有的技能里随机删
    def remove_random(self):
        if not  self.unlocked:
            return None

        victim = random.choice(list(self.unlocked))

        self.unlocked.remove(victim)

        if victim in self.values:
            del self.values[victim]

        return victim



class StateManager:
    """状态管理"""
    def __init__(self, json_path = "data/state.json"):
        #加载数据
        self.db = self._load_json(json_path)

        self.unlocked = set()
        self.values = {}

    def _load_json(self, path):
        """读取 JSON 文件"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__ )))
        full_path = os.path.join(base_dir, path)

        try:
            with open (full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("state",{})
        except FileNotFoundError:           #没找到文件，返回空
            return {}                       
        except json.JSONDecodeError:        #格式有问题
            return {}


    def pickup(self, state_id):
        """玩家碰到碎片时调用，返回 True 表示拾取成功"""
        if state_id not in self.db:
            return False    #不存在

        if state_id in self.unlocked:
            return False    #拥有

        # 检查前置依赖
        prere = self.db[state_id].get("prerequisite")
        if prere is not None:
            if prere not in self.unlocked:
                return False

        self.unlocked.add(state_id)

        default_val = self.db[state_id].get("default_value")
        if default_val is not None:
            self.values[state_id] = default_val

        return True

    # 判断是否激活
    def is_active(self, state_id):
        return state_id in self.unlocked

    # 获取数值（带默认值保护）
    def get_value(self, state_id, default=0):
        return self.values.get(state_id, default)

    # 覆盖逻辑（处理“捡到新碎片替换旧碎片”）
    def override_value(self, state_id, new_value):
        if state_id in self.unlocked:
            self.values[state_id] = new_value
            return True
        return False

            
