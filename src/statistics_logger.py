'''
Classes used to log the moves made by each player and the winner of each game.
This data is used later to generate game statistics in the app.
Here 'game' means like the Spanish 'partida'. Didn't find a better translation.
Available moves (hit and stand) are represented with the strings 'H' and 'S'.
Players (croupier, ai1, ai2 and the human) are represented with the strings
'croupier', 'ai1', 'ai2' and 'human', respectively.
'''


from typing import Any
import json


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
    Holds a record of all games and saves it to static/games.json when the app
    is closed.
    '''

    def __init__(self) -> None:
        self.games: list[dict[str, Any]] = []
        self.current_game: Game = Game()
        self.load_data()

    def load_data(self) -> None:
        '''
        Loads the content of static/games.json file to self.games.
        '''

        with open('../static/games.json', 'r', encoding='utf-8') as file:
            self.games = json.load(file)

    def store_data(self) -> None:
        '''
        Stores the content of self.games to static/games.json file.
        '''

        with open('../static/games.json', 'w', encoding='utf-8') as file:
            json.dump(self.games, file)

    def add_current_game(self) -> None:
        '''
        Appends the current game in the games list.
        '''

        game_dict: dict[str, list[str] | str] = {
            'croupier_moves': self.current_game.croupier_moves,
            'ai1_moves': self.current_game.ai1_moves,
            'ai2_moves': self.current_game.ai2_moves,
            'human_moves': self.current_game.human_moves,
            'winner': self.current_game.winner
        }
        self.games.append(game_dict)
        self.current_game = Game()

    def log_move(self, entity: str, move: str) -> None:
        '''
        Logs the specified move of the specified entity in the current game.
        '''

        if move not in ['H', 'S']:
            print(f'WARNING: Unknown move found in log_move ({move}).')
            return

        match entity:
            case 'croupier':
                self.current_game.croupier_moves.append(move)
            case 'ai1':
                self.current_game.croupier_moves.append(move)
            case 'ai2':
                self.current_game.croupier_moves.append(move)
            case 'human':
                self.current_game.croupier_moves.append(move)
            case _:
                print(f'WARNING: Unknown entity found in log_move ({entity}).')

    def log_winner(self, winner: str) -> None:
        '''
        Logs the specified winner in the current game.
        '''

        self.current_game.winner = winner


if __name__ == '__main__':
    logger = StatisticsLogger()
    logger.log_move('croupier', 'S')
    logger.log_move('ai1', 'S')
    logger.log_move('ai2', 'S')
    logger.log_move('human', 'S')
    logger.log_winner('human')

