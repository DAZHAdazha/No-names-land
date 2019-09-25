import pygame
import time
import sys
import json
import os
import re
import random

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREY = 128, 128, 128
CREAM = 230, 230, 230
YELLOW = 255,255,0
size = width, height = 1100, 800  # size of the window
fps = 300  # frames per second for game
path = os.getcwd()
files = os.listdir(path)

pygame.init()
screen = pygame.display.set_mode(size)
fclock = pygame.time.Clock()

font = pygame.font.Font("ShenYunSuXinTi-2.ttf", 32)
font_small = pygame.font.Font("ShenYunSuXinTi-2.ttf", 20)
icon = pygame.image.load("./image/icon.png")
pygame.display.set_icon(icon)
character_images = pygame.image.load("./image/角色.png")
character_image = character_images.get_rect()
character_image = character_image.move(width - 60, height - 60)
bag_images = pygame.image.load("./image/背包.png")
bag_image = bag_images.get_rect()
bag_image = bag_image.move(width - 120, height - 60)
achievement_images = pygame.image.load("./image/成就.png")
achievement_image = achievement_images.get_rect()
achievement_image = achievement_image.move(width - 180, height - 60)
strengthen_images = pygame.image.load("./image/强化.png")
strengthen_image = strengthen_images.get_rect()
strengthen_image = strengthen_image.move(width / 2 - 90, 100)
sale_images = pygame.image.load("./image/出售.png")
sale_image = sale_images.get_rect()
sale_image = sale_image.move((width - 200) / 3 - 140, 100)
enchant_images = pygame.image.load("./image/附魔.png")
enchant_image = enchant_images.get_rect()
enchant_image = enchant_image.move((width - 200) / 1.5 + 160, 100)
shoe_images = pygame.image.load("./image/鞋子.png")
sword_images = pygame.image.load("./image/剑.png")
helmet_images = pygame.image.load("./image/头盔.png")
ring_images = pygame.image.load("./image/戒指.png")
armor_images = pygame.image.load("./image/护甲.png")
wand_images = pygame.image.load("./image/法杖.png")
bow_images = pygame.image.load("./image/弓箭.png")
title_images = pygame.image.load("./image/称号.png")
big_health_images = pygame.image.load("./image/大红药.png")
small_health_images = pygame.image.load("./image/小红药.png")
big_magic_images = pygame.image.load("./image/大蓝药.png")
small_magic_images = pygame.image.load("./image/小蓝药.png")
big_attack_images = pygame.image.load("./image/攻击药剂（大）.png")
small_attack_images = pygame.image.load("./image/攻击药剂（小）.png")
enchant_material_images = pygame.image.load("./image/附魔材料.png")
vocational_material_images = pygame.image.load("./image/职业材料.png")
mission_material_images = pygame.image.load("./image/任务材料.png")
pygame.display.set_caption("无名之地")


class Material:
    def __init__(self, name):
        self.name = name

    def create_new_material(self, attack, defence, health, magic, critical, speed, luck, num, value, type):
            self.attack = attack
            self.defence = defence
            self.health = health
            self.magic = magic
            self.critical = critical
            self.speed = speed
            self.luck = luck
            self.num = num
            self.value = value
            self.type = type


class Baggage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.objects = []
        self.amount = 0


class Prop:
    def __init__(self, name):
        self.name = name

    def create_new_prop(self, attack, defence, health, magic, critical, speed, luck, grow_attack, grow_defence,
                        grow_health, grow_magic, grow_critical, grow_speed, grow_luck, value, pos, level=1,
                        exp=0, need_exp=10, enchant_time=5, is_wear=0, numb=1):
        """numb 表示此装备的序列号"""
        """-1 = 法杖， 1 = 剑， 0 = 弓箭, 2 = helmet, 3 = armor, 4 = shoes, 5 = ornament, 6 = title"""
        #  is_wear = 0,1,2,3 0 for not wearing, 1,2,3 for character 1, 2, 3
        self.level = level
        self.exp = exp
        self.need_exp = need_exp
        self.pos = pos
        self.enchant_time = enchant_time  # 剩余的附魔次数
        self.grow_attack = grow_attack
        self.grow_defence = grow_defence
        self.grow_health = grow_health
        self.grow_magic = grow_magic
        self.grow_critical = grow_critical
        self.grow_speed = grow_speed
        self.grow_luck = grow_luck
        self.attack = attack
        self.defence = defence
        self.health = health
        self.magic = magic
        self.critical = critical
        self.speed = speed
        self.luck = luck
        self.is_wear = is_wear
        self.value = value
        self.numb = numb

    def up_level(self, exp):
        self.exp += exp
        while self.exp >= self.need_exp:
            self.value += self.need_exp//2
            self.level += 1
            self.exp = self.exp - self.need_exp
            self.need_exp *= 2
            self.attack += self.grow_attack
            self.defence += self.grow_defence
            self.health += self.grow_health
            self.magic += self.grow_magic
            self.critical += self.grow_critical
            self.speed += self.grow_speed
            self.luck += self.grow_luck


