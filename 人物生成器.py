#coding=gbk
import json
import os


class Character:

    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.need_exp = 10
        self.position = []

    def equip_prop(self, prop):
        self.attack = self.attack + prop.attack
        self.defence = self.defence + prop.defence
        self.health = self.health + prop.health
        self.magic = self.magic + prop.magic
        self.critical = self.critical + prop.critical
        self.speed = self.speed + prop.speed
        self.luck = self.luck + prop.luck
        self.insight = self.insight + prop.insight
        self.position.append(prop.pos)

    def unload_prop(self, prop):
        self.attack = self.attack - prop.attack
        self.defence = self.defence - prop.defence
        self.health = self.health - prop.health
        self.magic = self.magic - prop.magic
        self.critical = self.critical - prop.critical
        self.speed = self.speed - prop.speed
        self.luck = self.luck - prop.luck
        self.insight = self.insight - prop.insight
        self.position.remove(prop.pos)

    def set_growth_ability(self, attack, defence, health, magic, critical, speed, luck, insight):
        self.grow_attack = attack
        self.grow_defence = defence
        self.grow_health = health
        self.grow_magic = magic
        self.grow_critical = critical
        self.grow_speed = speed
        self.grow_luck = luck
        self.grow_insight = insight

    def set_ability(self, attack, defence, health, magic, critical, speed, luck, insight):
        self.attack = attack
        self.defence = defence
        self.health = health
        self.magic = magic
        self.critical = critical
        self.speed = speed
        self.luck = luck
        self.insight = insight

    def growth(self):
        self.attack += self.grow_attack
        self.defence += self.grow_defence
        self.health += self.grow_health
        self.magic += self.grow_magic
        self.critical += self.grow_critical
        self.speed += self.grow_speed
        self.luck += self.grow_luck
        self.insight += self.grow_insight

    def set_cur_ability(self):
        """set cur_ability"""
        self.cur_attack = self.attack
        self.cur_defence = self.defence
        self.cur_health = self.health
        self.cur_speed = self.speed
        self.cur_magic = self.magic

    def change_cur_ability(self, attack, defence, health, speed, magic):
        """change cur_ability"""
        self.cur_attack = self.cur_attack + attack
        if self.cur_attack < 0:
            self.cur_attack = 0
        self.cur_defence = self.cur_defence + defence
        if self.cur_defence < 0:
            self.cur_defence = 0
        self.cur_health = self.cur_health + health
        if self.cur_health < 0:
            self.cur_health = 0
        elif self.cur_health > self.health:
            self.cur_health = self.health
        self.cur_magic = self.cur_magic + magic
        if self.cur_magic < 0:
            self.cur_magic = 0
        elif self.cur_magic > self.magic:
            self.cur_magic = self.magic
        self.cur_speed = self.cur_speed + speed
        if self.cur_speed < 0:
            self.speed = 0

    def up_level(self, remainder):
        self.level += 1
        self.need_exp *= 1.5
        self.exp = remainder
        self.growth()

    def change_character_dic(self, characters_list):
        """add a character to characters_list"""
        dic = {'name': self.name, 'attack': self.attack, 'defence': self.defence, 'health': self.health, 'magic': self.magic,
               'critical': self.critical, 'speed': self.speed, 'luck': self.luck, 'insight': self.insight, 'level': self.level,
               'exp': self.exp, 'need_exp':self.need_exp, 'grow_attack': self.grow_attack, 'grow_defence': self.grow_defence,
               'grow_health': self.grow_health, 'grow_magic': self.grow_magic, 'grow_critical': self.grow_critical,
               'grow_speed': self.grow_speed, 'grow_luck': self.grow_luck, 'grow_insight': self.grow_insight, 'position': self.position}
        characters_list.append(dic)

    def alter_character_ability(self, contents):
        """alter a character in contents"""
        for i in contents['characters']:
            if i['name'] == self.name:
                i['attack'] = self.attack
                i['defence'] = self.defence
                i['health'] = self.health
                i['magic'] = self.magic
                i['critical'] = self.critical
                i['speed'] = self.speed
                i['luck'] = self.luck
                i['insight'] = self.insight
                i['level'] = self.level
                i['need_exp'] = self.need_exp
                i['exp'] = self.exp
                i['grow_attack'] = self.grow_attack
                i['grow_defence'] = self.grow_defence
                i['grow_health'] = self.grow_health
                i['grow_magic'] = self.grow_magic
                i['grow_luck'] = self.grow_luck
                i['grow_speed'] = self.grow_speed
                i['grow_insight'] = self.grow_insight
                i['grow_critical'] = self.grow_critical
                i['position'] = self.position

    def create_character(self, attack, defence, health, magic, critical, speed, luck, insight, g_attack, g_defence,
                    g_health, g_magic, g_critical, g_speed, g_luck, g_insight, dic):
        self.set_ability(attack, defence, health, magic, critical, speed, luck, insight)
        self.set_growth_ability(g_attack, g_defence, g_health, g_magic, g_critical, g_speed, g_luck, g_insight)
        self.change_character_dic(dic)

    def get_exp(self, get_exp):
        self.exp += get_exp
        if self.exp >= self.need_exp:
            remainder = self.exp - self.need_exp
            self.up_level(remainder)


def load_characters(contents, characters_list):
    for i in contents['characters']:
        ch = Character(i['name'])
        ch.set_ability(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'], i['luck'], i['insight'])
        ch.set_growth_ability(i['grow_attack'], i['grow_defence'], i['grow_health'], i['grow_magic'], i['grow_critical'],
                              i['grow_speed'], i['grow_luck'], i['grow_insight'])
        ch.exp = i['exp']
        ch.need_exp = i['need_exp']
        ch.level = i['level']
        ch.position = i['position']
        characters_list.append(ch)


def down_characters(contents, characters_list):
    for i in characters_list:
        i.alter_character_ability(contents)

def load_file():
    """存档读取"""
    if not os.path.exists('fileSave.json'):
        with open('fileSave.json', 'a') as f:
            characters = []
            drug = []
            dic = {'plot': 0, 'money': 0, 'characters': characters, 'drug': drug}
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
role = Character(name)
attack = int(input('attack: '))
defence = int(input('defence: '))
health = int(input('health: '))
magic = int(input('magic: '))
critical = int(input('critical: '))
speed = int(input('speed: '))
luck = int(input('luck: '))
insight = int(input('insight: '))
g_attack = int(input('grow_attack: '))
g_defence = int(input('grow_defence: '))
g_health = int(input('grow_health: '))
g_magic = int(input('grow_magic: '))
g_speed = int(input('grow_speed: '))
g_critical = int(input('grow_critical: '))
g_luck = int(input('grow_luck: '))
g_insight = int(input('grow_insight: '))
role.create_character(attack, defence, health, magic, critical, speed, luck, insight, g_attack, g_defence,
                    g_health, g_magic, g_critical, g_speed, g_luck, g_insight, contents['characters'])
down_file(contents)
