from bs4 import BeautifulSoup
import os.path
import re
import requests
import tqdm
import datetime as dt
        
pathdir = ".\\pymodule\\"

def scrapedate(appid):
    urlsteam = "https://store.steampowered.com/app/"
    baseurl = urlsteam
    try:
        r = requests.get(baseurl+appid)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    soup = BeautifulSoup(r.content, 'lxml')
    temp = soup.find('div', class_='date')
    patterndate = r'<div class=\"date">(.*)</div?>'
    matches = re.findall(patterndate, str(temp))

    # print(soup)
    # print(matches.pop())

    if matches:
        return(matches.pop())
    else:
        return("")

def scrapepopular(page_num):
    date = dt.datetime.now()
    now = date.strftime("%B%Y")
    namafile = "populer" + now + ".txt"

    if  os.path.exists(pathdir+namafile):
        print("Sudah scraping!")
        return
        
    urlpopuler = "https://store.steampowered.com/search/?category1=998&os=win&filter=topsellers&page="
    baseurl = urlpopuler
    i = 1
    hasil = []
    print("Scrape Populer: ")
    with tqdm.tqdm() as progess_bar:
        while i <= page_num:
            try:
                r = requests.get(baseurl + str(i))
                r.raise_for_status()
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)

            soup = BeautifulSoup(r.content, 'lxml')
            # print(soup)
            temp = soup.find('div', {"id": "search_result_container"})
            # print(temp)
            temp = temp.find_all('a', class_= "search_result_row ds_collapse_flag", href=True)
            # temp = soup.find(id="search_resultRows")
            # print(temp)

            patternlink = r'data-ds-appid=\"(.*?)\"'
            matches = re.findall(patternlink, str(temp))
            # print(matches)
            if matches == []:
                break
            hasil = hasil+matches
            i += 1
            progess_bar.update(1)

    strhasil = ','.join(hasil)
    hasil = strhasil.split(",")
    hasil = list(dict.fromkeys(hasil))
    # print(hasil)
    masuktxt(hasil,pathdir+namafile)

def masuktxt(list, file):
    with open(file, 'w') as f:
        for item in list:
            f.write("%s\n" % item)
