import os
import re
import csv
import requests


def prenesi_stran(url, ime):
    odziv = requests.get(url)
    if odziv.status_code == 200:
        with open(ime, "w", encoding="utf-8") as f:
            f.write(odziv.text)
    else:
        print("Nekje je šlo narobe...  :(")
        

url = "https://www.ukcrimestats.com/Police_Forces/"
ime = os.path.join("stran_osnova.html")
prenesi_stran(url, ime)



with open("stran_osnova.html", "r", encoding="utf-8") as f:
    tabele = re.findall(r"<table.*?>(.*?)</table>", f.read(), re.DOTALL)
        # dobimo dve tabeli, a nas zanima le 2.
    tabela = tabele[1]
    

#po tem ko sem ustvaril slovar iz tabele sem ugotovil, da je key le številka vrstice, prvi element
#seznama v value pa še "neočiščeno" ime postaje, vrednosti pa števila zamisana kot niz z vejico;
#ki ločuje 10^3n, zato sem moral ta sledeči del kode malo zakomplicirati
#da sem dobil lep slovar:     
slovar = {}
for vrstica in re.findall(r"<tr.*?>(.*?)</tr>", tabela, re.DOTALL):
    vrsta_seznam = []
    for celica in re.findall(r"<td.*?>(.*?)</td>", vrstica, re.DOTALL):
        vrsta_seznam.append(celica)
    if vrsta_seznam != []:
        policija_ali_datum = re.findall(r"<a.*?>(.*?)</a>", vrsta_seznam[1], re.DOTALL)[0]
        slovar[policija_ali_datum] = []
        for vrednost in vrsta_seznam[2:]:
            slovar[policija_ali_datum].append(int(vrednost.replace(",", "")))
    




slovar_leto = {}

def policija_cez_leto(policija):
    a = policija.replace(" ", "_")
    url = f"https://www.ukcrimestats.com/Police_Force/{a}"
    ime = ime = os.path.join("spletne_strani", f"{a}.html")
    prenesi_stran(url, ime)
    
    with open(f"spletne_strani/{a}.html", "r", encoding="utf-8") as f:
        tabele = re.findall(r"<table.*?>(.*?)</table>", f.read(), re.DOTALL)
            # dobimo dve tabeli, a nas zanima le 2.
        tabela = tabele[1]

    slovar = {}
    #moramo še specificirati, da le prvih 12 vrstic - 12 mesecev = 1 leto
    for vrstica in re.findall(r"<tr.*?>(.*?)</tr>", tabela, re.DOTALL)[0:13]:
        vrsta_seznam = []
        for celica in re.findall(r"<td.*?>(.*?)</td>", vrstica, re.DOTALL):
            vrsta_seznam.append(celica)
        if vrsta_seznam != []:
            datum = vrsta_seznam[0]
            #datum = re.findall(r"<a.*?>(.*?)</a>", vrsta_seznam[1], re.DOTALL)[0]
            slovar[datum] = []
            for vrednost in vrsta_seznam[1:]:
                slovar[datum].append(int(vrednost.replace(",", "")))
    slovar_leto[policija] = slovar
    
    
for policija in slovar:
    policija_cez_leto(policija)

#tako smo dobili slovar, ki ima za ključe ime postaje in za vrednost zeznam števil storjenih prekrškov
#slovar_leto pa ima za ključe imena postaj, za vrednosti pa slovarje v katerih so prešteti posamezni prekrški
#po mesecih (od septembra 2022 do avgusta 2023), ki so ključi.



            