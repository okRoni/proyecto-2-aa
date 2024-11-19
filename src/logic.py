from random import choice, randint
from .socketio_setup import socketio
from .entities.player import AiPlayer, Crupier, Player
from .entities.deck import Deck
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

  players : list[Player] = [aiPlayer1, aiPlayer2]

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



  

