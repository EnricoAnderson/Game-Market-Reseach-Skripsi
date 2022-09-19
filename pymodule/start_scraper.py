import os
import pickle
import sys
import module.skripsiutil as su
import module.scraper as s
from module.games import games

def file_delete(names):
    for name in names:
        if os.path.exists(name):
            os.remove(name)

filename = ['datakotorpopulerAugust2022.xlsx',
            'databersihpopulerAugust2022.xlsx',
            'populerAugust2022.json',
            'populerAugust2022.txt',
            'game_instance.pkl']

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            print("[ERROR] : Invalid Argument")
            exit()

        print("Scraping ", sys.argv[1], " pages")
        path = ".\\pymodule\\"
        file_delete([path+name for name in filename])
        g = games()
        s.scrapepopular(int(sys.argv[1]))
        g.getjson()
        g.convertfile()
        g.bersihindata()

        with open(path+'game_instance.pkl', 'wb') as outp:
            pickle.dump(g, outp, pickle.HIGHEST_PROTOCOL)
        
        print("[SUCCESS]")
    except (e):
        print("[ERROR] : ", e)