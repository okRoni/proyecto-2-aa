from random import randint
from card import Card


class Deck:
    """ Class that represents a deck of cards of a blackjack game. """
    
    instance = None # Shared instance of the deck (it works as our global variable)

    @staticmethod
    def getDeck():
        '''
        Returns the shared instance of the deck.
        If the instance does not exist, it creates one.
        '''
        if Deck.instance == None:
            Deck.instance = Deck()
        return Deck.instance
        

    def __init__(self) -> None:
        # This list contains all 52 cards of a standard deck
        self.unshown_cards: list[Card] = [
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
        self.shown_cards: list[Card] = []

        # 6 full decks are going to be used, that is, 6 of every card
        for i in range(52):
            self.unshown_cards += [self.unshown_cards[i] for _ in range(5)]

    def get_random_card(self) -> Card:
        """
        Picks a random card and returns it. Also moves
        the card from unshown_cards to shown_cards.
        """

        card_index = randint(0, len(self.unshown_cards) - 1)
        try:
            card = self.unshown_cards[card_index]
            del self.unshown_cards[card_index]
        except IndexError:
            raise IndexError('Tried to get a card from a empty deck.')

        self.shown_cards.append(card)
        return card

    def reset(self) -> None:
        '''
        Puts all cards in unshown_cards.
        '''

        self.unshown_cards += self.shown_cards
        self.shown_cards = []
        if len(self.unshown_cards) != 6 * 52:
            print('Something strange happened. A card was stolen. See Deck.')

    def __len__(self) -> int:
        """
        Returns the amount of unshown cards.
        """

        return len(self.unshown_cards)
