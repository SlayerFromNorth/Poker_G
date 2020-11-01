import numpy as np
import random

kortstokk =[[20,2],[20,3],[20,4],[20,5],[20,6],[20,7],[20,8],[20,9],[20,10],[20,11],[20,12],[20,13],[20,14],
           [30,2],[30,3],[30,4],[30,5],[30,6],[30,7],[30,8],[30,9],[30,10],[30,11],[30,12],[30,13],[30,14],
           [40,2],[40,3],[40,4],[40,5],[40,6],[40,7],[40,8],[40,9],[40,10],[40,11],[40,12],[40,13],[40,14],
           [50,2],[50,3],[50,4],[50,5],[50,6],[50,7],[50,8],[50,9],[50,10],[50,11],[50,12],[50,13],[50,14]]
farge = [20, 30, 40, 50]
navn = [{1: "Feil",    2: "To", 3: "Tre", 4: "Fire", 5: "Fem",
        6: "Seks",    7: "Syv", 8: "Åtte", 9: "Ni", 10: "Ti",
        11: "Knekt",    12: "Dame", 13: "Konge", 14: "Ess",
        20: "Spar", 30: "Hjerter", 40: "Ruter", 50: "Kløver"},
        {1: "Feil",    2: "2", 3: "3", 4: "4", 5: "5",
        6: "6",    7: "7", 8: "8", 9: "9", 10: "10",
        11: "11",    12: "12", 13: "13", 14: "14",
        20: "S", 30: "H", 40: "R", 50: "K"}]



def find_Gant(kortene):
    """StrightFlush | Fire like | Hus | Flush | Stright | Trelike | To par | Et par | high card"""

    farger =[kortstokk[a, 0] for a in kortene]
    tallerverdier = [kortstokk[a, 1] for a in kortene]
    tallerverdier.sort(reverse=True)


    # High card
    high = f"{tallerverdier[0]:02d}{tallerverdier[1]:02d}{tallerverdier[2]:02d}{tallerverdier[3]:02d}{tallerverdier[4]:02d}"
    points = [0, int(high)]

    # Flush
    for ss in farge:
        gg = [1 if a == ss else 0 for a in farger]
        if sum(gg) > 4:
            print("flush")
            riktige = [kortene[index] if a == 1 else None for index, a in enumerate(gg)]
            riktige = [i for i in riktige if i != None]
            tallerverdierflush = [kortstokk[a, 1] for a in riktige]
            tallerverdierflush.sort(reverse=True)
            high = f"{tallerverdierflush[0]:02d}{tallerverdierflush[1]:02d}{tallerverdierflush[2]:02d}{tallerverdierflush[3]:02d}{tallerverdierflush[4]:02d}"
            points = [6, int(high)]
            if tallerverdierflush[0]== 14:
                tallerverdierflush.append(1)
            for cc in range(len(tallerverdierflush) - 4):
                if tallerverdierflush[cc]-tallerverdierflush[cc + 4] == 4:
                    print("Straitflush")
                    points = [9, tallerverdierflush[cc]]
            return points

    # Straight

    teller = 0
    hoy = 0
    if tallerverdier[0] == 14:
        tallerverdier.append(1)
    for a in range(len(tallerverdier)-1):
        if hoy == 0:
            hoy = tallerverdier[a]
        if tallerverdier[a] - 1 == tallerverdier[a+1]:
            teller += 1
            if teller > 3:
                print("Straight")
                points = [5, hoy]
                return points
        elif tallerverdier[a] == tallerverdier[a+1]:
            pass
        else:
            teller = 0
            hoy = 0

    # Like

    par = 0
    parene =[]
    trelikeverdi=0
    trelike = 0
    for ss in [a+2 for a in range(13)]:

        gg = [1 if a == ss else 0 for a in tallerverdier]
        if sum(gg) > 3:
            print("Fire like", ss)
            points = [8, ss]
        elif sum(gg) > 2:
            print("Tre like", ss)
            trelike +=1
            trelikeverdi = ss
            riktige = [i for i in tallerverdier if i != ss]
            high = f"{ss:02d}{ss:02d}{ss:02d}{riktige[0]:02d}{riktige[1]:02d}"
            points = [4, int(high)]
        elif sum(gg) > 1:
            print("Par", ss)
            parene.append(ss)
            par +=1
            riktige = [i for i in tallerverdier if i != ss]
            high = f"{ss:02d}{ss:02d}{riktige[0]:02d}{riktige[1]:02d}{riktige[2]:02d}"
            points = [2, int(high)]
    if par == 2:
        print("To par")
        riktige = [i for i in tallerverdier if i != parene[0]]
        riktige = [i for i in riktige if i != parene[1]]
        high = f"{parene[1]:02d}{parene[1]:02d}{parene[0]:02d}{parene[0]:02d}{riktige[0]:02d}"
        points = [3, int(high)]
    if par > 2:
        print("To* par")
        riktige = [i for i in tallerverdier if i != parene[2]]
        riktige = [i for i in riktige if i != parene[1]]
        high = f"{parene[2]:02d}{parene[2]:02d}{parene[1]:02d}{parene[1]:02d}{riktige[0]:02d}"
        points = [3, int(high)]
    if trelike == 1 and par == 1:
        print("Fult hus")
        points = [7, trelikeverdi*10 + par]


    return points

