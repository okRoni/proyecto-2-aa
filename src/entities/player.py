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
    def make_move(self) -> None:
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

        if self.get_hand_value() == 21:
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
        self.NUM_ACTIONS = 2  # Hit or stand
        self.NUM_STATES = 21  # Max hand value. If greater, already lost.
        # Matrix with all possible (action, hand_value) pairs.
        self.qtable = np.zeros((self.NUM_ACTIONS, self.NUM_STATES), np.int8)
        self.LEARNING_RATE = 0.75
        self.DISCOUNT_FACTOR = 0.75
        self.EXPLORATION_PROBABILITY = 0.25

    def make_move(self) -> None:
        '''
        Player chooses what to do on their turn.
        '''

        pass

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

    def __show_qtable(self) -> None:
        '''
        Prints the qtable. For testing only.
        '''

        for i in range(self.NUM_ACTIONS):
            for j in range(self.NUM_STATES):
                print(self.qtable[i][j], end=' ')
            print()
