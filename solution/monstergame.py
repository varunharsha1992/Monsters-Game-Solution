#!/usr/bin/env python
__author__ = 'rachid belaid'
import sys
import argparse
import re
import random

MAX_MOVE_TURN =10000;

DIRECTIONS = ['north','east','south','west']
directions_match_regexp = []
for direction in DIRECTIONS:
    directions_match_regexp.append(r"( %s = (?P<%s>(\w+([ ]?\-[ ]?\w+)*)))" %(direction,direction))

FILE_PATERN = re.compile(r"(?P<city>(\w+([ ]?\-[ ]?\w+)*))(%s){0,%s}"%('|'.join(directions_match_regexp),len(DIRECTIONS)))
DIRECTIONS = ['north','east','south','west']
LIMIT_MONSTER_BY_CITY = 1


class Map(object):

    def __init__(self,name=""):
        self.name = name
        self.list_city = {}
        self.list_monsters=[]


    def add_city(self,city):
        self.list_city[city] = city

    def delete_monster(self,monster):
        self.list_monsters.remove(monster)
        if not self.list_monsters :
            raise Map.AllMonstersDead()
        
    def delete_city(self,city):
        del self.list_city[city] 

    @staticmethod
    def opposite_direction(direction):
        try:
            return DIRECTIONS[(DIRECTIONS.index(direction)+2)%4]
        except Exception:
            return ''

    @staticmethod
    def get_random_direction(self):
        return DIRECTIONS[random.randint(0,3)]

    def move_monster(self,monster,to_city):
        """
        fonction to add monster the first time to a node or moving each turn
        """
        if monster.city :
            self.list_city[monster.city].remove_monster(monster)
        else :
            self.list_monsters.append(monster)

        try:
            self.list_city[to_city].add_monster(monster)
        except City.CityDestruction:
            print (' CITY %s HAS BEEN DESTROYED ,  NOOOOOOOO !!! ' % to_city).center(100, '=')
            for direction,neighbor in to_city.neighbors_generator():
                neighbor.delete_neighbor(to_city)
            self.delete_city(to_city)

    def get_random_city(self):
        return self.list_city.values()[random.randint(0, len(self.list_city)-1)]


    def __repr__(self):
        output = ''
        for city in self.list_city:
            output +=  repr(city) + '\n'
        return output

    class AllCityDestroyed(Exception):
        pass

    class AllMonstersDead(Exception):
        pass

class City(object):
    def __init__(self,name,map,**kwargs):
        self.name   = name
        self.monsters = []
        self.map    = map
        for direction in DIRECTIONS :
            if kwargs.get(direction,False) :
                setattr (self,direction,kwargs.get(direction,None))

    def __setitem__(self, key, value):
        """
        Because I m lazy shit , I want to be able to use bracket syntax
        """
        if key in DIRECTIONS:
          return self.__setattr__(key, value)
        else :
          raise  KeyError()

    def __getitem__(self, item):
        if item in DIRECTIONS:
          return self.__getattr__(item)
        else :
          raise  KeyError()

    def __getattribute__(self, name):
        if name in DIRECTIONS :
            city = object.__getattribute__(self, name )
            if city :
                try :
                    return self.map.list_city[object.__getattribute__(self, name )]
                except KeyError:
                    return object.__getattribute__(self, name )
            else :
                raise AttributeError()

        else :
           return object.__getattribute__(self, name )
            
    def __repr__(self):
        output = self.name
        for direction in DIRECTIONS:
            neighbor = getattr(self, direction,False)
            if neighbor :
                output+= " %s=%s" %(direction,neighbor)
        return output

    def delete_neighbor(self,city):
        for direction, neighbor in self.neighbors_generator():
            if neighbor == city :
                delattr(self,direction)
        return 

    def neighbors_generator(self):
        for direction in DIRECTIONS:
            if getattr(self,direction,False):
                yield (direction,self.map.list_city[getattr(self,direction)])

    def neighbors(self):
        l = []
        for direction,city in self.neighbors_generator():
            l.append(city)
        return l

    def add_monster(self,new_monster):
        new_monster.city = self
        self.monsters.append(new_monster)
        if len(self.monsters) > LIMIT_MONSTER_BY_CITY :
            print (' FIGHT : MONSTERS %s are fighting ' % self.monsters).center(100, '=')
            for monster in self.monsters:
                self.map.delete_monster(monster)
            raise City.CityDestruction()

    def remove_monster(self,monster):
        self.monsters.remove(monster)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __cmp__(self, other):
        if str(self) == str(other):
            return 0
        elif str(self) > str(other):
            return 1
        else :
            return -1

    def __hash__(self):
        return hash(self.name)

    class CityDestruction(Exception):
        pass

class Monster(object):

    def __init__(self,name):
        self.name = name
        self.city = None

    def __cmp__(self, other):
        if str(self) == str(other):
            return 0
        elif str(self) > str(other):
            return 1
        else :
            return -1
    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)




class MonsterGame():
    def initialize(self,input,output,nb_monsters=1):
        self.turn = 0
        self.output = output
        self.map = Map()
        for line in input :
           m = FILE_PATERN.match(line)
           if not m.group('city') :
               continue
           kwargs= {}
           for direction in DIRECTIONS :
               if m.group(direction):
                   kwargs[direction]=m.group(direction)
           city = City( m.group('city'),self.map,**kwargs)
           self.map.add_city(city)

        for i in range(nb_monsters):
           self.map.move_monster(Monster(str(i)),self.map.get_random_city())


    def play(self):
        for monster in self.map.list_monsters :
            neighbors = monster.city.neighbors()
            if neighbors:
                self.map.move_monster(monster,neighbors[random.randint(0,len(neighbors)-1)])
        self.turn += 1
        if self.turn > MAX_MOVE_TURN :
            raise  MonsterGame.LimitTurnReached()

    def end(self):
        self.output.write(repr(self.map))

    class LimitTurnReached(Exception):
        pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monster Game')
    parser.add_argument('monsters', metavar='N', type=int, nargs='?',
                       help='The number of monster that you want to rush on the map. It need to be an integer')
    parser.add_argument('--map', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('--output', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)
    args = parser.parse_args()
    game = None
    game = MonsterGame()
    try :
        game.initialize(input=args.map,output=args.output,nb_monsters=args.monsters)
        while True:
            print (' ROUND %s : START ' % (game.turn+1)).center(100, '=')
            game.play()
            print (' ROUND %s : END ' % game.turn).center(100, '=')
    except MonsterGame.LimitTurnReached :
        print ' GAME OVER : LIMIT OF MONSTERS MOVE REACHED '.center(100, '=')
    except Map.AllCityDestroyed :
        print ' GAME OVER : ALL CITIES DESTROYED '.center(100, '=')
    except Map.AllMonstersDead :
        print ' GAME OVER : ALL MONSTERS DEAD '.center(100, '=')
    finally:
        game.end()