def betting(status,teller_tur_inn):
    """
    [0] spiller 1 totalbeløp tilgjengelig,   [1]spiller 1 betting denne runden,
    [2]     pot
    [3] spiller 2 betting denne runden,     [4] spiller 2 totalbeløp tilgjengelig

    bet > 0, check = 0, fold = -1
    """
    teller_tur = teller_tur_inn
    pågår = True
    while pågår:
        print(status)
        if teller_tur % 2 == 0:
            userInput = int(input('Ditt bet?'))
        else:
            userInput = random.choice([0, status[1]])    # ---------------HER ER AI SPILLER---------------check/call
        if userInput == -1:
            status[((teller_tur + 1) % 2) * 4] += status[1] + status[2] + status[3]
            status[1], status[2], status[3] = 0, 0, 0
            print("fold")
            pågår = False
        if userInput + status[1+(teller_tur % 2)*2] < status[1+((teller_tur+1) % 2)*2]:
            print("for lite bet!")
            continue
        if userInput > status[0] + status[1] or userInput > status[4] + status[3]:
            userInput = min(max(0, status[0] + status[1]), max(0, status[4] + status[3]))-status[1+(teller_tur % 2)*2]
        status[(teller_tur % 2) * 4] -= userInput
        status[1+((teller_tur % 2)*2)] += userInput
        teller_tur += 1

        if teller_tur > (1 + teller_tur_inn) and status[1] == status[3]:
            pågår = False
            status[2] += status[1]*2
            status[1], status[3] = 0, 0


    return status

"""
class poker_ai:
    def __init__(self, kortet):
        self.kortdata = kortet
        """

stat = [300, 0, 0, 0, 300]
blind = 5
for tass in range(0):
    if stat[0] == 0 or stat[4] == 0:
        print("Spillet er avsluttet!")
        break
    if tass % 2 == 0:
        teller_tur = 0
        spiller_EN = blind
        spiller_TO = blind * 2
    else:
        teller_tur = 1
        spiller_EN = blind * 2
        spiller_TO = blind
    stat[0], stat[1], stat[3], stat[4] = stat[0]-spiller_EN, spiller_EN, spiller_TO, stat[4]-spiller_TO
    kortstokk = np.asarray(kortstokk)
    en_kortstokk = [a for a in range(51)]
    kortet = []


    for a in range(9):
        kort = random.choice(en_kortstokk)
        en_kortstokk.remove(kort)
        kortet.append(kort)
    for gg in [2, 5, 6, 7]:
        for ss in range(gg):
            print(navn[1].get(kortstokk[kortet[ss], 0]), navn[1].get(kortstokk[kortet[ss], 1]))
        stat = betting(stat, teller_tur)
        if stat[2] == 0 or gg == 7:

            a = find_Gant(kortet[0:7])
            b = find_Gant(kortet[2:9])
            print(a, b)
            if a > b:
                print("Du vant:", stat[2])
                stat[0] += stat[2]
                stat[2] = 0
            elif a == b:
                print("Begge vant:", stat[2])
                stat[0] += int(stat[2]/2)
                stat[4] += int(stat[2] / 2)
                stat[2] = 0
            else:
                print("AI vant:", stat[2])
                stat[4] += stat[2]
                stat[2] = 0
            break


# Tester

for a in range(1):
    kortstokk = np.asarray(kortstokk)
    en_kortstokk = [a for a in range(51)]
    kortet = []
    for a in range(9):
        kort = random.choice(en_kortstokk)
        en_kortstokk.remove(kort)
        kortet.append(kort)

    print(navn[1].get(kortstokk[kortet[0], 0]), navn[1].get(kortstokk[kortet[0], 1]), navn[1].get(kortstokk[kortet[1], 0]), navn[1].get(kortstokk[kortet[1], 1]))
    print(navn[1].get(kortstokk[kortet[2], 0]), navn[1].get(kortstokk[kortet[2], 1]), navn[1].get(kortstokk[kortet[3], 0]), navn[1].get(kortstokk[kortet[3], 1]),
          navn[1].get(kortstokk[kortet[4], 0]), navn[1].get(kortstokk[kortet[4], 1]), navn[1].get(kortstokk[kortet[5], 0]), navn[1].get(kortstokk[kortet[5], 1]),
          navn[1].get(kortstokk[kortet[6], 0]), navn[1].get(kortstokk[kortet[6], 1]))
    print(navn[1].get(kortstokk[kortet[7], 0]), navn[1].get(kortstokk[kortet[7], 1]), navn[1].get(kortstokk[kortet[8], 0]), navn[1].get(kortstokk[kortet[8], 1]))

    a = find_Gant(kortet[0:7])
    b = find_Gant(kortet[2:9])

    print(a, b)
    print(kortet)

kortet1= [0,2,3,12,14,23,34]
gg = find_Gant(kortet1[0:7])
print(gg)
