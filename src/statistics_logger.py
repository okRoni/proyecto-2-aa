'''
Classes used to log the moves made by each player in the actual game session.
This data is used later to generate game statistics in the app.
Terminology conventions:
 - Game session: Isolated set of all games played while the app is open.
 - Game: Like the Spanish 'partida'. Didn't find a better translation.
Available moves (hit and stand) are represented with the strings 'H' and 'S'.
Players (croupier, ai1, ai2 and the human) are represented with the strings
'croupier', 'ai1', 'ai2' and 'human', respectively.
'''


class Game:
    '''
    Class that represents a game of blackjack.
    '''

    def __init__(self) -> None:
        self.croupier_moves: list[str] = []
        self.ai1_moves: list[str] = []
        self.ai2_moves: list[str] = []
        self.human_moves: list[str] = []
        self.winner: str = ''

class StatisticsLogger:
    '''
    Holds a record of all games in the actual game sessions and saves it to
    a .json file when the app is closed.
    '''

    def __init__(self) -> None:
        self.game_sessions