import pickle
import module.skripsiutil as su
import module.scraper as s
from module.games import games

with open('game_instance.pkl', 'rb') as inp:
    g = pickle.load(inp)

print(g.getparameter())