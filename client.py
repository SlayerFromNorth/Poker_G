import numpy as np
import random
from Poker import ai_poker_v01 as aa
from Poker import engine_poker

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
        if status[2] != status[3]:
            if status[0] > status[1]:
                status[0] += status[2]-status[3]
                status[2] -= status[2] - status[3]
            else:
                status[1] += status[3]-status[2]
                status[2] -= status[3] - status[2]
        pågår = False
    while pågår:
        print(status)
        spiller_better = (runde + 1) % spillere
        if spiller_better == 0:
            spillerInput = int(input('Ditt bet?'))
        else:
            spillerInput = aa.ai_starter(kortet, stat)

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


for runde in range(10):

    if stat[0] == 0 or stat[1] == 0:
        print("Spillet er avsluttet!")
        break

    small = (runde + 1) % spillere
    big = (runde + 2) % spillere
    stat[small], stat[small + 2] = stat[small]-small_blind, stat[small +2] + small_blind
    stat[big], stat[big + 2] = stat[big] - small_blind * 2, stat[big + 2] + small_blind * 2
    if stat[small] < 0:
        stat[small], stat[small + 2] = 0, stat[small + 2] + stat[small]
    if stat[big] < 0:
        stat[big], stat[big + 2] = 0, stat[big + 2] + stat[big]

    kortstokk = engine_poker.kortstokk
    navn = engine_poker.navn
    en_kortstokk = [a for a in range(51)]
    kortet = []
    print(stat)
    for a in range(9):
        kort = random.choice(en_kortstokk)
        en_kortstokk.remove(kort)
        kortet.append(kort)
        for gg in [2, 5, 6, 7]:
            try:
                for ss in range(gg):
                    print(navn[1].get(kortstokk[kortet[ss], 0]), navn[1].get(kortstokk[kortet[ss], 1]))
                stat = betting(stat, spillere, runde, kortet)
                if stat[0] == 0 or stat[1] == 0 or gg == 7:

                    a = engine_poker.find_Gant(kortet[0:7])
                    b = engine_poker.find_Gant(kortet[2:9])
                    print(a, b)
                    if a > b:
                        stat[0] += (stat[4]+stat[5])
                        print("Du vant:", stat[4] + stat[5])
                        stat[4], stat[5] = 0, 0
                    elif a == b:
                        stat[0], stat[1] = stat[4]+stat[0], stat[5]+stat[1]
                        print("Begge vant:", stat[2])
                        stat[4], stat[5] = 0, 0
                    else:
                        stat[1] += (stat[4] + stat[5])
                        print("AI vant:", stat[4] + stat[5])
                        stat[4], stat[5] = 0, 0
                    break
            except:
                pass