class Drug:
    def __init__(self, name):
        self.name = name

    def create_new_drug(self, attack, defence, health, speed, magic, num, value):
        self.num = num
        self.attack = attack
        self.defence = defence
        self.health = health
        self.speed = speed
        self.magic = magic
        self.value = value


class Character:
    def __init__(self, name):
        self.name = name

    def create_new_character(self, attack, defence, health, magic, critical, speed, luck, insight, grow_attack,
                             grow_defence, grow_health, grow_magic, grow_critical, grow_speed, grow_luck, grow_insight,
                             level=1, exp=0, need_exp=10, position=[]):
        self.level = level
        self.exp = exp
        self.need_exp = need_exp
        self.position = position
        self.grow_attack = grow_attack
        self.grow_defence = grow_defence
        self.grow_health = grow_health
        self.grow_magic = grow_magic
        self.grow_critical = grow_critical
        self.grow_speed = grow_speed
        self.grow_luck = grow_luck
        self.grow_insight = grow_insight
        self.attack = attack
        self.defence = defence
        self.health = health
        self.magic = magic
        self.critical = critical
        self.speed = speed
        self.luck = luck
        self.insight = insight

    def up_level(self, exp):
        self.exp += exp
        while self.exp >= self.need_exp:
            self.level += 1
            self.exp = self.exp - self.need_exp
            self.need_exp *= 2
            self.attack += self.grow_attack
            self.defence += self.grow_defence
            self.health += self.grow_health
            self.magic += self.grow_magic
            self.critical += self.grow_critical
            self.speed += self.grow_speed
            self.luck += self.grow_luck
            self.insight += self.grow_insight

    def character_cur_ability(self):
        """set cur_ability"""
        self.cur_attack = self.attack
        self.cur_defence = self.defence
        self.cur_health = self.health
        self.cur_speed = self.speed
        self.cur_magic = self.magic


def load_file():
    """存档读取"""
    if not os.path.exists('fileSave.json'):
        with open('fileSave.json', 'a') as f:
            characters = []
            drug = []
            props = []
            materials = []
            dic = {'plot': 0, 'money': 0, 'characters': characters, 'drug': drug, 'props': props, 'materials': materials}
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


def make_lists(contents, props_list, drug_list, characters_list, materials_list):
    """存档变列表"""
    for j in contents['characters']:
        ch = Character(j['name'])
        ch_prop = []
        for i in j['position']:
            prop = Prop(i['name'])
            prop.create_new_prop(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'],
                                 i['luck'],
                                 i['grow_attack'], i['grow_defence'], i['grow_health'], i['grow_magic'],
                                 i['grow_critical'],
                                 i['grow_speed'], i['grow_luck'], i['value'], i['pos'], i['level'], i['exp'],
                                 i['need_exp'], i['enchant_time'], i['is_wear'], i['numb'])
            ch_prop.append(prop)
        ch.create_new_character(j['attack'], j['defence'], j['health'], j['magic'], j['critical'], j['speed'], j['luck'],
                                j['insight'], j['grow_attack'], j['grow_defence'], j['grow_health'], j['grow_magic'],
                                j['grow_critical'], j['grow_speed'], j['grow_luck'], j['grow_insight'], j['level'],
                                j['exp'], j['need_exp'], ch_prop)
        characters_list.append(ch)
    for i in contents['props']:
        prop = Prop(i['name'])
        prop.create_new_prop(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'], i['luck'],
                             i['grow_attack'], i['grow_defence'], i['grow_health'], i['grow_magic'], i['grow_critical'],
                             i['grow_speed'], i['grow_luck'], i['value'], i['pos'], i['level'], i['exp'],
                             i['need_exp'], i['enchant_time'], i['is_wear'], i['numb'])
        props_list.append(prop)
    for i in contents['drug']:
        drug = Drug(i['name'])
        drug.create_new_drug(i['attack'], i['defence'], i['health'], i['speed'], i['magic'], i['num'], i['value'])
        drug_list.append(drug)
    for i in contents['materials']:
        material = Material(i['name'])
        material.create_new_material(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'],
                                     i['luck'], i['num'], i['value'], i['type'])
        materials_list.append(material)


