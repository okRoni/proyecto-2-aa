'''
contains all the players types in the game
'''

from abc import ABC, abstractmethod
from deck import Deck


class Player(ABC):
    def __init__(self):
        self.hand : list = []
        self.standing : bool = False
        self.busted : bool = False

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
    def hit(self, deck) -> None:
        '''
        Adds a card to the player's hand
        '''
        pass

    def get_hand_value(self) -> int:
        '''
        Returns the value of the player's hand
        '''
        pass

    def add_card_to_hand(self, card) -> None:
        self.hand.append(card)

    def reset(self) -> None:
        '''
        Resets the player's game state
        '''
        self.hand = []
        self.standing = False
        self.busted = False

    def get_hand(self) -> list:
        '''
        Sends the player's hand
        '''
        return self.hand

    def is_busted(self) -> bool:
        '''
        Returns True if the player's hand value is greater than 21
        '''
        pass

    def is_blackjack(self) -> bool:
        '''
        Returns True if the player's hand value is 21
        '''
        pass

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

    def hit(self, deck) -> None:
        pass


class HumanPlayer(Player):
    """
    Class that represents a human player of a blackjack game.
    """

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
