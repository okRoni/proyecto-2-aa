'''
contains all the players types in the game
'''

from abc import ABC, abstractmethod
import numpy as np
from card import Card
from deck import Deck


class Player(ABC):

    def __init__(self):
        self.hand: list[Card] = []
        self.standing: bool = False
        self.busted: bool = False

    @abstractmethod
    def make_move(self, deck: Deck) -> None:
        '''
        Player chooses what to do on their turn
        '''

        pass

    @abstractmethod
    def stand(self) -> None:
        '''
        Player chooses to stand and end their turn
        '''

        pass

    @abstractmethod
    def hit(self, deck: Deck) -> None:
        '''
        Adds a card to the player's hand
        '''

        pass

    def get_hand_value(self) -> int:
        '''
        Returns the value of the player's hand
        '''

        hand_value = 0
        for card in self.hand:
            hand_value += card.value
        return hand_value

    def add_card_to_hand(self, card: Card) -> None:
        self.hand.append(card)

    def reset(self) -> None:
        '''
        Resets the player's game state
        '''

        self.hand = []
        self.standing = False
        self.busted = False

    def get_hand(self) -> list[Card]:
        '''
        Sends the player's hand
        '''

        return self.hand

    def is_busted(self) -> bool:
        '''
        Returns True if the player's hand value is greater than 21
        '''

        return True if self.get_hand_value() > 21 else False

    def is_blackjack(self) -> bool:
        '''
        Returns True if the player's hand value is 21
        '''

        if self.get_hand_value() == 21 and len(self.get_hand()) == 2:
            return True
        return False

    def is_standing(self) -> bool:
        '''
        Returns True if the player is standing
        '''

        return self.standing


class Crupier(Player):
    def __init__(self):
        super().__init__()

    def make_move(self) -> None:
        pass

    def stand(self) -> None:
        pass

    def hit(self, deck: Deck) -> None:
        pass


class HumanPlayer(Player):
    '''
    Class that represents a human player of a blackjack game.
    '''

    def __init__(self):
        super().__init__()

    def make_move(self) -> None:
        pass

    def stand(self) -> None:
        pass

    def hit(self, deck: Deck) -> None:
        if len(deck) == 0:
            # This should never happen. This is just so the app doesn't crash.
            print('WARNING: Tried to hit with an empty deck. See HumanPlayer.')
            return
        self.add_card_to_hand(deck.get_random_card())


class AiPlayer(Player):
    '''
    Class that represents an AI player of a blackjack game.
    '''

    def __init__(self):
        super().__init__()
        # Matrix with all possible (state, action) pairs.
        # Has dimensions 22x2, 22 states (hand values) and 2 actions.
        # Column 0 is hit and column 1 is stand.
        self.qtable = np.zeros((22, 2), np.int16)
        self.LEARNING_RATE = 0.75
        self.DISCOUNT_FACTOR = 0.75
        self.EXPLORATION_PROBABILITY = 0.25

    def make_move(self, deck: Deck) -> None:
        '''
        Player chooses what to do on their turn.
        '''

        # Available actions: hit (0), stand (1).
        action: int = 0  # Just as default value.
        state: int = self.get_hand_value()
        if np.random.rand() < self.EXPLORATION_PROBABILITY:
            # Decides to hit or stand randomly.
            action = np.random.randint(0, 2)  # Returns 0 or 1.
        else:
            # Decides to hit or stand based on the best Q-Value.
            hit_qvalue = self.qtable[state][0]
            stand_qvalue = self.qtable[state][1]
            action = 0 if hit_qvalue > stand_qvalue else 1

        if action == 0:
            self.standing = False
            self.hit(deck)
        else:
            self.standing = True
            self.stand()

        next_state = self.get_hand_value()
        reward = 0
        if next_state == 21:
            if len(self.get_hand()) == 2:
                # Big reward if got blackjack.
                reward = 10
            else:
                # Not so big reward if got a 21 but isn't blackjack.
                reward = 5
        elif next_state > state and next_state < 22:
            # Small reward if got closer to 21 without exceeding it.
            reward = 1
        else:
            # No! Bad AI! *slaps him/her*
            reward = -10

        if next_state <= 21:
            self.update_qvalue(state, next_state, action, reward)

    def stand(self) -> None:
        '''
        Player chooses to stand and end their turn.
        '''

        pass

    def hit(self, deck: Deck) -> None:
        '''
        Adds a card to the player's hand.
        '''

        if len(deck) == 0:
            # This should never happen. This is just so the app doesn't crash.
            print('WARNING: Tried to hit with an empty deck. See HumanPlayer.')
            return
        self.add_card_to_hand(deck.get_random_card())

    def update_qvalue(
        self, current_state: int, next_state: int, action: int, reward: int
    ) -> None:
        '''
        Updates the qvalue in the given context.
        '''

        lr = self.LEARNING_RATE
        df = self.DISCOUNT_FACTOR

        curr_state_qv = self.qtable[current_state][action]  # previous qvalue
        best_next_state_qv = np.max(self.qtable[next_state])
        new_curr_state_qv = \
            curr_state_qv \
            + lr * (reward + df * best_next_state_qv - curr_state_qv)
        self.qtable[current_state][action] = new_curr_state_qv

    def show_qtable(self) -> None:
        '''
        Prints the qtable. For testing only.
        '''

        # self.qtable has 22 rows and 2 columns.
        # Its transpose is shown just to fit better in screen.
        t_qtable = np.transpose(self.qtable)
        for i in range(2):
            for j in range(22):
                print(f'{t_qtable[i][j]:2}', end=' ')
            print()


deck = Deck()
ai = AiPlayer()

for i in range(5):
    print(f'round {i}:')
    for _ in range(21):
        ai.make_move(deck)
        if ai.is_busted():
            print('busted')
            break
        elif ai.is_blackjack():
            print('21 BJ')
            break
        elif ai.get_hand_value() == 21:
            print('21 not BJ')
        else:
            print(f'curr: {ai.get_hand_value()}')
    ai.reset()
    deck.reset()
    print()
