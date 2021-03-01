from Poker import engine_poker
import numpy as np
import random


def chance_ran (my_hand, board, epoker=1000):
    kortet = my_hand
    bordet = board
    ai_counter, Even_counter = 0, 0

    for _ in range(epoker):
        kortene = [kortet[0], kortet[1]]
        kortene += bordet
        en_kortstokk = [a for a in range(52)]
        [en_kortstokk.remove(b) for b in kortene]
        for a in range(9 - len(kortene)):
            kort = random.choice(en_kortstokk)
            en_kortstokk.remove(kort)
            kortene.append(kort)

        ai_styrke = engine_poker.find_Gant(kortene[:-2])
        Even_styrke = engine_poker.find_Gant(kortene[2:])

        if ai_styrke >= Even_styrke:
            ai_counter += 1
        else:
            Even_counter += 1

    return ai_counter/epoker




def ai_starter(kortene, status=[0,0,0,0,0,0]):
# Kortene,POT, CAll_sum, AGV, BS-Check, BS-Call, BS-Raise
    print(status)
    bs_check, bs_call, bs_raise = status[3], status[4], status[5]
    if (status[1] / status[0]) < 0.5:
        CB = (status[1]/status[0])
    else:
        CB = 2.5 * (status[1]/status[0])

    print("-----CB-----", CB)
    myhand = kortene[0:2]
    board = kortene[2:]
    a = chance_ran(myhand, board)
    inputs = [a, bs_check, bs_call, bs_raise, CB]
    # Fold - Call - Raise
    weights = [[-1, 0.55, 1], [0, 0.07, 0.15], [0.11, 0.05, 0], [0.18, 0.13, 0], [0.3, 0.1, 0]]
    biases = [1, 0.35, 0.1]
    lag = np.dot(inputs, weights) + biases
    print("vinner SJANSE:", a)
    out = np.argmax(lag)

    return [out, lag]


"""for a in [4,6,8,13,32,34,51,23,24,41,42]:
    for b in [2,5,9,21,44,45,50]:
        print(engine_poker.poker_names([a,b]))
        ai_starter([a,b])
"""
