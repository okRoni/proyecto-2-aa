from random import choice, randint
from .socketio_setup import socketio
from .entities.player import AiPlayer, Crupier, Player, HumanPlayer
from .entities.deck import Deck
from .statistics_logger import StatisticsLogger
import eventlet

def test_function():
  '''
  This function is called when the user clicks the "Start Test" button on the web page.
  It simulates a game of blackjack, where two AI players play against the dealer (Crupier).
  The game is played using the logic implemented in the entities and logic modules.
  The game state is updated on the web page using Flask-Socket
  '''

  deck : Deck = Deck.getDeck()
  crupier : Crupier = Crupier()
  aiPlayer1 : AiPlayer = AiPlayer('ai1')
  aiPlayer2 : AiPlayer = AiPlayer('ai2')
  humanPlayer : HumanPlayer = HumanPlayer()
  statsLogger : StatisticsLogger = StatisticsLogger.getLogger()

  players : list[Player] = [aiPlayer1, humanPlayer ,aiPlayer2]

  # initial render
  for player in players:
    player.renderOnWeb()
  crupier.renderOnWeb(True)
  eventlet.sleep(0.5)

  # deal cards
  for player in players:
    player.add_card_to_hand()
    player.renderOnWeb()
    eventlet.sleep(0.5)
    player.add_card_to_hand()
    player.renderOnWeb()
    eventlet.sleep(0.5)
  crupier.add_card_to_hand()
  crupier.renderOnWeb(True)
  eventlet.sleep(0.5)
  crupier.add_card_to_hand()
  crupier.renderOnWeb(True)
  eventlet.sleep(0.5)

  # Players make their moves
  for player in players:
    done = False
    while not done:
      player.make_move()
      if player.is_busted():
        done = True
      if player.is_standing():
        done = True
      player.renderOnWeb()
      eventlet.sleep(1)

  # show cruiper's second card
  crupier.renderOnWeb()
  eventlet.sleep(1)

  # crupier makes its move
  done = False
  while not done:
    crupier.make_move()
    if crupier.is_busted():
      done = True
    if crupier.is_standing():
      done = True
    crupier.renderOnWeb()
    eventlet.sleep(1)
  
  # determine the winner
  for player in players:
    player.renderOnWeb()
  crupier.renderOnWeb()

  socketio.emit('game-over', get_results_for_players(players, crupier))

def get_results_for_players(players : list[Player], crupier : Crupier) -> dict:
  '''
  Determines the winner of the game based on the players' and crupier's hands.
  Returns a dictionary with the winner and the results for each player.
  '''
  results = {}
  for player in players:
    if player.is_busted():
      results[player.position] = 'busted'
    elif crupier.is_busted():
      results[player.position] = 'win'
    elif player.get_hand_value() > crupier.get_hand_value():
      results[player.position] = 'win'
    elif player.get_hand_value() == crupier.get_hand_value():
      results[player.position] = 'draw'
    else:
      results[player.position] = 'lose'

  return results