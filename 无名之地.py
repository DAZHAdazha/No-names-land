import pygame
import time
import sys
import json
import os
import re

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREY = 128, 128, 128
CREAM = 230, 230, 230
size = width, height = 1100, 800  # size of the window
fps = 300  # frames per second for game
path = os.getcwd()
files = os.listdir(path)

pygame.init()
screen = pygame.display.set_mode(size)
fclock = pygame.time.Clock()

font = pygame.font.Font("ShenYunSuXinTi-2.ttf", 32)
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
material_images = pygame.image.load("./image/材料.png")
pygame.display.set_caption("无名之地")


class Material:
    def __init__(self, name):
        self.name = name

    def create_new_material(self, attack, defence, health, magic, critical, speed, luck, num, value):
            self.attack = attack
            self.defence = defence
            self.health = health
            self.magic = magic
            self.critical = critical
            self.speed = speed
            self.luck = luck
            self.num = num
            self.value = value


class Prop:
    def __init__(self, name):
        self.name = name

    def create_new_prop(self, attack, defence, health, magic, critical, speed, luck, grow_attack, grow_defence,
                        grow_health, grow_magic, grow_critical, grow_speed, grow_luck, value, pos, level=1,
                        exp=0, need_exp=10, enchant_time=5, is_wear=False):
        """type include 1,2,3,4,5,6"""
        """-1 = 法杖， 1 = 剑， 0 = 弓箭, 2 = helmet, 3 = armor, 4 = shoes, 5 = ornament, 6 = title"""
        #  is_wear = True/False
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

    def up_level(self, exp):
        self.exp += exp
        while self.exp >= self.need_exp:
            self.value += 1
            self.level += 1
            self.exp = self.exp - self.need_exp
            self.need_exp *= 1.5
            self.attack += self.grow_attack
            self.defence += self.grow_defence
            self.health += self.grow_health
            self.magic += self.grow_magic
            self.critical += self.grow_critical
            self.speed += self.grow_speed
            self.luck += self.grow_luck


class Baggage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.objects = []
        self.amount = 0


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
            self.need_exp *= 1.5
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
        file_object.write(contents)


def make_lists(contents, props_list, drug_list, characters_list, materials_list):
    """存档变列表"""
    for i in contents['characters']:
        ch = Character(i['name'])
        ch.create_new_character(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'], i['luck'],
                                i['insight'], i['grow_attack'], i['grow_defence'], i['grow_health'], i['grow_magic'],
                                i['grow_critical'], i['grow_speed'], i['grow_luck'], i['grow_insight'], i['level'],
                                i['exp'], i['need_exp'], i['position'])
        characters_list.append(ch)
    for i in contents['props']:
        prop = Prop(i['name'])
        prop.create_new_prop(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'],i['luck'],
                             i['grow_attack'], i['grow_defence'], i['grow_health'], i['grow_magic'], i['grow_critical'],
                             i['grow_speed'], i['grow_luck'], i['value'], i['pos'], i['level'], i['exp'],
                             i['need_exp'], i['enchant_time'], i['is_wear'])
        props_list.append(prop)
    for i in contents['drug']:
        drug = Drug(i['name'])
        drug.create_new_drug(i['attack'], i['defence'], i['health'], i['speed'], i['magic'], i['num'], i['value'])
        drug_list.append(drug)
    for i in contents['materials']:
        material = Material(i['name'])
        material.create_new_material(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'],
                                     i['luck'], i['num'], i['value'])
        materials_list.append(material)


def show_lines(lines, t):
    for i in range(len(lines)):
        texts = font.render(lines[i], True, BLACK)
        text = texts.get_rect()
        text.center = (width/2, 100 + i*200)
        screen.blit(texts, text)
        pygame.display.update()  # watch out its position
        time.sleep(t)


def show_words(words, coord):
    texts = font.render(words, True, BLACK)
    text = texts.get_rect()
    text.center = (coord[0], coord[1])
    screen.blit(texts, text)


