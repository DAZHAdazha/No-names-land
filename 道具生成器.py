import json
import os


class Prop:

    def __init__(self, name, pos):
        """type include 1,2,3,4,5,6"""
        self.name = name
        self.level = 1
        self.exp = 0
        self.need_exp = 10
        self.num = 0
        self.pos = pos

    def set_prop_ability(self, attack, defence, health, magic, critical, speed, luck):
        self.attack = attack
        self.defence = defence
        self.health = health
        self.magic = magic
        self.critical = critical
        self.speed = speed
        self.luck = luck

    def prop_growth_ability(self, attack, defence, health, magic, critical, speed, luck):
        self.grow_attack = attack
        self.grow_defence = defence
        self.grow_health = health
        self.grow_magic = magic
        self.grow_critical = critical
        self.grow_speed = speed
        self.grow_luck = luck

    def growth(self):
        self.attack += self.grow_attack
        self.defence += self.grow_defence
        self.health += self.grow_health
        self.magic += self.grow_magic
        self.critical += self.grow_critical
        self.speed += self.grow_speed
        self.luck += self.grow_luck

    def up_level(self, remainder):
        self.level += 1
        self.need_exp *= 1.5
        self.exp = remainder
        self.growth()

    def add_prop_list(self, props_list):
        """add a prop to props_list"""
        dic = {'name': self.name, 'attack': self.attack, 'defence': self.defence, 'health': self.health, 'magic': self.magic,
               'critical': self.critical, 'speed': self.speed, 'luck': self.luck, 'level': self.level,
               'exp': self.exp, 'need_exp':self.need_exp, 'grow_attack': self.grow_attack, 'grow_defence': self.grow_defence,
               'grow_health': self.grow_health, 'grow_magic': self.grow_magic, 'grow_critical': self.grow_critical,
               'grow_speed': self.grow_speed, 'grow_luck': self.grow_luck, 'num': self.num, 'pos': self.pos}
        props_list.append(dic)

    def alter_prop_list(self, props_list):
        """alter a prop in contents"""
        for i in props_list:
            if i['name'] == self.name:
                i['attack'] = self.attack
                i['defence'] = self.defence
                i['health'] = self.health
                i['magic'] = self.magic
                i['critical'] = self.critical
                i['speed'] = self.speed
                i['luck'] = self.luck
                i['level'] = self.level
                i['need_exp'] = self.need_exp
                i['exp'] = self.exp
                i['grow_attack'] = self.grow_attack
                i['grow_defence'] = self.grow_defence
                i['grow_health'] = self.grow_health
                i['grow_magic'] = self.grow_magic
                i['grow_luck'] = self.grow_luck
                i['grow_speed'] = self.grow_speed
                i['grow_critical'] = self.grow_critical
                i['num'] = self.num
                i['pos'] = self.pos

    def create_prop(self, attack, defence, health, magic, critical, speed, luck, g_attack, g_defence,
                    g_health, g_magic, g_critical, g_speed, g_luck, props_list):
        self.set_prop_ability(attack, defence, health, magic, critical, speed, luck)
        self.prop_growth_ability(g_attack, g_defence, g_health, g_magic, g_critical, g_speed, g_luck)
        self.add_prop_list(props_list)

    def get_exp(self, get_exp, props_list):
        self.exp += get_exp
        while self.exp >= self.need_exp:
            remainder = self.exp - self.need_exp
            self.up_level(remainder)
        self.alter_prop_list(props_list)

    def get_new_prop(self, props_list):
        for i in props_list:
            if i['name'] == self.name:
                i['num'] += 1
                break

    def destroy_prop(self, props_list):
        for i in props_list:
            if i['name'] == self.name:
                if i['num'] > 0:
                    i['num'] -= 1
                    break

    def grow_prop(self, prop, props_list):
        for i in props_list:
            if i['name'] == prop.name:
                i.num -= 1
            if self.name == i['name']:
                exp = prop.need_exp * prop.level
                self.get_exp(exp, props_list)


def load_props(contents, props_list):
    for i in contents['props']:
        p = Prop(i['name'])
        p.set_prop_ability(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'], i['luck'])
        p.prop_growth_ability(i['grow_attack'], i['grow_defence'], i['grow_health'], i['grow_magic'], i['grow_critical'],
                              i['grow_speed'], i['grow_luck'])
        p.exp = i['exp']
        p.need_exp = i['need_exp']
        p.level = i['level']
        p.num = i['num']
        p.pos = i['pos']
        props_list.append(p)


def down_props(contents, props_list):
    contents['props'] = props_list


def load_file():
    """存档读取"""
    if not os.path.exists('fileSave.json'):
        with open('fileSave.json', 'a') as f:
            characters = []
            drug = []
            props = []
            dic = {'plot': 0, 'money': 0, 'characters': characters, 'drug': drug, 'props': props}
            dic = json.dumps(dic, indent=4, ensure_ascii=False)
            f.write(dic)
    with open('fileSave.json', 'r', encoding='utf-8') as file_object:
        contents = json.load(file_object)
    return contents


def down_file(contents):
    """保存存档"""
    contents = json.dumps(contents, indent=4, ensure_ascii=False)
    with open('fileSave.json', 'w', encoding='utf-8') as file_object:
        """覆盖原存档"""
        file_object.write(contents)


contents = load_file()
name = str(input('name: '))
pos = int(input('position: '))
prop = Prop(name, pos)
attack = int(input('attack: '))
defence = int(input('defence: '))
health = int(input('health: '))
magic = int(input('magic: '))
critical = int(input('critical: '))
speed = int(input('speed: '))
luck = int(input('luck: '))
g_attack = int(input('grow_attack: '))
g_defence = int(input('grow_defence: '))
g_health = int(input('grow_health: '))
g_magic = int(input('grow_magic: '))
g_speed = int(input('grow_speed: '))
g_critical = int(input('grow_critical: '))
g_luck = int(input('grow_luck: '))
prop.create_prop(attack, defence, health, magic, critical, speed, luck, g_attack, g_defence,
                    g_health, g_magic, g_critical, g_speed, g_luck, contents['props'])
down_file(contents)
