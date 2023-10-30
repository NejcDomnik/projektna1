import poberi
import csv

slovar_leto = poberi.slovar_leto

def v_csv(ime_csv, zločini, slovar_pomozni):
    with open(ime_csv, "w", encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=zločini)
        writer.writeheader()
        for element in slovar_pomozni:
            writer.writerow(element)

#Anti-social behaviour = ASB
#vozniški prekrški = vozila
zločini = ["mesec", "antisocialno vedenje", "vlom", "rop", "vozniški prekrški", "nasilje", "kraja v trgovini", "požig ali poškodovanje lastnine", "ostale kraje", "prekrški povezani z drogami", "preostali prekrški", "kraja kolesa", "posedovanje orožja", "motenje javnega miru", "oropanje osebe"]
for enota in slovar_leto:
    sez = []
    for mesec in slovar_leto[enota]:
        pomozni_slovar = {}
        pomozni_slovar["mesec"] = mesec
        for x in range(len(zločini)-1):
            pomozni_slovar[zločini[x+1]] = slovar_leto[enota][mesec][x]
        sez.append(pomozni_slovar)
    a = enota.replace(" ", "_")
    ime_csv = f"csv_datoteke/{a}.csv"
    print(sez)
    v_csv(ime_csv, zločini, sez)