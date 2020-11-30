from Poker import engine_poker
import numpy as np
import random


def ai_starter(kortene, status):
    kortet = kortene
    en_kortstokk = [a for a in range(51)]
    [en_kortstokk.remove(b) for b in kortet]
    kortet = []
    for a in range(5-len(kortet)):
        kort = random.choice(en_kortstokk)
        en_kortstokk.remove(kort)
        kortet.append(kort)

    a = engine_poker.find_Gant(kortet)

    inputs = [a[0], a[1]/1000000000]
    weights = [-0.9, -1.5], [1.1, 0.2], [1.6, 0.7]
    biases = [3.7, 2.8, 0.1]


    layer_outputs=[]


    for neuron_weights, neuron_bias in zip(weights, biases):
        # Zeroed output of given neuron
        neuron_output = 0
        # For each input and weight to the neuron
        for n_input, weight in zip(inputs, neuron_weights):
            # Multiply this input by associated weight
            # and add to the neuron’s output variable
            neuron_output += n_input*weight
            # Add bias
        neuron_output += neuron_bias
        # Put neuron’s result to the layer’s output list
        layer_outputs.append(neuron_output)
    #print(layer_outputs)
    gg = np.argmax(layer_outputs)
    if gg == 0: return -1
    if gg == 1: return status[2]-status[3]
    if gg == 2: return status[1]
