import os
import re
import csv
import requests
import pandas




#ta datoteka obstaja samo zato ker me je opozorilo, da sem prevečkrat vstopil na stran in mi ni več želel prepisati html kode.




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
    



meseci = {"Sep 2022", "Oct 2022", "Nov 2022", "Dec 2022", "Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023", "Jun 2023", "Jul 2023", "Aug 2023"}
slovar_leto = {}

def policija_cez_leto(policija):
    a = policija.replace(" ", "_")
    
    
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
        #ker nekatere postaje niso imele shranjenih podatkov za vse mesece, 
        #smo morali te izločiti, da lahko ustrezno nadaljujemo z analizo podatkov
        if slovar.keys() == meseci:
            slovar_leto[policija] = slovar
    
    
for policija in slovar:
    policija_cez_leto(policija)
    
print(len(slovar_leto))

#tako smo dobili slovar, ki ima za ključe ime postaje in za vrednost zeznam števil storjenih prekrškov
#slovar_leto pa ima za ključe imena postaj, za vrednosti pa slovarje v katerih so prešteti posamezni prekrški
#po mesecih (od septembra 2022 do avgusta 2023), ki so ključi.
            