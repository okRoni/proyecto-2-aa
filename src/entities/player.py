'''
contains all the players types in the game
'''

from ..socketio_setup import socketio
import eventlet
from abc import ABC, abstractmethod
import numpy as np
from .card import Card
from .deck import Deck
from ..statistics_logger import StatisticsLogger


class Player(ABC):

    def __init__(self):
        self.hand: list[Card] = []
        self.standing: bool = False
        self.busted: bool = False
        self.position = ''

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
        
        # Check if there are aces in the hand
        aces = [card for card in self.hand if card.value == 11]
        for ace in aces:
            if hand_value > 21:
                hand_value -= 10

        return hand_value


    def add_card_to_hand(self) -> Card:
        '''
        Adds a card to the player's hand from the deck instance.
        It returns the card added to the hand.
        '''
        deck : Deck = Deck.getDeck()
        if len(deck) == 0:
            print('WARNING: Tried to add card to hand with an empty deck. See Player.')
            return
        card = deck.get_random_card()
        self.hand.append(card)
        return card

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
    
    @abstractmethod
    def copy(self) -> 'Player':
        '''
        Returns a copy of the player.
        '''
        
        pass

    def get_state(self) -> str:
        '''
        Returns the state of the player.
        '''

        if self.is_busted():
            return 'busted'
        elif self.is_blackjack():
            return 'blackjack'
        elif self.is_standing():
            return 'standing'
        else:
            if len(self.hand) < 2:
                return 'standby'
            return 'playing'

    def renderOnWeb(self, hideHand : bool = False) -> None:
        '''
        Sends the current state of the player to the web app
        for rendering.
        '''

        socketio.emit('update-and-render', {
            'position': self.position,
            'hideHand': hideHand,
            'hand': [card.to_dict() for card in self.get_hand()],
            'standing': self.is_standing(),
            'busted': self.is_busted(),
            'state': self.get_state(),
            'handValue': self.get_hand_value(),
            'hitSafeProbability': self.calculate_hit_probability()
        })
        eventlet.sleep(0)

    def calculate_hit_probability(self) -> float:
        '''
        Calculates how safe is to hit based on the current state.
        '''
        hit_safe_probability = 0.0

        # Simulate the player's move
        simulation_results = self.simulate_multiple_moves()
        hit_safe_probability = sum(simulation_results) / len(simulation_results)

        return hit_safe_probability

    def simulate_multiple_moves(self) -> list[float]:
        '''
        Simulates the next move of the player in multiple cases.
        Returns a list with the probability of hitting safely in each case.
        '''
        SIMULATION_ROUNDS : int = 1000
        round_probabilities = []

        for i in range(SIMULATION_ROUNDS):
            # Simulate a round
            round_probabilities.append(self.simulate_move())

        return round_probabilities

    def simulate_move(self) -> float:
        '''
        Simulates a move of the player based on the current state.
        Returns the probability of hitting safely.
        '''
        deck_copy = Deck.getDeck().copy()
        player_copy = self.copy()
        # crupier_copy = self.crupier.copy()
        hit_safe_probability = 0.0

        # Simulate the player's move
        card = deck_copy.get_random_card()
        player_copy.hand.append(card)
        if player_copy.is_busted():
            hit_safe_probability = 0.0
        else:
            hit_safe_probability = 1.0

        return hit_safe_probability

    def __str__(self) -> str:
        return f'Hand ({self.get_hand_value()}): {self.hand}'


class Crupier(Player):
    def __init__(self):
        super().__init__()
        self.position = 'crupier'

    def make_move(self) -> None:
        logger: StatisticsLogger = StatisticsLogger.get_logger()
        if self.get_hand_value() < 17:
            self.hit(Deck.getDeck())
            logger.log_move('croupier', 'H', self.get_hand_value())
        else:
            self.stand()
            logger.log_move('croupier', 'S', self.get_hand_value())

    def stand(self) -> None:
        self.standing = True
        pass

    def hit(self, deck: Deck) -> None:
        self.standing = False
        if len(deck) == 0:
            print('WARNING: Tried to hit with an empty deck. See Crupier.')
            return
        self.add_card_to_hand()

    def get_showing_card(self) -> Card:
        '''
        Returns the first card in the crupier's hand
        '''
        return self.hand[0]
    
    def copy(self) -> 'Crupier':
        '''
        Returns a copy of the crupier.
        '''
        crupier = Crupier()
        crupier.hand = self.hand.copy()
        crupier.standing = self.standing
        crupier.busted = self.busted
        return crupier


