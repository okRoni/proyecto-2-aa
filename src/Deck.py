from Card import Card


class Deck:
    """ Class that represents a deck of cards of a blackjack game. """

    def __init__(self) -> None:
        self.cards: list[Card] = [
            Card(2, '2_of_clubs.png', 0),
            Card(2, '2_of_diamonds.png', 1),
            Card(2, '2_of_hearts.png', 1),
            Card(2, '2_of_spades.png', 0),
            Card(3, '3_of_clubs.png', 0),
            Card(3, '3_of_diamonds.png', 1),
            Card(3, '3_of_hearts.png', 1),
            Card(3, '3_of_spades.png', 0),
            Card(4, '4_of_clubs.png', 0),
            Card(4, '4_of_diamonds.png', 1),
            Card(4, '4_of_hearts.png', 1),
            Card(4, '4_of_spades.png', 0),
            Card(5, '5_of_clubs.png', 0),
            Card(5, '5_of_diamonds.png', 1),
            Card(5, '5_of_hearts.png', 1),
            Card(5, '5_of_spades.png', 0),
            Card(6, '6_of_clubs.png', 0),
            Card(6, '6_of_diamonds.png', 1),
            Card(6, '6_of_hearts.png', 1),
            Card(6, '6_of_spades.png', 0),
            Card(7, '7_of_clubs.png', 0),
            Card(7, '7_of_diamonds.png', 1),
            Card(7, '7_of_hearts.png', 1),
            Card(7, '7_of_spades.png', 0),
            Card(8, '8_of_clubs.png', 0),
            Card(8, '8_of_diamonds.png', 1),
            Card(8, '8_of_hearts.png', 1),
            Card(8, '8_of_spades.png', 0),
            Card(9, '9_of_clubs.png', 0),
            Card(9, '9_of_diamonds.png', 1),
            Card(9, '9_of_hearts.png', 1),
            Card(9, '9_of_spades.png', 0),
            Card(10, '10_of_clubs.png', 0),
            Card(10, '10_of_diamonds.png', 1),
            Card(10, '10_of_hearts.png', 1),
            Card(10, '10_of_spades.png', 0),
            Card(10, 'jack_of_clubs.png', 0),
            Card(10, 'jack_of_diamonds.png', 1),
            Card(10, 'jack_of_hearts.png', 1),
            Card(10, 'jack_of_spades.png', 0),
            Card(10, 'queen_of_clubs.png', 0),
            Card(10, 'queen_of_diamonds.png', 1),
            Card(10, 'queen_of_hearts.png', 1),
            Card(10, 'queen_of_spades.png', 0),
            Card(10, 'king_of_clubs.png', 0),
            Card(10, 'king_of_diamonds.png', 1),
            Card(10, 'king_of_hearts.png', 1),
            Card(10, 'king_of_spades.png', 0),
            Card(11, 'ace_of_clubs.png', 0),
            Card(11, 'ace_of_diamonds.png', 1),
            Card(11, 'ace_of_hearts.png', 1),
            Card(11, 'ace_of_spades.png', 0)
        ]
        