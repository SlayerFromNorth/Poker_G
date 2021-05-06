import random
import numpy as np
from Poker import engine_poker as pe
class Chips:
    def __init__(self, staring=5000, players=2, blind_S=25):
        self.stack = []
        self.pot = []
        self.small_blind = blind_S
        self.big_blind = blind_S * 2
        for _ in range(players):
            self.stack.append(staring)
            self.pot.append(0)

    def blinds(self, player_small, player_big):
        if self.stack[player_big] > self.big_blind:
            self.pot[player_big] += self.big_blind
            self.stack[player_big] -= self.big_blind
        else:
            self.pot[player_big] += self.stack[player_big]
            self.stack[player_big] -= self.stack[player_big]

        if self.stack[player_small] > self.small_blind:
            self.pot[player_small] += self.small_blind
            self.stack[player_small] -= self.small_blind
        else:
            self.pot[player_small] += self.stack[player_small]
            self.stack[player_small] -= self.stack[player_small]
    def bet(self, player, bet):
        if self.stack[player] > bet and (bet + self.pot[player]) >= max(self.pot):
            self.stack[player] -= bet
            self.pot[player] += bet
        elif bet > self.stack[player]:  # Allin
            self.pot[player] += self.stack[player]
            self.stack[player] -= self.stack[player]
        else:
            print("Not enough!")
            return False
        return True
    def update_winner(self, player_s):
        sumpot = sum(self.pot)
        if isinstance(player_s, int):
            self.stack[player_s] += sumpot
        else:
            part = sumpot / len(player_s)
            for gg in player_s:
                self.stack[gg] += part
        self.pot = [0 for _ in self.pot]

class Table:
    def __init__(self):
        self.hands = []
        self.board = []

    def new_hands(self):
        cards = [a for a in range(52)]
        random.shuffle(cards)
        self.hands = [cards[:2], cards[2:4], cards[4:6], cards[6:8]]
        self.board = cards[22:27]

    def show_board(self, cards):
        return self.board[0:cards]
    def show_hand(self, player):
        return self.hands[player]

class TheGame():
    def __init__(self):
        self.hands_played = 0
        self.pre_flop_turn_river_states = [0, 3, 4, 5]
        self.chips = Chips()
        self.table = Table()
    def new_hand(self):
        self.table.new_hands()
        self.hands_played += 1
        self.turn = 0
        self.pre_flop_turn_river = 0
        self.chips.blinds((self.hands_played % 2), ((self.hands_played + 1) % 2))
    def forward(self):
        player_action = (self.hands_played + self.turn) % 2
        player_oppnent = (self.hands_played + self.turn + 1) % 2
        next_turn = False
        next_round = False
        player_input = False
        print(f'Player Action: {player_action}')
        print(f'Your cards : {self.table.show_hand(player_action)}')
        print(f'Board: {self.table.show_board(self.pre_flop_turn_river_states[self.pre_flop_turn_river])}')
        print(f'Pot: {self.chips.pot}')
        print(f'Stack: {self.chips.stack[player_action]}')

        if self.chips.stack[player_action] > 0:
            player_input = int(input("bet ?"))  # Here are inputs
        else:  # Allin is going
            next_turn = True

        if player_input > 0:  # Raise
            if self.chips.bet(player_action, player_input) == True:
                next_turn = True

        elif player_input == -1:  # Fold
            self.chips.update_winner(int(np.argmax(self.chips.pot)))  # This need be fix, find precise winner
            next_round = True

        if next_turn:
            if self.turn > 0 and self.pre_flop_turn_river == 3:  # Showdown
                player1 = pe.find_Gant(self.table.show_hand(player_action) + self.table.show_board(
                    self.pre_flop_turn_river_states[self.pre_flop_turn_river]))
                player2 = pe.find_Gant(self.table.show_hand(player_oppnent) + self.table.show_board(
                    self.pre_flop_turn_river_states[self.pre_flop_turn_river]))
                print("score:", player1, player2)
                if player1 > player2:
                    self.chips.update_winner(player_action)
                else:
                    self.chips.update_winner(player_oppnent)
                print(f'Chips: {self.chips.stack}')

                return False  # Updated and ready for next hand
            if self.turn > 0 and self.chips.pot[0] == self.chips.pot[1] and self.pre_flop_turn_river < 3:
                self.pre_flop_turn_river += 1
                self.turn = 0
                return True  # Updated and ready for next card
            self.turn += 1
            return True
        elif next_round:
            return False
        else:
            return True  # Not valid, Try again


for game in range(1):
    a = TheGame()
    for rounds in range(2):
        if min(a.chips.stack) > 0:
            a.new_hand()
        else:
            print('Game finish!')
            break
        while a.forward():
            pass
