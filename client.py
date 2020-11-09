import numpy as np
import random
import ai_poker_v01 as aa

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

def betting(status, spillere, runde_inn, kortene):
    """
    [0] spiller 1 totalbeløp tilgjengelig,   [1] spiller 2 totalbeløp tilgjengelig,
    [2] spiller 1 totalbeløp tilgjengelig,   [3] spiller 2 betting denne runden
    [4] spiller 1 pot bidrag             ,   [5] spiller 2 pot bidrag


    bet > 0, check = 0, fold = -1
    """
    runde = runde_inn
    pågår = True
    if status[0] == 0 or status[1] == 0:
        return status
    while pågår:
        print(status)
        spiller_better = (runde + 1) % spillere
        if spiller_better == 0:
            spillerInput = int(input('Ditt bet?'))
        else:
            spillerInput = aa.ai_starter(kortet,stat)

        if spillerInput == -1:
            status[(runde) % spillere] += (status[spiller_better+spillere]+status[spiller_better+spillere*2]) # motspiller får penger, ikke multiplayer
            status[spiller_better+spillere], status[spiller_better+spillere*2] = 0, 0
            pågår = False
            print("fold")

        if spillerInput >= status[spiller_better]: # all in
            status[spiller_better + spillere] += status[spiller_better]
            if status[((runde) % spillere)+spillere] > status[spiller_better + spillere]: # mer bet enn motspiller hadde
                status[spiller_better] += status[((runde) % spillere)+spillere] - status[spiller_better + spillere]
                status[((runde) % spillere) + spillere] = status[spiller_better + spillere]
                pågår = False
            status[spiller_better] = 0
            print("allin")
            print(status)

        if spillerInput + status[spiller_better+spillere] < status[((runde) % spillere)+spillere]:
            print("for lite bet!")
            continue

        if not status[spiller_better] == 0 and pågår:
            status[spiller_better] -= spillerInput
            status[spiller_better + spillere] += spillerInput
        runde += 1
        if runde > (1 + runde_inn) and status[0] == 0 and status[1] == 0:
            pågår = False
            status[4] += status[2]
            status[5] += status[3]

            status[2], status[3] = 0, 0
        if runde > (1 + runde_inn) and status[2] == status[3]:
            pågår = False
            status[4] += status[2]
            status[5] += status[3]

            status[2], status[3] = 0, 0


    return status

spillere = 2
start_chips = 300
small_blind = 5

stat = [start_chips for a in range(spillere)]
[stat.append(0) for a in range(spillere*2)]

print(stat)
for runde in range(10):
    if stat[0] == 0 or stat[1] == 0:
        print("Spillet er avsluttet!")
        break
    dealer = runde % spillere
    print(stat)
    for runde in range(1):
        dealer = runde % spillere
        if stat[(runde + 1) % spillere] > small_blind:
            stat[(runde + 1) % spillere] -= small_blind
            stat[(runde + 1) % spillere + spillere] += small_blind
        else:
            stat[(runde + 1) % spillere] -= stat[(runde + 1) % spillere]
            stat[(runde + 1) % spillere + spillere] += stat[(runde + 1) % spillere]
        if stat[(runde + 2) % spillere] > small_blind:
            stat[(runde + 2) % spillere] -= (small_blind * 2)
            stat[(runde + 2) % spillere + spillere] += (small_blind * 2)
        else:
            stat[(runde + 2) % spillere] -= stat[(runde + 2) % spillere]
            stat[(runde + 2) % spillere + spillere] += stat[(runde + 2) % spillere]

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
        stat = betting(stat, spillere, runde, kortet)
        if stat[4] == 0 or gg == 7:

            a = find_Gant(kortet[0:7])
            b = find_Gant(kortet[2:9])
            print(a, b)
            if a > b:
                stat[0] += (stat[4]+stat[5])
                stat[4], stat[5] = 0, 0
                print("Du vant:", stat[0])
            elif a == b:
                stat[0], stat[1] = stat[4]+stat[0], stat[5]+stat[1]
                stat[4], stat[5] = 0, 0
                print("Begge vant:", stat[2])
            else:
                stat[1] += (stat[4] + stat[5])
                stat[4], stat[5] = 0, 0
                print("AI vant:", stat[1])

            break


# Tester

for a in range(0):
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

    a = find_Gant(kortet[0:5])
    b = find_Gant(kortet[2:9])

    print(a, b)
    print(kortet)
