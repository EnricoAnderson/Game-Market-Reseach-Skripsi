import pandas as pd
from numerize import numerize as num
# import plotly.express as px
from fpgrowth_py import fpgrowth
import math
import tqdm
# import plotly.graph_objects as go
pathdir = ".\\pymodule\\"
def splitinput(genrein):

    genrein = genrein.lower()

    genrein = genrein.replace(" ", "").replace("-", "")
    genrein = genrein.split(",")

    return genrein


def getrevenuesorted(revenue):
    df = pd.DataFrame.from_dict(revenue, orient='index')
    df.columns = ["Revenue"]
    df = df.rename_axis('Genre')

    df = df.sort_values(by="Revenue", ascending=False)
    df.to_csv(pathdir+'datarev.csv')
    return df


def gettotalrev(dataframerevenue):
    tot = list(dataframerevenue["Revenue"])
    totalrevenue = 0

    for x in tot:
        totalrevenue += x

    totalrevenue = num.numerize(totalrevenue)

    return tot, totalrevenue


def showgraphtoprevenue(totalrevenue, dataframerevenue):
    tit = "Total Revenue " + "$" + str(totalrevenue)
    fig = px.bar(dataframerevenue[0:10], y='Revenue', title="Top 10 Genre by Revenue",
                 labels={"Genre": tit, "Revenue": "Revenue ($)"}, )
    fig.show()


def lowergenretxt(listgenre):
    paramlower = []
    for x in listgenre:
        x = [s.lower().replace(" ", "").replace("-", "") for s in x]
        paramlower.append(x)

    return paramlower


def makedfGenre(listid, listgenrelow):
    dic = {"appid": listid, "genre": listgenrelow}
    dfGenre = pd.DataFrame(dic)

    dfGenre.to_csv(pathdir+'datainput.csv')
    return dfGenre

def lowergenreinput(dataframegenre, listinputawal):
    paramMining = []

    for x, genrelow in dataframegenre.iterrows():
        if set(listinputawal).issubset(genrelow["genre"]):
            #         print(genrelow["appid"])
            paramMining.append(genrelow["genre"])

    return paramMining


def startmining(listgenremining, minsupratio, minconfidence):

    freqItemSet, rules = fpgrowth(listgenremining, minSupRatio=minsupratio, minConf=minconfidence)
    # print("Terbentuk " + str(len(rules)) + " Strong rules")

    return rules, freqItemSet

def urutberdasarkanrevenue(dataframerevenue, listinputawal, liststrongrule):

    genrelow = list(dataframerevenue.index.str.lower())
    listhasilurut = []
    temp = []
    pembanding = []

    with tqdm.tqdm(range(len(genrelow))) as progressbar:

        for x in genrelow:
            pembanding.clear()
            pembanding = listinputawal.copy()
            pembanding.append(x)
            for y in liststrongrule:
                dibanding = y[0].union(y[1])
                if set(pembanding).issubset(dibanding):
                    #                 print(pembanding)
                    temp.clear()
                    temp.append(y)
                    #                 print(temp)
                    if not (any(z in temp for z in listhasilurut)):
                        listhasilurut.append(y)
                else:
                    pass
            progressbar.update(1)


    dfoutput = pd.DataFrame(listhasilurut, columns=["antecendents", "consequent", "support"])

    return dfoutput, listhasilurut

def urutkanberdasarkantop10(listinputawal, dataframerevenue, listhasilurut):
    inp = []
    genrelow = list(dataframerevenue.index)
    inp = listinputawal.copy()
    inp = inp + genrelow[:10]
    # print(inp)
    listhasiltop10 = []
    len_inp = len(inp) - len(listinputawal)

    for y in range(len_inp):
        for x in listhasilurut:
            if set(inp).issubset(x[0].union(x[1])):
                listhasiltop10.append(x)
        #             print("x =", x)
        inp.pop()

    # print(len(temp2))
    dftop10 = pd.DataFrame(listhasiltop10, columns=["antecendents", "consequent", "support"])
    return dftop10, listhasiltop10


def ubahjadirekomendasi(listhasilmining):
    temp_rekomendasi = []

    for x in listhasilmining:
        temp_rekomendasi.append(x[0].union(x[1]))

    result = []
    for item in temp_rekomendasi:
        if item not in result:
            result.append(item)

    return result

def ubahjadirekomendasijumlah(listhasilmining, panjangrekomendasi):
    temp_rekomendasi = []

    for x in listhasilmining:
        temp_rekomendasi.append(x[0].union(x[1]))

    result = []

    if panjangrekomendasi != 0:
        for item in temp_rekomendasi:
            if item not in result and len(item) <= panjangrekomendasi:
                result.append(item)
    else:
        for item in temp_rekomendasi:
            if item not in result:
                result.append(item)

    return result

def tampilkangraphbanding(dataframerevenue, listresult, inputnomorgraph):
    df = dataframerevenue
    result = listresult
    df['color'] = "blue"

    dft = df.index.str.lower()
    dft = dft.str.strip()
    dft = dft.str.replace("-", "")
    df.loc[dft.isin(list(result[inputnomorgraph])), "color"] = "gold"

    fig = go.Figure(
        go.Bar(x=df.index,
               y=df['Revenue'],
               marker={'color': df['color']})
    )
    fig.show()

def ubahjadidataframe(input):
    dfrekomendasi = pd.DataFrame({"Rekomendasi": input})

    return dfrekomendasi