def show_lines(lines, t):
    for i in range(len(lines)):
        texts = font.render(lines[i], True, BLACK)
        text = texts.get_rect()
        text.center = (width/2, 100 + i*200)
        screen.blit(texts, text)
        pygame.display.update()  # watch out its position
        time.sleep(t)


def show_words(words, coord, font, color):
    texts = font.render(words, True, color)
    text = texts.get_rect()
    text.center = (coord[0], coord[1])
    screen.blit(texts, text)


def show_attr(character, coord):
    show_words('经验:' + str(character.exp) + '/' + str(character.need_exp), (coord[0] + 72, coord[1]), font, BLACK)
    show_words('攻击:' + str(character.attack), (coord[0], coord[1] + 50), font, BLACK)
    show_words('防御:' + str(character.defence), (coord[0] + 145, coord[1] + 50), font, BLACK)
    show_words('生命:' + str(character.health), (coord[0], coord[1] + 100), font, BLACK)
    show_words('魔法:' + str(character.magic), (coord[0] + 145, coord[1] + 100), font, BLACK)
    show_words('暴击:' + str(character.critical), (coord[0], coord[1] + 150), font, BLACK)
    show_words('速度:' + str(character.speed), (coord[0] + 145, coord[1] + 150), font, BLACK)
    show_words('幸运:' + str(character.luck), (coord[0], coord[1] + 200), font, BLACK)
    show_words('洞视:' + str(character.insight), (coord[0] + 145, coord[1] + 200), font, BLACK)
    show_words('等级:' + str(character.level), (coord[0], coord[1] + 250), font, BLACK)


def refresh_lists(baggage, props_list, drug_list, materials_list):
    """背包存入列表"""
    props_list.clear()
    drug_list.clear()
    materials_list.clear()
    for i in baggage.objects:
        if Prop == type(i):
            props_list.append(i)
        elif Drug == type(i):
            drug_list.append(i)
        elif Material == type(i):
            materials_list.append(i)


def refresh_content(contents, characters_list, props_list, drug_list, materials_list):
    """列表变存档"""
    contents['characters'].clear()
    contents['drug'].clear()
    contents['props'].clear()
    contents['materials'].clear()
    for i in characters_list:
        dic = {'name': i.name, 'attack': i.attack, 'defence': i.defence, 'health': i.health,
               'magic': i.magic, 'critical': i.critical, 'speed': i.speed, 'luck': i.luck,
               'insight': i.insight, 'level': i.level, 'exp': i.exp, 'need_exp': i.need_exp,
               'grow_attack': i.grow_attack, 'grow_defence': i.grow_defence, 'grow_health': i.grow_health,
               'grow_magic': i.grow_magic, 'grow_critical': i.grow_critical, 'grow_speed': i.grow_speed,
               'grow_luck': i.grow_luck, 'grow_insight': i.grow_insight, 'position': i.position}
        prop_dic = []
        for j in dic['position']:
            prop= {'name': j.name, 'attack': j.attack, 'defence': j.defence, 'health': j.health, 'magic': j.magic,
                        'critical': j.critical, 'speed': j.speed, 'luck': j.luck, 'level': j.level,'exp': j.exp,
                        'need_exp': j.need_exp, 'grow_attack': j.grow_attack, 'grow_defence': j.grow_defence,
                        'grow_health': j.grow_health, 'grow_magic': j.grow_magic, 'grow_critical': j.grow_critical,
                        'grow_speed': j.grow_speed, 'grow_luck': j.grow_luck, 'pos': j.pos, 'value': j.value,
                        'is_wear': j.is_wear, 'enchant_time': j.enchant_time, 'numb': j.numb}
            prop_dic.append(prop)
        dic['position'] = prop_dic
        content['characters'].append(dic)
    for i in drug_list:
        dic = {'name': i.name, 'attack': i.attack, 'defence': i.defence, 'health': i.health,
               'magic': i.magic, 'speed': i.speed, 'value': i.value, 'num': i.num}
        content['drug'].append(dic)
    for i in props_list:
        dic = {'name': i.name, 'attack': i.attack, 'defence': i.defence, 'health': i.health,
               'magic': i.magic, 'critical': i.critical, 'speed': i.speed, 'luck': i.luck, 'level': i.level,
               'exp': i.exp, 'need_exp': i.need_exp, 'grow_attack': i.grow_attack, 'grow_defence': i.grow_defence,
               'grow_health': i.grow_health, 'grow_magic': i.grow_magic, 'grow_critical': i.grow_critical,
               'grow_speed': i.grow_speed, 'grow_luck': i.grow_luck, 'pos': i.pos, 'value': i.value,
               'is_wear': i.is_wear, 'enchant_time': i.enchant_time, 'numb': i.numb}
        content['props'].append(dic)
    for i in materials_list:
        dic = {'name': i.name, 'attack': i.attack, 'defence': i.defence, 'health': i.health, 'critical': i.critical,
               'magic': i.magic, 'speed': i.speed, 'value': i.value, 'num': i.num, 'luck': i.luck, 'type': i.type}
        content['materials'].append(dic)