class HumanPlayer(Player):
    '''
    Class that represents a human player of a blackjack game.
    '''

    instance : 'HumanPlayer' = None

    @staticmethod
    def get_current_instance() -> 'HumanPlayer':
        return HumanPlayer.instance

    def __init__(self):
        super().__init__()
        self.position = 'player'

        HumanPlayer.instance = self

    def make_move(self) -> None:
        
        socketio.emit('start-player-turn')
        eventlet.sleep(0)

        move = self.wait_for_player_move()
        logger: StatisticsLogger = StatisticsLogger.get_logger()
        if move == 'hit':
            print('Player hit')
            self.hit()
            logger.log_move('human', 'H', self.get_hand_value())
        elif move == 'stand':
            print('Player stand')
            self.stand()
            logger.log_move('human', 'S', self.get_hand_value())

        socketio.emit('end-player-turn')

    def wait_for_player_move(self) -> str:
        move = None

        def handle_move(data : dict):
            nonlocal move
            move = data.get('move')

        socketio.on_event('player-move', handle_move)

        while move is None:
            eventlet.sleep(0.1)

        return move

    def stand(self) -> None:
        self.standing = True
        pass

    def hit(self) -> None:
        deck : Deck = Deck.getDeck()
        if len(deck) == 0:
            # This should never happen. This is just so the app doesn't crash.
            print('WARNING: Tried to hit with an empty deck. See HumanPlayer.')
            return
        self.add_card_to_hand()

    def copy(self) -> 'HumanPlayer':
        '''
        Returns a copy of the player.
        '''

        player = HumanPlayer()
        player.hand = self.hand.copy()
        player.standing = self.standing
        player.busted = self.busted
        player.position = self.position
        return player


class AiPlayer(Player):
    '''
    Class that represents an AI player of a blackjack game.
    It uses Q-Learning and Probalistic Algorithms to make decisions.
    '''

    def __init__(self, position: str = ''):
        super().__init__()
        self.position = position

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

        # Prob algorithm variables
        self.crupier : Crupier = None
        self.hit_probability = 0.0

        self.ql_weight = 0.4
        self.prob_weight = 0.6


    def make_move(self) -> None:
        '''
        Player chooses what to do on their turn.
        '''

        print('------------------')
        print('Player hand:', self.get_hand_value())
        print('Hit safe probability:', self.calculate_hit_probability())
        print('------------------')

        state: int = self.get_hand_value()
        ql_action: int = self.get_ql_action(state)
        prob_action = self.get_prob_action()

        action = 0

        if ql_action == 0 and prob_action == 0:
            action = 0
        elif ql_action == 1 and prob_action == 1:
            action = 1
        else:
            random_number = np.random.rand()
            if random_number < self.ql_weight:
                action = ql_action
            else:
                action = prob_action

        logger: StatisticsLogger = StatisticsLogger.get_logger()
        if action == 0:
            print('Hitting...')
            self.standing = False
            self.hit()
            logger.log_move(self.position, 'H', self.get_hand_value())
        else:
            print('Standing...')
            self.standing = True
            self.stand()
            logger.log_move(self.position, 'S', self.get_hand_value())

        next_state = self.get_hand_value()
        reward = self.get_reward(state, next_state)
        self.update_qvalue(state, next_state, action, reward)

    def stand(self) -> None:
        '''
        Player chooses to stand and end their turn.
        '''

        pass

    def hit(self) -> None:
        '''
        Adds a card to the player's hand.
        '''

        deck : Deck = Deck.getDeck()
        if len(deck) == 0:
            # This should never happen. This is just so the app doesn't crash.
            print('WARNING: Tried to hit with an empty deck. See HumanPlayer.')
            return
        self.add_card_to_hand()

    def copy(self) -> 'AiPlayer':
        '''
        Returns a copy of the player.
        '''

        player = AiPlayer()
        player.hand = self.hand.copy()
        player.standing = self.standing
        player.busted = self.busted
        player.qtable = self.qtable.copy()
        player.prev_hand_value = self.prev_hand_value
        return player

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

    def get_ql_action(self, state: int) -> int:
        '''
        Decides if hit or stand based on the current qtable.
        '''

        # Available actions: hit (0), stand (1).
        action: int = 0  # Just as default value.
        self.prev_hand_value = state  # For testing purposes.
        if np.random.rand() < self.EXPLORATION_PROBABILITY:
            # Decides to hit or stand randomly.
            action = np.random.randint(0, 2)  # Returns 0 or 1.
        else:
            # Decides to hit or stand based on the best Q-Value.
            hit_qvalue = self.qtable[state][0]
            stand_qvalue = self.qtable[state][1]
            action = 0 if hit_qvalue > stand_qvalue else 1

        return action

    def get_reward(self, state: int, next_state: int) -> float:
        '''
        Returns the corresponding reward based on a state change.
        '''

        reward: float = 0
        if next_state == 21:
            reward = 1
        elif next_state > 21:
            reward = -0.25
        elif next_state < 21:
            if next_state > state:
                reward = 0.25
            else:
                reward = 0
        return reward

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
    
    def get_prob_action(self) -> int:
        '''
        Decides if hit or stand based on the current qtable.
        '''

        # Available actions: hit (0), stand (1).
        action: int = 0

        hit_safe_probability = self.calculate_hit_probability()
        if hit_safe_probability > 0.6:
            action = 0
        else:
            action = 1

        return action
