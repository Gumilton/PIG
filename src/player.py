import numpy as np


class PlayerRandom():

    def __init__(self):
        self.cards = []
        self.collected_cards = []

    def add_cards(self, card_list):
        self.cards = sorted(card_list)
        self.collected_cards = []

    def re_add(self, card):
        self.cards.append(card)

    def _get_available_choices(self, shown_cards, lead_card):
        if lead_card is None:
            return self.cards

        available_choices = []
        type = lead_card // 13
        for card in self.cards:
            if card // 13 == type:
                available_choices.append(card)

        if len(available_choices) == 0:
            return self.cards

        if len(available_choices) > 1:
            for shown_card in shown_cards:
                if shown_card in available_choices:
                    available_choices.remove(shown_card)

        return available_choices

    def render(self, shown_cards, lead_card, previous=None):
        available_choices = self._get_available_choices(shown_cards, lead_card)
        card = np.random.choice(available_choices)
        self.cards.remove(card)
        return card

    def collect(self, cards):
        self.collected_cards.extend(cards)