def add_prop_character(character, prop, num):
    """人物装备道具"""
    character.attack += prop.attack
    character.defence += prop.defence
    character.health += prop.health
    character.magic += prop.magic
    character.critical += prop.critical
    character.luck += prop.luck
    character.speed += prop.speed
    for i in character.position:
        if prop.pos <= 1:
            if i.pos <= 1:
                remove_prop_character(character, i)
                break
        else:
            if i.pos == prop.pos:
                remove_prop_character(character, i)
                break
    if prop.is_wear != 0:
        remove_prop_character(character_list[prop.is_wear-1], prop)
    character.position.append(prop)
    prop.is_wear = num
    for i in prop_list:
        if i.name == prop.name and i.numb == prop.numb:
            i.is_wear = prop.is_wear
    for i in character_list:
        if i.name == character.name:
            i.position = character.position
    refresh_baggage(baggage, prop_list, drug_list, material_list)


def remove_prop_character(character, prop):
    """移除装备"""
    for i in character.position:
        if i.name == prop.name:
            character.position.remove(i)
    prop.is_wear = 0
    for i in character_list:
        if i.name == character.name:
            i.position = character.position
    refresh_baggage(baggage, prop_list, drug_list, material_list)
    for i in prop_list:
        if i.name == prop.name and i.numb == prop.numb:
            i.is_wear = 0
    character.attack -= prop.attack
    character.defence -= prop.defence
    character.health -= prop.health
    character.magic -= prop.magic
    character.critical -= prop.critical
    character.luck -= prop.luck
    character.speed -= prop.speed


def strengthen_prop(prop):
    """强化装备"""
    level = prop.level
    chance = 100 - ((level - 1) * 10)
    if level == 10:
        return 2  # 2 for out of range
    if content['money'] < baggage.objects[chose_num].need_exp:
        return 3  # 3 for lack of money
    content['money'] -= baggage.objects[chose_num].need_exp
    rand = random.randint(1, 100)
    if rand <= chance:
        prop.up_level(prop.need_exp)
        if prop.is_wear != 0:
            for i in character_list[prop.is_wear - 1].position:
                if i.name == prop.name and i.numb == prop.numb:
                    i.attack = prop.attack
                    i.defence = prop.defence
                    i.health = prop.health
                    i.magic = prop.magic
                    i.critical = prop.critical
                    i.speed = prop.speed
                    i.luck = prop.luck
                    i.value = prop.value
                    i.level = prop.level
                    i.need_exp = prop.need_exp
                    i.exp = prop.exp
        for i in prop_list:
            if i.name == prop.name and i.numb == prop.numb:
                i.attack = prop.attack
                i.defence = prop.defence
                i.health = prop.health
                i.magic = prop.magic
                i.critical = prop.critical
                i.speed = prop.speed
                i.luck = prop.luck
                i.value = prop.value
                i.level = prop.level
                i.need_exp = prop.need_exp
                i.exp = prop.exp
        refresh_baggage(baggage, prop_list, drug_list, material_list)
        return 1  # 1 for success
    else:
        return 0  # 0 for fail


