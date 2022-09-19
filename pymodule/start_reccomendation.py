import pickle
import sys
import os
import json
import pandas as pd
import module.skripsiutil as su
import module.scraper as s
from module.games import games

g = None
dfrevenue = None
totalrevenue = ""
listgenremining = []
dfgenre = None
path = ".\\pymodule\\"

def file_delete(names):
    for name in names:
        if os.path.exists(name):
            os.remove(name)

def init():
    global g
    global dfrevenue
    global totalrevenue
    global listgenremining
    global dfgenre

    with open(path+'game_instance.pkl', 'rb') as inp:
        g = pickle.load(inp)

    dfrevenue = su.getrevenuesorted(g.revenue)
    _, totalrevenue = su.gettotalrev(dfrevenue)
    listgenrelow = su.lowergenretxt(g.getparameter())
    dfgenre = su.makedfGenre(g.getid(),listgenrelow)

def save_top10revenue(g):
    global dfrevenue
    global totalrevenue

    file_delete([path+"genretop10.json"])
    with open(path+"genretop10.json", "w") as outfile:
        json.dump({
            'genre': dfrevenue.index.tolist(),
            'revenue': dfrevenue['Revenue'].tolist(),
            'total': totalrevenue}, 
            outfile)

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    arg_len = len(sys.argv)
    try:
        if arg_len != 5:
            print("Argument must be exist for reccomendation!")
        else:
            init()
            
            genre_input = su.splitinput(sys.argv[1])
            supp_input = float(sys.argv[2])
            conf_input = float(sys.argv[3])
            pnj_input = float(sys.argv[4])
            # print("The input was : ", genre_input)

            listgenremining = su.lowergenreinput(dfgenre, genre_input)
            # print("The filtered genres are : ", listgenremining)

            save_top10revenue(g)

            #nanti waktu jadi aplikasi harus bikin bisa input dari user juga
            strongrule, freqitem = su.startmining(listgenremining, supp_input, conf_input)
            rules, listrules = su.urutberdasarkanrevenue(dfrevenue, genre_input, strongrule)
            rekomendasi = su.ubahjadirekomendasijumlah(listrules, pnj_input)
            dfrekomendasi = su.ubahjadidataframe(rekomendasi)
            print(rekomendasi)

            with open(path+"rekomendasi.json", "w") as outfile:
                json.dump(rekomendasi, outfile, cls=SetEncoder)
            
            print("[SUCCESS] Succesfully process data!")
    except:
        print("[ERROR] : ", error)


