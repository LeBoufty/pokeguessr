import json
from random import randint, choice, shuffle

filename = 'pokedex_raw_array.json'
challenges = ['typing', 'stat/hp', 'stat/attack', 'stat/defense', 'stat/special-attack', 'stat/special-defense', 'stat/speed',
              'bst', 'height', 'weight', 'first-letter', 'abilities', 'number']

with open(filename) as file:
    pokedex = json.load(file)
    print(type(pokedex))

def get_random_number() -> int:
    return randint(0, len(pokedex)-1)

def get_name(n) -> str:
    return pokedex[n]['name']

def get_image(n) -> str:
    return f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{n+1}.png"

def get_index(pokemon) -> int:
    i = 0
    while i < len(pokedex) and pokedex[i]['name'] != pokemon: i += 1
    if i != len(pokedex): return i
    else: return None

def get_typing(n) -> list:
    typing = pokedex[n]['types']
    return [i['name'] for i in typing]

def stat_to_index(stat) -> int:
    stats = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    return stats.index(stat)

def index_to_stat(i) -> str:
    stats = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
    return stats[i]

def get_stat(n, stat) -> int:
    if (type(stat)) == str: stat = stat_to_index(stat)
    return pokedex[n]['stats'][stat]['base_stat']

def get_random_stat(n) -> tuple:
    stat = randint(0,5)
    return get_stat(n,stat), index_to_stat(stat)

def get_bst(n) -> int:
    bst = 0
    for i in range(6): bst += get_stat(n, i)
    return bst

def get_height(n) -> float:
    return round(pokedex[n]['height']/100, 1)

def get_weight(n) -> float:
    return round(pokedex[n]['weight']/10, 1)

def get_abilities(n) -> list:
    abilities = pokedex[n]['abilities']
    return [i['name'] for i in abilities]

class Game():
    def __init__(self, player:str, pokemon:int):
        self.player = player
        self.pokemon = pokemon
        self.pokename = get_name(pokemon)
        self.round = 0
        self.challenges = challenges[:]
        shuffle(self.challenges)
        self.gameover = len(self.challenges)
        self.over = False
    
    def guess(self, mon):
        if type(mon) == str: mon = get_index(mon)
        return mon == self.pokemon
    
    def next_round(self):
        if self.round >= self.gameover or self.over:
            self.over = True
            return f'Game Over ! The Pokémon was {self.pokename.capitalize()}. Use **!start** to start a new game.'
        topic = self.challenges[self.round]
        self.round += 1
        if topic == 'typing':
            return '**Type :** ' + ' - '.join(get_typing(self.pokemon))
        if topic == 'bst':
            return '**BST :** ' + str(get_bst(self.pokemon))
        if topic == 'height':
            return '**Height :** ' + str(get_height(self.pokemon)) + 'm'
        if topic == 'weight':
            return '**Weight :** ' + str(get_weight(self.pokemon)) + 'kg'
        if topic == 'first-letter':
            return '**Starts with :** ' + get_name(self.pokemon)[0].upper()
        if topic == 'abilities':
            return '**Abilities :** ' + ', '.join(get_abilities(self.pokemon))
        if topic == 'number':
            return '**Pokédex ID :** ' + str(self.pokemon+1)
        if topic.split('/')[0] == 'stat':
            stat = topic.split('/')[1]
            index = stat_to_index(stat)
            return f'**Base {stat.capitalize()} :** ' + str(get_stat(self.pokemon, index))