def enchant_prop(prop, material):
    for i in prop_list:
        if i.name == prop.name and i.numb == prop.numb:
            i.enchant_time -= 1
            i.attack += material.attack
            i.defence += material.defence
            i.health += material.health
            i.magic += material.magic
            i.critical += material.critical
            i.speed += material.speed
            i.luck += material.luck
            i.value += material.value // 2
    if prop.is_wear != 0:
        for i in character_list[prop.is_wear - 1].position:
            if i.name == prop.name and i.numb == prop.numb:
                i.enchant_time = prop.enchant_time
                i.attack = prop.attack
                i.defence = prop.defence
                i.health = prop.health
                i.magic = prop.magic
                i.critical = prop.critical
                i.speed = prop.speed
                i.luck = prop.luck
                i.value = prop.value
    refresh_baggage(baggage, prop_list, drug_list, material_list)


def is_new(contents):
    new = contents["plot"]
    plot_1 = ["一觉醒来，你不知道自己身处何处，", "甚至自己是何许人也亦无从得知，世界犹如混沌般恍惚。", "徘徊于这谜一般的大陆上，你决定只身探索，寻找真相......"]
    if new == 0:
        contents["plot"] = 1
        """测试为0，实际为1"""
        screen.fill(CREAM)
        show_lines(plot_1, 2)
        pygame.display.update()
        fclock.tick(fps)
        down_file(contents)


def draw_window():
    pygame.draw.rect(screen, BLACK, (100, 50, width - 200, height - 200), 4)
    """rect stand for (x,y,width,height)"""
    pygame.draw.rect(screen, BLACK, (width - 130, 50, 30, 30), 4)
    pygame.draw.line(screen, RED, (width - 125, 55), (width - 105, 75), 4)
    pygame.draw.line(screen, RED, (width - 105, 55), (width - 125, 75), 4)
    pygame.display.update()
    fclock.tick(fps)


def close_window():
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():  # magic move
        if event.type == pygame.QUIT:  # close the window
            content['baggage'] = baggage.amount  # put into fileSave
            refresh_content(content, character_list, prop_list, drug_list, material_list)
            down_file(content)
            sys.exit()
    if width - 130 < mouse_pos[0] < width - 100 and 50 < mouse_pos[1] < 80 and mouse_pressed[0] == 1:
        return 1


def show_image(item_list_image, coord, id, num):
    dic = {'-1': wand_images, '0': bow_images, '1': sword_images, '2': helmet_images, '3': armor_images,
           '4': shoe_images, '5': ring_images, '6': title_images, '大红药': big_health_images,
           '小红药': small_health_images, '大蓝药': big_magic_images, '小蓝药': small_magic_images,
           '小攻击药': small_attack_images, '大攻击药': big_attack_images, '附魔材料':enchant_material_images,
           '职业材料':vocational_material_images, '任务材料':mission_material_images}
    item_list_image.append(dic[id].get_rect())
    item_list_image[num] = item_list_image[num].move(coord)
    screen.blit(dic[id], item_list_image[num])
    return item_list_image


