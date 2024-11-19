class Card:
    """ Class that represents a card of a blackjack game. """

    def __init__(self, value: int, filename: str, color: int) -> None:
        self.value = value
        self.filename = filename
        self.color = color  # Color 0: black. Color 1: red.

    def __str__(self) -> str:
        return f'{self.value}'
    
    def to_dict(self) -> dict:
        return {
            'value': self.value,
            'filename': self.filename,
            'color': self.color
        }