def show_attr(character, coord):
    """change 'attack...' to '攻击' """
    show_words('经验:' + str(character.exp) + '/' + str(character.need_exp), (coord[0] + 72, coord[1]))
    show_words('攻击:' + str(character.attack), (coord[0], coord[1] + 50))
    show_words('防御:' + str(character.defence), (coord[0] + 145, coord[1] + 50))
    show_words('生命:' + str(character.health), (coord[0], coord[1] + 100))
    show_words('魔法:' + str(character.magic), (coord[0] + 145, coord[1] + 100))
    show_words('暴击:' + str(character.critical), (coord[0], coord[1] + 150))
    show_words('速度:' + str(character.speed), (coord[0] + 145, coord[1] + 150))
    show_words('幸运:' + str(character.luck), (coord[0], coord[1] + 200))
    show_words('洞视:' + str(character.insight), (coord[0] + 145, coord[1] + 200))
    show_words('等级:' + str(character.level), (coord[0], coord[1] + 250))
    """one more attr"""


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
               'is_wear': i.is_wear, 'enchant_time': i.enchant_time}
        content['props'].append(dic)
    for i in materials_list:
        dic = {'name': i.name, 'attack': i.attack, 'defence': i.defence, 'health': i.health, 'critical': i.critical,
               'magic': i.magic, 'speed': i.speed, 'value': i.value, 'num': i.num, 'luck': i.luck}
        content['materials'].append(dic)


def add_prop_character(character, prop):
    """人物装备道具"""
    if prop.pos in character.position or prop.is_wear:
        return False
    else:
        character.position.append(prop.pos)
        prop.is_wear = True
        character.attack += prop.attack
        character.defence += prop.defence
        character.health += prop.health
        character.magic += prop.magic
        character.critical += prop.critical
        character.speed += prop.speed
        character.luck += prop.luck


def remove_prop_character(character, prop):
    """移除装备"""
    character.position.remove(prop.pos)
    prop.is_wear = False
    character.attack -= prop.attack
    character.defence -= prop.defence
    character.health -= prop.health
    character.magic -= prop.magic
    character.critical -= prop.critical
    character.speed -= prop.speed
    character.luck -= prop.luck


def strengthen_prop(prop1, prop2):
    """强化装备"""
    prop1.up_level(prop2.value)


def enchant_prop(prop, material):
    """附魔装备"""
    prop.enchant_time -= 1
    prop.attack += material.attack
    prop.defence += material.defence
    prop.health += material.health
    prop.magic += material.magic
    prop.critical += material.critical
    prop.speed += material.speed
    prop.luck += material.luck
    prop.value += material.value//2


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
            content['baggage'] = baggage.amount #  put into fileSave
            sys.exit()
    if width - 130 < mouse_pos[0] < width - 100 and 50 < mouse_pos[1] < 80 and mouse_pressed[0] == 1:
        return 1


