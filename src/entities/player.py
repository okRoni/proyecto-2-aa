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
        # Has dimensions 32x2, 32 states (hand values) and 2 actions.
        # Column 0 is hit and column 1 is stand.
        # Has 32 possible states because the worst hand possible is reached
        # by having 20, hitting and getting an ace (11). That adds up to 31.
        # 1 extra state is added to count the 0 state (empty hand).
        self.qtable = np.zeros((32, 2))

        self.LEARNING_RATE = 0.75
        self.DISCOUNT_FACTOR = 0.75
        self.EXPLORATION_PROBABILITY = 0.25
        self.prev_hand_value = 0  # Just for testing purposes.

    def make_move(self, deck: Deck) -> None:
        '''
        Player chooses what to do on their turn.
        '''

        # Available actions: hit (0), stand (1).
        action: int = 0  # Just as default value.
        state: int = self.get_hand_value()
        self.prev_hand_value = state  # For testing purposes.
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
            reward = 1
        elif next_state > 21:
            reward = -0.25
        elif next_state < 21:
            if next_state > state:
                reward = 0.25
            else:
                reward = 0

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
        self, current_state: int, next_state: int, action: int, reward: float
    ) -> None:
        '''
        Updates the qvalue in the given context.
        '''

        lr = self.LEARNING_RATE
        df = self.DISCOUNT_FACTOR

        curr_state_qv = self.qtable[current_state][action]
        best_next_state_qv = np.max(self.qtable[next_state])
        new_curr_state_qv = \
            curr_state_qv \
            + lr * (reward + df * best_next_state_qv - curr_state_qv)
        self.qtable[current_state][action] = new_curr_state_qv

    def show_qtable(self) -> None:
        '''
        Prints the qtable. For testing only.
        '''

        # self.qtable has 32 rows and 2 columns.
        # Its transpose is shown just to fit better in screen.
        t_qtable = np.transpose(self.qtable)
        for i in range(2):
            for j in range(22):  # After the 21st row there are just zeros.
                rounded_value = f'{t_qtable[i][j]:.2f}'
                print(f'{rounded_value:5}', end=' ')
            print()

if __name__ == '__main__':

    deck = Deck()
    ai = AiPlayer()

    for i in range(20):
        # print(f'round {i}:')
        done = False
        while not done:
            ai.make_move(deck)
            if ai.is_busted():
                # print('busted')
                done = True
            elif ai.is_blackjack():
                print('21 BJ on round', i)
                done = True
            elif ai.get_hand_value() == 21:
                # print('21 not BJ on round', i)
                done = True
            elif ai.is_standing():
                # print('standing')
                # done = True
                pass
            else:
                p = ai.prev_hand_value
                s = 'stand' if ai.is_standing() else 'hit'
                # print(f'curr: {ai.get_hand_value()}. Was in {p} and {s}.')
        print('ended with', ai.get_hand_value())
        ai.reset()
        deck.reset()
        # print()

    ai.show_qtable()