'''
Classes used to log the moves made by each player and the winners of each game.
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
        # These lists store the moves made by each player and the hand value
        # obtained next to the move. For example, if ai1 hits and gets
        # 10, then stands, then hits and gets 7, it will look like
        # ['H', 10, 'S', 10, 'H', 17]. The same for the other players.
        # Note that this stores the cumulative sum instead of each card value.
        self.croupier_moves: list[str | int] = []
        self.ai1_moves: list[str | int] = []
        self.ai2_moves: list[str | int] = []
        self.human_moves: list[str | int] = []
        self.winners: list[str] = []


class StatisticsLogger:
    '''
    Holds a record of all games and saves it to static/games.json.
    Also, offers useful statistics about the game.
    '''

    instance = None  # Shared instance of StatisticsLogger.

    @staticmethod
    def get_logger() -> 'StatisticsLogger':
        '''
        Returns the shared instance of StatisticsLogger.
        If the instance doesn't exist, it creates one.
        '''

        if StatisticsLogger.instance is None:
            StatisticsLogger.instance = StatisticsLogger()
        return StatisticsLogger.instance

    def __init__(self) -> None:
        self.games: list[dict[str, Any]] = []
        self.current_game: Game = Game()
        self.load_data()

    def load_data(self) -> None:
        '''
        Loads the content of static/games.json file to self.games.
        '''

        with open('./static/games.json', 'r', encoding='utf-8') as file:
            self.games = json.load(file)

    def store_data(self) -> None:
        '''
        Stores the content of self.games to static/games.json file.
        '''

        self.add_current_game()
        with open('./static/games.json', 'w', encoding='utf-8') as file:
            json.dump(self.games, file)

    def add_current_game(self) -> None:
        '''
        Appends the current game in the games list.
        '''

        game_dict: dict[str, Any] = {
            'croupier_moves': self.current_game.croupier_moves,
            'ai1_moves': self.current_game.ai1_moves,
            'ai2_moves': self.current_game.ai2_moves,
            'human_moves': self.current_game.human_moves,
            'winners': self.current_game.winners
        }
        self.games.append(game_dict)
        self.current_game = Game()

    def log_move(self, entity: str, move: str, new_hand_value: int) -> None:
        '''
        Logs the specified move and new hand value of the specified entity
        in the current game.
        '''

        if new_hand_value < 0:
            print('WARNING: Tried to log a negative hand value in log_move.')
            return

        if move not in ['H', 'S']:
            print(f'WARNING: Unknown move found in log_move ({move}).')
            return

        match entity:
            case 'croupier':
                self.current_game.croupier_moves += [move, new_hand_value]
            case 'ai1':
                self.current_game.ai1_moves += [move, new_hand_value]
            case 'ai2':
                self.current_game.ai2_moves += [move, new_hand_value]
            case 'human':
                self.current_game.human_moves += [move, new_hand_value]
            case _:
                print(f'WARNING: Unknown entity found in log_move ({entity}).')

    def log_winners(self, winners: list[str]) -> None:
        '''
        Logs the specified winners in the current game.
        '''

        for i in winners:
            if i not in ['croupier', 'ai1', 'ai2', 'human']:
                print(f'WARNING: Unknown entity found in log_winners ({i}).')
                return
        self.current_game.winners = winners

    def get_win_percentage(self) -> list[float]:
        '''
        Returns the percentage of win per player.
        Order: Croupier, ai1, ai2, human.
        '''

        total_games: int = len(self.games)
        # This is needed because otherwise a division by zero will be
        # performed at the end of the function.
        if total_games == 0:
            return [0, 0, 0, 0]
        total_wins: list[float] = [0, 0, 0, 0]  # Total wins per player.
        for game in self.games:
            for winner in game['winners']:
                match winner:
                    case 'croupier':
                        total_wins[0] += 1
                    case 'ai1':
                        total_wins[1] += 1
                    case 'ai2':
                        total_wins[2] += 1
                    case 'human':
                        total_wins[3] += 1
                    case _:
                        pass
        return [100 * i / total_games for i in total_wins]

    def get_success_percentage(self) -> list[float]:
        '''
        Returns the percentage of right decisions made per player.
        A bad decision is hitting and getting above 21 or standing bellow
        17 (by probability, is bad to stand bellow 17). Anything else is
        considered a good decision.
        Order: Croupier, ai1, ai2, human.
        '''

        def get_bad_decisions(moves_list: list[Any]) -> int:
            bad_decisions: int = 0
            # A bad decision is hitting and getting above 21 or standing below
            # 17. This loop looks for situations like that.
            for i in range(0, len(moves_list), 2):
                hit: bool = moves_list[i] == 'H'
                hand_value: int = moves_list[i + 1]
                if hit and hand_value > 21 or not hit and hand_value < 17:
                    bad_decisions += 1
            return bad_decisions

        # Total decisions and bad decisions per player.
        total_decisions: list[int] = [0, 0, 0, 0]
        bad_decisions: list[int] = [0, 0, 0, 0]

        for game in self.games:
            # Each moves list contains the move and the new hand value.
            # For example, game['ai1'] may contain ['H', 4, 'S', 9]. So, the
            # amount of decisions is the length of that list divided by 2.
            total_decisions[0] += len(game['croupier_moves']) // 2
            total_decisions[1] += len(game['ai1_moves']) // 2
            total_decisions[2] += len(game['ai2_moves']) // 2
            total_decisions[3] += len(game['human_moves']) // 2

            bad_decisions[0] += get_bad_decisions(game['croupier_moves'])
            bad_decisions[1] += get_bad_decisions(game['ai1_moves'])
            bad_decisions[2] += get_bad_decisions(game['ai2_moves'])
            bad_decisions[3] += get_bad_decisions(game['human_moves'])

        if 0 in total_decisions:
            # This is needed to prevent 0 division errors.
            return [0, 0, 0, 0]

        success_percentages: list[float] = []
        for i in range(4):
            # 100 * bad / total gives the percentage of bad decisions.
            # Therefore, 100 - 100 * bad / total gives the percentage of success.
            success_percentages.append(
                100 - 100 * bad_decisions[i] / total_decisions[i]
            )
        return success_percentages

    def get_stand_values(self) -> list[list[int]]:
        '''
        Returns a list of stand values per player of every game.
        '''

        def get_stand_value(moves_list: list[Any]) -> int:
            for i in range(0, len(moves_list), 2):
                if moves_list[i] == 'S':
                     return moves_list[i + 1]
            return moves_list[-1]

        croupier_s_v: list[int] = []
        ai1_s_v: list[int] = []
        ai2_s_v: list[int] = []
        human_s_v: list[int] = []

        for game in self.games:
            croupier_s_v.append(get_stand_value(game['croupier_moves']))
            ai1_s_v.append(get_stand_value(game['ai1_moves']))
            ai2_s_v.append(get_stand_value(game['ai2_moves']))
            human_s_v.append(get_stand_value(game['human_moves']))

        return [croupier_s_v, ai1_s_v, ai2_s_v, human_s_v]