def show_object(baggage):
    item_list_image = []
    j = 0
    for i in baggage.objects:
        if Prop == type(i):
            if i.pos == -1:
                item_list_image.append(wand_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(wand_images, item_list_image[j])
            elif i.pos == 0:
                item_list_image.append(bow_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(bow_images, item_list_image[j])
            elif i.pos == 1:
                item_list_image.append(sword_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(sword_images, item_list_image[j])
            elif i.pos == 2:
                item_list_image.append(helmet_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(helmet_images, item_list_image[j])
            elif i.pos == 3:
                item_list_image.append(armor_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(armor_images, item_list_image[j])
            elif i.pos == 4:
                item_list_image.append(shoe_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(shoe_images, item_list_image[j])
            elif i.pos == 5:
                item_list_image.append(ring_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(ring_images, item_list_image[j])
            elif i.pos == 6:
                item_list_image.append(title_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(title_images, item_list_image[j])
        elif Drug == type(i):
            if i.name == '大红药':
                item_list_image.append(big_health_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(big_health_images, item_list_image[j])
            elif i.name == '小红药':
                item_list_image.append(small_health_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(small_health_images, item_list_image[j])
            elif i.name == '大蓝药':
                item_list_image.append(big_magic_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(big_magic_images, item_list_image[j])
            elif i.name == '小蓝药':
                item_list_image.append(small_magic_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(small_magic_images, item_list_image[j])
            elif i.name == '小攻击药':
                item_list_image.append(small_attack_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(small_attack_images, item_list_image[j])
            elif i.name == '大攻击药':
                item_list_image.append(big_attack_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(big_attack_images, item_list_image[j])
        elif Material == type(i):
            item_list_image.append(material_images.get_rect())
            item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
            screen.blit(material_images, item_list_image[j])
        show_words(i.name, (j % 6 * 150 + 180, j // 6 * 150 + 150))
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


def translate(str):
    translator = {'name': '名称', 'attack': '攻击', 'defence': '防御', 'health': '生命', 'magic': '魔法', 'critical': '暴击',
                  'speed': '速度', 'luck': '幸运', 'level': '等级', 'num': '数量', 'enchant_time': '可附魔次数',
                  'value': '价格'}  # time change
    return translator[str]


def sale_obj(baggage, obj, contents):
    """卖出物品"""
    contents['money'] += obj.value  # value是物品的价值
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
    show_words(character_list[0].name, ((width - 200) / 6 + 100, 100))
    show_words(character_list[1].name, ((width - 200) / 2 + 100, 100))
    show_words(character_list[2].name, ((width - 200) / 6 * 5 + 100, 100))
    show_attr(character_list[0], ((width - 200) / 6 + 20, height / 2 - 20))
    show_attr(character_list[1], ((width - 200) / 2 + 20, height / 2 - 20))
    show_attr(character_list[2], ((width - 200) / 6 * 5 + 20, height / 2 - 20))
    draw_window()


def refresh_baggage(baggage, props_list, drug_list, materials_list):
    """列表载入背包"""
    baggage.objects = props_list[:] + drug_list[:] + materials_list[:]
    baggage.amount = len(baggage.objects)


content = load_file()
baggage = Baggage(content['baggage'])
is_new(content)
character_list = []
drugs_list = []
material_list = []
prop_list = []
make_lists(content,  prop_list, drugs_list, character_list, material_list)
refresh_baggage(baggage, prop_list, drugs_list, material_list)
map_choice = [20, height - 20]
map_x_velocity = 0
map_y_velocity = 0


while(True):
    screen.fill(CREAM)
    for event in pygame.event.get():  # event list
        if event.type == pygame.QUIT:  # close the window
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # event of press the key
            if event.key == pygame.K_d:
                map_x_velocity = 1
            if event.key == pygame.K_s:
                map_y_velocity = 1
            if event.key == pygame.K_a:
                map_x_velocity = -1
            if event.key == pygame.K_w:
                map_y_velocity = -1
        elif event.type == pygame.KEYUP:  # event of release the key
            if event.key == pygame.K_d:
                map_x_velocity = 0
            if event.key == pygame.K_s:
                map_y_velocity = 0
            if event.key == pygame.K_a:
                map_x_velocity = 0
            if event.key == pygame.K_w:
                map_y_velocity = 0
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    '''return tuple object, which [0] represent left key, [1] for middle, [2] for right'''
    if width - 60 < mouse_pos[0] < width and height - 60 < mouse_pos[1] < height and mouse_pressed[0] == 1:
        draw_character()
        draw_window()
        while True:
            if close_window() == 1:
                break
    if width - 120 < mouse_pos[0] < width - 60 and height - 60 < mouse_pos[1] < height and mouse_pressed[0] == 1:
        """bag"""

        for i in range(3):
            pygame.draw.line(screen, BLACK, (100, 200 + i * 150), (width - 100, 200 + i * 150), 4)
        for i in range(5):
            pygame.draw.line(screen, BLACK, (250 + i * 150, 50), (250 + i * 150, height - 150), 4)

        ''' put into function'''
        props_num = show_object(baggage)
        draw_window()
        while True:
            mouse_pressed = pygame.mouse.get_pressed()
            cur_word_1 = ''
            cur_word_2 = ''
            if mouse_pressed[2] == 1:
                chose_num = click_on_props()
                if 0 <= chose_num < props_num:
                    sale_obj(baggage, baggage.objects[chose_num], content)
                    time.sleep(0.2)  # test
            elif mouse_pressed[0] == 1:
                chose_num = click_on_props()
                if 0 <= chose_num < props_num:
                    pygame.draw.rect(screen, CREAM, ((0, height - 145), (1100, 800)),)
                    word_len = 0
                    obj = vars(baggage.objects[chose_num])
                    for i in obj:
                        if not re.findall('(^grow|^need|pos|exp|is_wear)', str(i)):
                            if obj[i] != 0:
                                if word_len < 6:
                                    cur_word_1 += translate(str(i)) + ':' + str(obj[i]) + ' '
                                    word_len += 1
                                else:
                                    cur_word_2 += translate(str(i)) + ':' + str(obj[i]) + ' '
                show_words(cur_word_1, (width / 2, height - 120))
                show_words(cur_word_2, (width / 2, height - 70))
            if close_window() == 1:
                refresh_lists(baggage, prop_list, drugs_list, material_list)
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
    pygame.display.update()
    fclock.tick(fps)
