import pygame
import time
import sys
import json
import os

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
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
character_images = pygame.image.load("角色.png")
character_image = character_images.get_rect()
character_image = character_image.move(width - 60, height - 60)
bag_images = pygame.image.load("背包.png")
bag_image = bag_images.get_rect()
bag_image = bag_image.move(width - 120, height - 60)
achievement_images = pygame.image.load("成就.png")
achievement_image = achievement_images.get_rect()
achievement_image = achievement_image.move(width - 180, height - 60)
shoe_images = pygame.image.load("鞋子.png")
sword_images = pygame.image.load("剑.png")
helmet_images = pygame.image.load("头盔.png")
ring_images = pygame.image.load("戒指.png")
armor_images = pygame.image.load("护甲.png")
wand_images = pygame.image.load("法杖.png")
bow_images = pygame.image.load("弓箭.png")
title_images = pygame.image.load("称号.png")
pygame.display.set_caption("无名之地")


class Prop:

    def __init__(self, name, pos):
        """type include 1,2,3,4,5,6"""
        """1 = weapon, 2 = helmet, 3 = armor, 4 = shoes, 5 = ornament, 6 = title"""
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


class Drug:

    def __init__(self, name):
        self.name = name

    def drug_capacity(self, drug_size=5, num=0):
        self.drug_size = drug_size
        self.num = num

    def drug_effect(self, attack, defence, health, speed, magic):
        self.attack = attack * self.drug_size
        self.defence = defence * self.drug_size
        self.health = health * self.drug_size
        self.speed = speed * self.drug_size
        self.magic = magic * self.drug_size

    def change_drug_dic(self, drug_list):
        dic = {'name': self.name, 'attack': self.attack, 'defence': self.defence, 'health': self.health,
               'magic': self.magic,
               'speed': self.speed, 'num': self.num}
        drug_list.append(dic)

    def alter_drug(self, contents):
        """alter a drug in contents"""
        for i in contents['drug']:
            if i['name'] == self.name:
                i['num'] = self.num

    def create_drug(self, attack, defence, health, speed, magic, num, drug_size, drug_list):
        self.drug_capacity(drug_size, num)
        self.drug_effect(attack, defence, health, speed, magic)
        self.change_drug_dic(drug_list)




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
        dic = {'name': self.name, 'attack': self.attack, 'defence': self.defence, 'health': self.health,
               'magic': self.magic,'critical': self.critical, 'speed': self.speed, 'luck': self.luck,
               'insight': self.insight, 'level': self.level,'exp': self.exp, 'need_exp':self.need_exp,
               'grow_attack': self.grow_attack, 'grow_defence': self.grow_defence,'grow_health': self.grow_health,
               'grow_magic': self.grow_magic, 'grow_critical': self.grow_critical,'grow_speed': self.grow_speed,
               'grow_luck': self.grow_luck, 'grow_insight': self.grow_insight, 'position': self.position}
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
        ch.set_ability(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'], i['luck'],
                       i['insight'])
        ch.set_growth_ability(i['grow_attack'], i['grow_defence'], i['grow_health'], i['grow_magic'],
                              i['grow_critical'],i['grow_speed'], i['grow_luck'], i['grow_insight'])
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


def use_drug(drug, character):
    character.cur_ability(drug.attack, drug.defence, drug.health, drug.magic, drug.speed)
    drug.num -= 1


def get_drug(drug, num=1):
    drug.num += num


def load_drug(contents, drug_list):
    for i in contents['drug']:
        dr = Drug(i['name'])
        dr.health = i['health']
        dr.speed = i['speed']
        dr.magic = i['magic']
        dr.defence = i['defence']
        dr.attack = i['attack']
        dr.num = i['num']
        drug_list.append(dr)


def down_drug(contents, drug_list):
    for j in drug_list:
        j.alter_drug(contents)


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


