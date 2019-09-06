import pygame
import time
import sys
import json
import os


BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREY = 128, 128, 128
size = width, height = 1080, 800  # size of the window
fps = 300  # frames per second for game
path = os.getcwd()
files = os.listdir(path)

pygame.init()
screen = pygame.display.set_mode(size)
fclock = pygame.time.Clock()

font = pygame.font.Font("ShenYunSuXinTi-2.ttf", 40)
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
pygame.display.set_caption("无名之地")


class Character:

    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.need_exp = 10

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

    def up_level(self, remainder):
        self.level += 1
        self.need_exp *= 1.5
        self.exp = remainder
        self.growth()

    def change_character_dic(self, contents):
        """add a character to contents"""
        dic = {'name': self.name, 'attack': self.attack, 'defence': self.defence, 'health': self.health, 'magic': self.magic,
               'critical': self.critical, 'speed': self.speed, 'luck': self.luck, 'insight': self.insight, 'level': self.level,
               'exp': self.exp, 'need_exp':self.need_exp, 'grow_attack': self.grow_attack, 'grow_defence': self.grow_defence,
               'grow_health': self.grow_health, 'grow_magic': self.grow_magic, 'grow_critical': self.grow_critical,
               'grow_speed': self.grow_speed, 'grow_luck': self.grow_luck, 'grow_insight': self.grow_insight}
        contents['characters'].append(dic)

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


def load_character(contents, characters_list):
    for i in contents['characters']:
        ch = Character(i['name'])
        ch.set_ability(i['attack'], i['defence'], i['health'], i['magic'], i['critical'], i['speed'], i['luck'],
                       i['insight'])
        ch.set_growth_ability(i['grow_attack'], i['grow_defence'], i['grow_health'], i['grow_magic'],
                              i['grow_critical'], i['grow_speed'], i['grow_luck'], i['grow_insight'])
        ch.exp = i['exp']
        ch.need_exp = i['need_exp']
        ch.level = i['level']
        characters_list.append(ch)


def load_file():
    """存档读取"""
    if not os.path.exists('fileSave.json'):
        with open('fileSave.json', 'a') as f:
            characters = []
            drug = []
            dic = {'plot': 0, 'money': 0, 'characters': characters, 'drug': drug}
            dic = json.dumps(dic, indent=4)
            f.write(dic)
    with open('fileSave.json', 'r') as file_object:
        contents = json.load(file_object)
    return contents


def down_file(contents):
    """保存存档"""
    contents = json.dumps(contents, indent=4)
    with open('fileSave.json', 'w') as file_object:
        """覆盖原存档"""
        file_object.write(contents)


def show_lines(lines, t):
    for i in range(len(lines)):
        texts = font.render(lines[i], True, WHITE)
        text = texts.get_rect()
        text.center = (width/2, 100 + i*200)
        screen.blit(texts, text)
        pygame.display.update()  # watch out its position
        time.sleep(t)

def show_words(words, coord):
    texts = font.render(words, True, WHITE)
    text = texts.get_rect()
    text.center = (coord[0], coord[1])
    screen.blit(texts, text)

def is_new(contents):
    new = contents["plot"]
    plot_1 = ["一觉醒来，你不知道自己身处何处，", "甚至自己是何许人也亦无从得知，世界犹如混沌般恍惚。", "徘徊于这谜一般的大陆上，你决定只身探索，寻找真相......"]
    if new == 0:
        contents["plot"] = 1
        """测试为0，实际为1"""
        screen.fill(BLACK)
        show_lines(plot_1, 2)
        pygame.display.update()
        fclock.tick(fps)
        down_file(contents)


content = load_file()
is_new(content)
character_list = []
load_character(content, character_list)
map_choice = [20, height - 20]
map_x_velocity = 0
map_y_velocity = 0

def draw_window():
    pygame.draw.rect(screen, WHITE, (100, 100, width - 200, height - 200), 5)
    """rect stand for (x,y,width,height)"""
    pygame.draw.rect(screen, WHITE, (width - 130, 100, 30, 30), 5)
    pygame.draw.line(screen, RED, (width - 125, 105), (width - 105, 125), 5)
    pygame.draw.line(screen, RED, (width - 105, 105), (width - 125, 125), 5)
    pygame.display.update()
    fclock.tick(fps)

def close_window():
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():  # magic move
        if event.type == pygame.QUIT:  # close the window
            sys.exit()
    if width - 130 < mouse_pos[0] < width - 100 and 100 < mouse_pos[1] < 130 and mouse_pressed[0] == 1:
        return 1


while(True):
    screen.fill(BLACK)
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
        pygame.draw.line(screen, WHITE, ((width - 200) / 3 + 100,  100), ((width - 200) / 3 + 100, height - 100), 5)
        pygame.draw.line(screen, WHITE, ((width - 200) / 1.5 + 105, 100), ((width - 200) / 1.5 + 105, height - 100), 5)
        pygame.draw.line(screen, GREY, (100, height / 2), (width - 100, height / 2), 5)
        show_words(character_list[0].name, ((width - 200) / 6 + 100, 150))
        show_words(character_list[1].name, ((width - 200) / 2 + 100, 150))
        show_words('攻击', ((width - 200) / 6 * 5 + 100, 170))
        draw_window()
        while(True):
            if close_window() == 1:
                break
    if (width - 120 < mouse_pos[0] < width - 60 and height - 60 < mouse_pos[1] < height and mouse_pressed[0] == 1):
        """bag"""
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
    pygame.draw.circle(screen, WHITE, tuple(map_choice), 10)
    screen.blit(character_images, character_image)
    screen.blit(bag_images, bag_image)
    screen.blit(achievement_images, achievement_image)
    pygame.display.update()
    fclock.tick(fps)

