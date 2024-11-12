from abc import ABC, abstractmethod

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

    @abstractmethod
    def show_hand(self) -> None:
        pass

    @abstractmethod
    def get_hand_value(self) -> int:
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