def draw_window():
    pygame.draw.rect(screen, BLACK, (100, 50, width - 200, height - 200), 5)
    """rect stand for (x,y,width,height)"""
    pygame.draw.rect(screen, BLACK, (width - 130, 50, 30, 30), 5)
    pygame.draw.line(screen, RED, (width - 125, 55), (width - 105, 75), 5)
    pygame.draw.line(screen, RED, (width - 105, 55), (width - 125, 75), 5)
    pygame.display.update()
    fclock.tick(fps)


def close_window():
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():  # magic move
        if event.type == pygame.QUIT:  # close the window
            sys.exit()
    if width - 130 < mouse_pos[0] < width - 100 and 50 < mouse_pos[1] < 80 and mouse_pressed[0] == 1:
        return 1


content = load_file()
is_new(content)
character_list = []
drug_list = []
load_characters(content, character_list)
load_drug(content, drug_list)
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
    if (width - 60 < mouse_pos[0] < width and height - 60 < mouse_pos[1] < height and mouse_pressed[0] == 1):
        """character"""
        pygame.draw.line(screen, GREY, (100, height / 2 - 50), (width - 100, height / 2 - 50), 5)
        pygame.draw.line(screen, BLACK, ((width - 200) / 3 + 100,  50), ((width - 200) / 3 + 100, height - 150), 5)
        pygame.draw.line(screen, BLACK, ((width - 200) / 1.5 + 105, 50), ((width - 200) / 1.5 + 105, height - 150), 5)

        """ merge into function"""
        show_words(character_list[0].name, ((width - 200) / 6 + 100, 100))
        show_words(character_list[1].name, ((width - 200) / 2 + 100, 100))
        show_words(character_list[2].name, ((width - 200) / 6 * 5 + 100, 100))
        show_attr(character_list[0], ((width - 200) / 6 + 20, height / 2 - 20))
        show_attr(character_list[1], ((width - 200) / 2 + 20, height / 2 - 20))
        show_attr(character_list[2], ((width - 200) / 6 * 5 + 20, height / 2 - 20))
        draw_window()
        while(True):
            if close_window() == 1:
                break
    if (width - 120 < mouse_pos[0] < width - 60 and height - 60 < mouse_pos[1] < height and mouse_pressed[0] == 1):
        """bag"""
        for i in range(3):
            pygame.draw.line(screen, BLACK, (100, 200 + i * 150), (width - 100, 200 + i * 150), 5)
        for i in range(5):
            pygame.draw.line(screen, BLACK, (250 + i * 150, 50), (250 + i * 150, height - 150), 5)

        ''' put into function'''
        item_list_image = []
        j = 0
        for i in content['props']:
            if i['pos'] == -1:
                item_list_image.append(wand_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(wand_images, item_list_image[j])
            elif i['pos'] == 0:
                item_list_image.append(bow_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(bow_images, item_list_image[j])
            elif i['pos'] == 1:
                item_list_image.append(sword_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(sword_images, item_list_image[j])
            elif i['pos'] == 2:
                item_list_image.append(helmet_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(helmet_images, item_list_image[j])
            elif i['pos'] == 3:
                item_list_image.append(armor_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(armor_images, item_list_image[j])
            elif i['pos'] == 4:
                item_list_image.append(shoe_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(shoe_images, item_list_image[j])
            elif i['pos'] == 5:
                item_list_image.append(ring_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(ring_images, item_list_image[j])
            elif i['pos'] == 6:
                item_list_image.append(title_images.get_rect())
                item_list_image[j] = item_list_image[j].move(j % 6 * 150 + 150, j // 6 * 150 + 70)
                screen.blit(title_images, item_list_image[j])
            j += 1
            draw_window()
        while (True):
            if close_window() == 1:
                break
    if (width - 180 < mouse_pos[0] < width - 120 and height - 60 < mouse_pos[1] < height and mouse_pressed[0] == 1):
        """achievement"""
        draw_window()
        while (True):
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
