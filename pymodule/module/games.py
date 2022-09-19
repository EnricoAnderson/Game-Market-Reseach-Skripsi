import math

import requests
import os.path
import tqdm
import xlsxwriter
import module.scraper as s
import numpy as np
import re
import datetime as dt
import pandas as pd


class games:
    
    def __init__(self):
        self.now = self.gettime()
        self.revenue = {}
        self.path = ".\\pymodule\\"

        self.namatxt = "populer" + self.now + ".txt"

        self.namajson = "populer" + self.now + ".json"

        self.namadatakotor = "datakotorpopuler"+ self.now + ".xlsx"

        self.namadatabersih = "databersihpopuler"+ self.now +".xlsx"

        self.parameter = []

        self.appid = []

    def gettime(self):
        date = dt.datetime.now()
        return date.strftime("%B%Y")

    def getid(self):
        return self.appid

    def addparameter(self, parameter):
        self.parameter.append(parameter)

    def addappid(self, id):
        self.appid.append(id)

    def getparameter(self):
        return self.parameter

    # input disini appid

    def requestjson(self, lineappid):
        response_API = requests.get('https://steamspy.com/api.php?request=appdetails&appid=' + lineappid)

        data = response_API.text
        # return string dari request api per appid
        return data

    def testread(self,txt):
        with open(txt + ".txt") as file:
            while line := file.readline():
                print(line.rstrip())


    def getjson(self):
        if not (os.path.exists(self.path+self.namajson)):
            print("Get Json :")
            with open(self.path+self.namajson, 'w') as f:
                with open(self.path + self.namatxt) as file:
                    # progress bar bikin cantik doang
                    with tqdm.tqdm() as progress_bar:
                        while line := file.readline():
                            # print("Line :" + line.rstrip())
                            # tulis perline dari text 1000 top game didalam sebuah json
                            isi = self.requestjson(line.rstrip())
                            f.write(isi)
                            f.write('\n')
                            progress_bar.update(1)

        else:
            print("Data Json sudah ada")

    def randomgame(self, idtxtpath):
        if not (os.path.exists(idtxtpath + ".txt")):
            r = requests.get("http://steamspy.com/api.php?request=all&page=1")
            data = r.content
            print(data)
            patternid = r'appid\":([^:]+),'
            match = re.findall(patternid, str(data))

            with open(idtxtpath + ".txt", 'w') as f:
                for id in match:
                    f.write(id)
                    f.write('\n')
            f.close()
        else:
            print("File sudah ada")

    def convertfile(self):

        if not (os.path.exists(self.path+self.namadatakotor)):

            workbook = xlsxwriter.Workbook(self.path+self.namadatakotor)
            worksheet = workbook.add_worksheet()
            worksheet2 = workbook.add_worksheet()
            row = 0
            column = 0
            column2 = 0

            header = ["appid",
                      "Name",
                      "Developer",
                      "Publisher",
                      "Release Date",
                      "Score rank",
                      "Positive",
                      "Negative",
                      "Owner",
                      "Median Owner",
                      "Average Forever",
                      "Average 2 Weeks",
                      "Median Forever",
                      "Median 2 Weeks",
                      "Price",
                      "Initial Price",
                      "Discount",
                      "CCU",
                      "Language",
                      "Genre",
                      "Tag"
                      ]

            for x in header:
                worksheet.write(row, column, x)
                column += 1

            header = ["appid",
                      "Release Date",
                      "Positive",
                      "Negative",
                      "Owner",
                      "Median Owner",
                      "Genre",
                      "Tag",
                      "Game's Revenue"
                      ]

            for x in header:
                worksheet2.write(row, column2, x)
                column2 += 1

            column = 0
            row += 1

            print("Convert File :")
            with tqdm.tqdm() as progress_bar:
                # harusnya file datanya nnti diganti
                with open(self.path+self.namajson, 'r') as f:
                    while line := f.readline():
                        # per line didalam json
                        txt = line.rstrip()
                        temp = []
                        temp2 = []
                        medown = ""

                        patternid = r'appid\":([^:]+),'
                        ids = re.findall(patternid, txt)
                        temp.append(ids[0])
                        temp2.append(ids[0])



                        patternname = r'.*name\":\"([^\"]+)\".*'
                        t = re.findall(patternname, txt)
                        # t = match.group(1)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("")


                        patterndev = r'.*developer\":\"([^\"]+)\".*'
                        t = re.findall(patterndev, txt)
                        # t = match.group(1)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("")

                        patternpub = r'.*publisher\":\"([^\"]+)\".*'
                        t = re.findall(patternpub, txt)
                        # t = match.group(1)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("")


                        #date
                        date = s.scrapedate(ids[0])
                        temp.append(date)
                        temp2.append(date)

                        patternscorank = r'score_rank\":([^:]+),'
                        t = re.findall(patternscorank, txt)
                        if (t[0] == ""):
                            temp.append("0")
                        else:
                            temp.append(t[0])

                        patternpos = r'positive\":([^:]+),'
                        t = re.findall(patternpos, txt)
                        temp.append(t[0])
                        temp2.append(t[0])
                        reviewcount = 0
                        reviewcount += int(t[0])

                        patternneg = r'negative\":([^:]+),'
                        t = re.findall(patternneg, txt)
                        temp.append(t[0])
                        temp2.append(t[0])
                        reviewcount += int(t[0])

                        year = []
                        # if "," in date: # Check if year contain commas
                        #     year = date.split(", ")
                        #     if (len(year)== 1):
                        #         if year[0]== "":
                        #             inputyear = 2017
                        #         elif type(year[0]) == str:
                        #             inputyear = 2017
                        #         else:
                        #             year = date.split(" ")
                        #             inputyear = int(year[-1])
                        #     else:
                        #         if type(year[1]) == str:
                        #             inputyear = 0
                        #         inputyear = int(year[1])
                        # elif "/" in date: # Check if year contain slash
                        #     year = date.split("/")
                        #     inputyear = int(year[-1])

                        year = re.findall(r'(\d\d\d\d)', date)

                        # Not a year (Coming soon, soon, "")
                        if len(year) == 0:
                            inputyear = 2017
                        else:
                            inputyear = int(year[0])

                        #median owner
                        hasil = self.boxleiterowner(reviewcount, inputyear)
                        owner = str(hasil[0]) + " - " + str(hasil[1])
                        temp.append(owner)
                        temp.append(hasil[2])
                        temp2.append(owner)
                        temp2.append(hasil[2])
                        medown = hasil[2]


                        patternavgfor = r'average_forever\":([^:]+),'
                        t = re.findall(patternavgfor, txt)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("0")

                        patternavg2 = r'average_2weeks\":([^:]+),'
                        t = re.findall(patternavg2, txt)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("0")

                        patternmedfor = r'median_forever\":([^:]+),'
                        t = re.findall(patternmedfor, txt)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("0")

                        patternmed2 = r'median_2weeks\":([^:]+),'
                        t = re.findall(patternmed2, txt)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("0")

                        patternprice = r'.*price\":\"([^\"]+)\".*'
                        t = re.findall(patternprice, txt)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("0")

                        patterninit = r'.*initialprice\":\"([^\"]+)\".*'
                        t = re.findall(patterninit, txt)
                        if t:
                            price = t[-1]
                            temp.append(t.pop())
                        else:
                            temp.append("0")
                            price = 0

                        #Game Revenue
                        price = int(price) / 100
                        # print("harga game =", price)
                        # print("median owner =", medown)
                        #Rumus formula
                        #https://www.gamedeveloper.com/business/genre-viability-on-steam-and-other-trends---an-analysis-using-review-count
                        rev = int(medown) * price * 0.93 * 0.92 * 0.8 * 0.8 * 0.7
                        # print("revenue = ", math.ceil(rev))


                        patterndisc = r'.*discount\":\"([^\"]+)\".*'
                        t = re.findall(patterndisc, txt)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("0")

                        patternccu = r'ccu\":([^:]+),'
                        t = re.findall(patternccu, txt)
                        if t:
                            temp.append(t.pop())
                        else:
                            temp.append("0")

                        patternlanguage = r'.*languages\":\"([^\"]+)\".*'
                        t = re.findall(patternlanguage, txt)
                        p = ""
                        p = ", ".join(t)
                        temp.append(p)

                        # genre
                        patterngenre = r'.*genre\":\"([^\"]+)\".*'
                        t = re.findall(patterngenre, txt)
                        # t = match.group(1)
                        # print(t)

                        # ini sebelumnya
                        # genre = t

                        p = ""
                        p = ", ".join(t)
                        temp.append(p)
                        temp2.append(p)



                        # tags
                        patterntags = r'.*tags\":{([^{]+)}}.*'
                        test = re.findall(patterntags, txt)
                        # print(test)
                        p = ""
                        p = ", ".join(test)
                        temp.append(p)
                        temp2.append(p)

                        # test = match.group(1)

                        # ini sebelumnya
                        # patterntags = r'\"(.*?)\"'
                        # t = re.findall(patterntags, str(test))

                        # # output udah selesai
                        # gentag = genre + t
                        # p = ""
                        # p = ", ".join(gentag)
                        # temp.append(p)
                        # # print(gentag)
                        #
                        # # print(temp)

                        column = 0

                        for x in temp:
                            worksheet.write(row, column, str(x))
                            column += 1

                        column = 0

                        for x in temp2:
                            worksheet2.write(row, column, str(x))
                            column += 1

                        worksheet2.write(row, column, math.ceil(rev))




                        row += 1
                        progress_bar.update(1)

            workbook.close()

        else:
            print("File excel udah ada")



    def boxleiterowner(self, reviewcount, releaseyear):

        if (releaseyear < 2014):
            low = 40
            high = 100
            median = 60
        elif (releaseyear) in range(2014, 2017):
            low = 35
            high = 90
            median = 50
        elif (releaseyear == 2017):
            low = 30
            high = 75
            median = 40
        elif (releaseyear) in range(2018, 2020):
            low = 25
            high = 60
            median = 35
        elif (releaseyear >= 2020):
            low = 20
            high = 55
            median = 30
        else:
            low = 0
            high = 0
            median = 0
            print("ada yg error")

        min = reviewcount * low
        max = reviewcount * high
        median = reviewcount * median

        hasil = [min, max, median]

        return hasil

    def hitungrating(self, pos, neg):
        totalreview = pos + neg
        reviewscore = pos/totalreview
        rating = reviewscore - (reviewscore - 0.5) * 2 ** (-math.log10(totalreview+1))
        # print(rating * 100)
        return (rating * 100)

    def bersihindata(self):
        path = self.path+self.namadatakotor
        if (os.path.exists(path)):
            df = pd.read_excel(path, sheet_name="Sheet2", usecols="A, B, G, H, I")
            book = xlsxwriter.Workbook(self.path+self.namadatabersih)
            writer = book.add_worksheet()
            row = 0
            temp = []
            temp2 = []
            header = ["appid", "Tahun Rilis",  "Genre & Tag", "Revenue"]
            column = 0

            for x in header:
                writer.write(row, column, x)
                column += 1

            row += 1
            data = []
            date = ""

            # list = df.values.tolist()
            id = df["appid"].tolist()
            dfdate = df["Release Date"].tolist()
            temp = df["Tag"].tolist()
            # print(temp[0])
            gen = df["Genre"].tolist()
            reve = df["Game's Revenue"].tolist()


            i = 0
            #jangan lupa bikin pengulangan pada tiap isi list

            for x in temp:
                if type(x) == str:
                    temp2 = temp[i].split(",")
                else:
                    temp2 = []
                # print(temp2[0])
                t = []
                patternangka = r"\":([^:]+)"
                for x in temp2:
                    t.append(int((re.findall(patternangka, x)).pop()))

                # out = self.outlier(self, t)
                # print(out)

                date = []
                if x:
                    if x == "":
                        date.append("nan")
                    elif type(x) == str:
                        cor = str(dfdate[i]).split(", ")
                        if len(cor) == 2: # Tahun tapi pake koma
                            date.append(cor[1])
                        else: # Tahun tapi pake spasi
                            cor = cor[0].split(" ")
                            if len(cor) == 2:
                                date.append(cor[1])
                            else:
                                date.append(cor[0])
                        
                else:
                    date.append("nan")

                # print(date)


                row2 = 0
                hasil = []

                # kalau deteksi outlier
                # for x in temp2:
                #     if out < t[row2]:
                #         hasil.append(temp2[row2].split(":")[0].strip('"'))
                #     row2 += 1

                for x in temp2:
                    hasil.append(temp2[row2].split(":")[0].strip('"'))
                    row2 += 1

                # print(hasil)
                # print(gen[i])
                if type(gen[i]) == str:
                    genre = gen[i].split(", ")
                else:
                    genre = []
                # print(genre)

                if len(date) > 0 and (date[0] != "nan" or date != None):
                    gentag = genre + hasil
                    dt = date[0]
                else:
                    gentag = ""
                    dt = "nan"

                a = list(set(gentag))
                # print(a)



                if a and (dt != "nan"):
                    #tambah ke parameter
                    self.addparameter(sorted(a))
                    self.addappid(str(id[i]))

                    writer.write(row, 0, str(id[i]))
                    writer.write(row, 1, str(dt))
                    p = ", ".join(sorted(a))
                    writer.write(row, 2, str(p))
                    writer.write(row, 3, str(reve[i]))
                    self.revenuegenre2(p, reve[i])
                    row += 1


                i += 1
                # print("No ", i)

            book.close()

        else:
            print("File tidak ditemukan")


    def outlier(self, list):
        # print("List =", list)
        if not list:
            return 0

        data = np.array(list)
        # std = np.std(data)
        mean = np.mean(data)
        q1 = np.percentile(data, 25)
        # xi = 0
        # for x in range(len(data)):
        #     xi += math.pow((data[x] - mean), 2)
        #     print(data[x], " - ", mean)
        #     print(xi)
        #
        # top = xi / len(data)
        #
        # sd = math.sqrt(top)


        # buang =  mean
        return q1
        # buang2 = mean + std

        # print(mean)
        # print(std)
        # print(buang)
        # print(buang2)
        # print(q1)

    def revenuegenre2(self, inputgentag, inputrevenue):
        inputgentag = inputgentag.split(", ")
        for listgen in inputgentag:
            if listgen in self.revenue:
                self.revenue[listgen] = self.revenue[listgen] + inputrevenue
            else:
                self.revenue[listgen] = inputrevenue






