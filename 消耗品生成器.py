import json


class Drug:

    def __init__(self, name):
        self.name = name

    def drug_capacity(self,num = 0):
        self.size = 1
        self.num = num

    def drug_effect(self, attack, defence, health, speed, magic):
        self.attack = attack * self.size
        self.defence = defence * self.size
        self.health = health * self.size
        self.speed = speed * self.size
        self.magic = magic * self.size

    def change_drug_dic(self, drug_list):
        dic = {'name': self.name, 'attack': self.attack, 'defence': self.defence, 'health': self.health, 'magic': self.magic,
               'speed': self.speed, 'num': self.num}
        drug_list.append(dic)

    def create_drug(self, attack, defence, health, speed, magic, drug_list):
        self.drug_effect(attack, defence, health, speed, magic)
        self.change_drug_dic(drug_list)


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
        drug_list.append(dr)


def down_drug(contents, drug_list):
    contents['drug'] = drug_list
    

name = str(input("name: "))
with open("fileSave.json",'r') as f:
	contents = json.load(f)
dr = Drug(name)
dr.drug_capacity(0)
attack = int(input("attack: "))
defence = int(input("defence: "))
health = int(input("health: "))
speed = int(input("speed: "))
magic = int(input("magic: "))
dr.create_drug(attack, defence, health, speed, magic, contents['drug'])
with open("fileSave.json",'w') as f:
	contents = json.dumps(contents, indent=4)
	f.write(contents)