def show_object(baggage):
    item_list_image = []
    j = 0
    for i in baggage.objects:
        coord = j % 6 * 150 + 150, j // 6 * 150 + 70
        if type(i) == Prop:
            item_list_image = show_image(item_list_image, coord, str(i.pos), j)
            if i.is_wear > 0:
                pygame.draw.line(screen, RED, (j % 6 * 150 + 115, j // 6 * 150 + 65), (j % 6 * 150 + 125, j // 6 * 150
                                                                                       + 75), 4)
                pygame.draw.line(screen, RED, (j % 6 * 150 + 125, j // 6 * 150 + 75), (j % 6 * 150 + 145, j // 6 * 150
                                                                                       + 55), 4)
                show_words(str(character_list[i.is_wear - 1].name),
                           (j % 6 * 150 + 190, j // 6 * 150 + 60), font_small, GREY)
        elif type(i) == Drug:
            item_list_image = show_image(item_list_image, coord, str(i.name), j)
        elif type(i) == Material:
            '''change into upper form'''
            item_list_image = show_image(item_list_image, coord, str(i.type), j)
        show_words(i.name, (j % 6 * 150 + 180, j // 6 * 150 + 150), font, BLACK)
        j += 1
    return len(item_list_image)


def click_on_props():
        mouse_pos = pygame.mouse.get_pos()
        for i in range(4):
            if 100 < mouse_pos[0] < width - 100 and 50 + i * 150 < mouse_pos[1] < 200 + i * 150:
                for j in range(6):
                    if 100 + j * 150 < mouse_pos[0] < 250 + j * 150:
                        return i * 6 + j
        return -1


def translate(word):
    translator = {'name': '名称', 'attack': '攻击', 'defence': '防御', 'health': '生命', 'magic': '魔法', 'critical': '暴击',
                  'speed': '速度', 'luck': '幸运', 'level': '等级', 'num': '数量', 'enchant_time': '可附魔次数',
                  'value': '价格', 'type': '类型'}
    return translator[word]


def sale_obj(baggage, obj, contents):
    """卖出物品"""
    contents['money'] += obj.value
    if Prop == type(obj):
        baggage.objects.remove(obj)
    else:
        for i in baggage.objects:
            if i.name == obj.name:
                i.num -= 1
                if i.num <= 0:
                    baggage.objects.remove(i)
                    baggage.amount -= 1
                break


def draw_character():
    pygame.draw.line(screen, GREY, (100, height / 2 - 50), (width - 100, height / 2 - 50), 4)
    pygame.draw.line(screen, BLACK, ((width - 200) / 3 + 100, 50), ((width - 200) / 3 + 100, height - 150), 4)
    pygame.draw.line(screen, BLACK, ((width - 200) / 1.5 + 105, 50), ((width - 200) / 1.5 + 105, height - 150), 4)
    show_words(character_list[0].name, ((width - 200) / 6 + 100, 100), font, BLACK)
    show_words(character_list[1].name, ((width - 200) / 2 + 100, 100), font, BLACK)
    show_words(character_list[2].name, ((width - 200) / 6 * 5 + 100, 100), font, BLACK)
    show_attr(character_list[0], ((width - 200) / 6 + 20, height / 2 - 20))
    show_attr(character_list[1], ((width - 200) / 2 + 20, height / 2 - 20))
    show_attr(character_list[2], ((width - 200) / 6 * 5 + 20, height / 2 - 20))
    for i in range(6):
        pygame.draw.rect(screen, GREY, (((width - 200) / 6 - 40 + 97 * (i % 3), 240 if i > 2 else 130), (85, 85)), 4)
        pygame.draw.rect(screen, GREY, (((width - 200) / 2 - 35 + 97 * (i % 3), 240 if i > 2 else 130), (85, 85)), 4)
        pygame.draw.rect(screen, GREY, (((width - 200) / 6 * 5 - 35 + 97 * (i % 3),
                                         240 if i > 2 else 130), (85, 85)), 4)
    item_list_image = []
    k = 0
    for i in range(3):
        for j in range(6):
            if j < len(character_list[i].position):
                coord = (width - 200) / 6 - 25 + 97 * (j % 3) + 308 * i - (i // 2) * 8, 250 if j > 2 else 140
                item_list_image = show_image(item_list_image, coord, str(character_list[i].position[j].pos), k)
                show_words(str(character_list[i].position[j].name),
                           ((width - 200) / 6 + 97 * (j % 3) + i * 300, 340 if j > 2 else 230),
                           font_small, RED)
                k += 1
    draw_window()


def draw_map():
    for point in point_list:
        pygame.draw.circle(screen, YELLOW, point, 15, 4)


def level_choose():
    i = 0
    for point in point_list:
        if point[0] - 25 < map_choice[0] < point[0] + 25 and point[1] - 25 < map_choice[1] < point[1] + 25:
            pygame.draw.circle(screen, RED, point, 15, 4)
            return i
        i += 1
    return -1

def refresh_baggage(baggage, props_list, drug_list, materials_list):
    """列表载入背包"""
    baggage.objects = props_list[:] + drug_list[:] + materials_list[:]
    baggage.amount = len(baggage.objects)


content = load_file()
baggage = Baggage(content['baggage'])
is_new(content)
character_list = []
drug_list = []
material_list = []
prop_list = []
make_lists(content,  prop_list, drug_list, character_list, material_list)
refresh_baggage(baggage, prop_list, drug_list, material_list)
map_choice = [20, height - 20]
map_x_velocity = 0
map_y_velocity = 0
flag = 0
point_list = [(100, 200), [200, 100], [300, 400], [500, 400]]
level_choice = -1

while True:
    screen.fill(CREAM)
    for event in pygame.event.get():  # event list
        if event.type == pygame.QUIT:  # close the window
            refresh_content(content, character_list, prop_list, drug_list, material_list)
            down_file(content)
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # event of press the key
            if event.key == pygame.K_d:
                map_x_velocity = 2
            if event.key == pygame.K_s:
                map_y_velocity = 2
            if event.key == pygame.K_a:
                map_x_velocity = -2
            if event.key == pygame.K_w:
                map_y_velocity = -2
        elif event.type == pygame.KEYUP:  # event of release the key
            if event.key == pygame.K_d:
                map_x_velocity = 0
            if event.key == pygame.K_s:
                map_y_velocity = 0
            if event.key == pygame.K_a:
                map_x_velocity = 0
            if event.key == pygame.K_w:
                map_y_velocity = 0
            if event.key == pygame.K_SPACE and level_choice is not -1:
                print(level_choice)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    '''return tuple object, which [0] represent left key, [1] for middle, [2] for right'''
    if width - 60 < mouse_pos[0] < width and height - 60 < mouse_pos[1] < height and mouse_pressed[0] == 1:
        '''character'''
        draw_character()
        draw_window()
        while True:
            if close_window() == 1:
                break
    if (width - 120 < mouse_pos[0] < width - 60 and height - 60 < mouse_pos[1] < height and mouse_pressed[0] == 1)\
            or flag == 1:
        """bag"""
        show_words("金钱：" + str(content['money']), (width / 2, 30), font, BLACK)
        for i in range(3):
            pygame.draw.line(screen, BLACK, (100, 200 + i * 150), (width - 100, 200 + i * 150), 4)
        for i in range(5):
            pygame.draw.line(screen, BLACK, (250 + i * 150, 50), (250 + i * 150, height - 150), 4)
        ''' put into function'''
        props_num = show_object(baggage)
        draw_window()
        flag = 0
        while True:
            if close_window() == 1:
                refresh_lists(baggage, prop_list, drug_list, material_list)
                break
            mouse_pressed = pygame.mouse.get_pressed()
            cur_word_1 = ''
            cur_word_2 = ''
            tag = 0
            if mouse_pressed[0] == 1:
                chose_num = click_on_props()
                if 0 <= chose_num < props_num:
                    pygame.draw.rect(screen, CREAM, ((0, height - 145), (1100, 145)))
                    word_len = 0
                    obj = vars(baggage.objects[chose_num])
                    for i in obj:
                        if not re.findall('(^grow|^need|pos|exp|is_wear|numb)', str(i)):
                            if obj[i] != 0:
                                if word_len < 6:
                                    cur_word_1 += translate(str(i)) + ':' + str(obj[i]) + ' '
                                    word_len += 1
                                else:
                                    cur_word_2 += translate(str(i)) + ':' + str(obj[i]) + ' '
                show_words(cur_word_1, (width / 2, height - 120), font, BLACK)
                show_words(cur_word_2, (width / 2, height - 70), font, BLACK)
            elif mouse_pressed[2] == 1:
                chose_num = click_on_props()
                if 0 <= chose_num < props_num:
                    chose_num = click_on_props()
                    if type(baggage.objects[chose_num]) == Material or type(baggage.objects[chose_num]) == Drug:
                        sale_obj(baggage, baggage.objects[chose_num], content)
                        refresh_lists(baggage, prop_list, drug_list, material_list)
                        time.sleep(0.2)
                        flag = 1
                        break
                    else:
                        screen.fill(CREAM)
                        pygame.draw.line(screen, BLACK, (100, 450), (width - 100, 450), 4)
                        pygame.draw.line(screen, BLACK, ((width - 200) / 3 + 100, 50),
                                         ((width - 200) / 3 + 100, 650), 4)
                        pygame.draw.line(screen, BLACK, ((width - 200) / 1.5 + 100, 50),
                                         ((width - 200) / 1.5 + 100, 650), 4)
                        show_words("售出", ((width - 200) / 3 - 50, 350), font, BLACK)
                        screen.blit(sale_images, sale_image)
                        show_words("强化", (width / 2, 350), font, BLACK)
                        screen.blit(strengthen_images, strengthen_image)
                        show_words("附魔", ((width - 200) / 1.5 + 250, 350), font, BLACK)
                        screen.blit(enchant_images, enchant_image)
                        show_words("装备于" + str(character_list[0].name), ((width - 200) / 3 - 50, 550), font, BLACK)
                        show_words("装备于" + str(character_list[1].name), (width / 2, 550), font, BLACK)
                        show_words("装备于" + str(character_list[2].name), ((width - 200) / 1.5 + 250, 550), font, BLACK)
                        draw_window()
                        while True:
                            mouse_pressed = pygame.mouse.get_pressed()
                            if mouse_pressed[0] == 1:
                                mouse_pos = pygame.mouse.get_pos()
                                if 100 < mouse_pos[0] < (width - 200) / 3 + 100 and 50 < mouse_pos[1] < 450:
                                    sale_obj(baggage, baggage.objects[chose_num], content)
                                    refresh_lists(baggage, prop_list, drug_list, material_list)
                                    refresh_baggage(baggage, prop_list, drug_list, material_list)
                                    tag = 1
                                    break
                                if (width - 200) / 3 + 100 < mouse_pos[0] < (width - 200) / 1.5 + 100 and 50 <\
                                        mouse_pos[1] < 450:
                                    streng_status = strengthen_prop(baggage.objects[chose_num])
                                    pygame.draw.rect(screen, CREAM, ((0, height - 145), (1100, 145)))
                                    if streng_status == 1:
                                        show_words('强化成功！', (width / 2, height - 100), font, RED)
                                    elif streng_status == 0:
                                        show_words('强化失败...', (width / 2, height - 100), font, RED)
                                    elif streng_status == 2:
                                        show_words('你的装备已经满级了！', (width / 2, height - 100), font, RED)
                                    elif streng_status == 3:
                                        show_words('没钱强化个毛啊！需要' + str(baggage.objects[chose_num].need_exp),
                                                   (width / 2, height - 100), font, RED)
                                    pygame.display.update()
                                    fclock.tick(fps)
                                    time.sleep(0.2)
                                if 100 < mouse_pos[0] < (width - 200) / 3 + 100 and 450 < mouse_pos[1] < 650:
                                    add_prop_character(character_list[0], baggage.objects[chose_num], 1)
                                    tag = 1
                                    break
                                elif (width - 200) / 3 + 100 < mouse_pos[0] < (width - 200) / 1.5 + 100 and 450 \
                                        < mouse_pos[1] < 650:
                                    add_prop_character(character_list[1], baggage.objects[chose_num], 2)
                                    tag = 1
                                    break
                                elif (width - 200) / 1.5 + 100 < mouse_pos[0] < width - 100 and 450 < mouse_pos[1] < 650:
                                    add_prop_character(character_list[2], baggage.objects[chose_num], 3)
                                    tag = 1
                                    break
                            if close_window() == 1:
                                break
            if tag == 1:
                flag = 1
                break
            pygame.display.update()
            fclock.tick(fps)
    if width - 180 < mouse_pos[0] < width - 120 and height - 60 < mouse_pos[1] < height and mouse_pressed[0] == 1:
        """achievement"""
        draw_window()
        while True:
            if close_window() == 1:
                break
    if (map_x_velocity > 0 and map_choice[0] < width - 10) or (map_x_velocity < 0 and map_choice[0] > 10):
        map_choice[0] += map_x_velocity
    if (map_y_velocity > 0 and map_choice[1] < height - 10) or (map_y_velocity < 0 and map_choice[1] > 10):
        map_choice[1] += map_y_velocity
    pygame.draw.circle(screen, BLACK, tuple(map_choice), 10)
    screen.blit(character_images, character_image)
    screen.blit(bag_images, bag_image)
    screen.blit(achievement_images, achievement_image)
    draw_map()
    level_choice = level_choose()
    pygame.display.update()
    fclock.tick(fps)
