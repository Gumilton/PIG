import numpy as np


class PlayerRandom():

    def __init__(self, name=str(np.random.random_integers(10))):
        self.name = name
        self.cards = []
        self.collected_cards = []
        self.collected_value_cards = []

    def add_cards(self, card_list):
        self.cards = sorted(card_list)
        self.collected_cards = []
        self.collected_value_cards = []

    def get_name(self):
        return self.name

    def get_holding_cards(self):
        return self.cards

    def show_card(self, **kwargs):
        return []

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

    def render(self, shown_cards, previous, **kwargs):
        lead_card = None if len(previous) == 0 else previous[0]
        available_choices = self._get_available_choices(shown_cards, lead_card)
        card = np.random.choice(available_choices)
        self.cards.remove(card)
        return card

    def collect(self, cards, **kwargs):
        self.collected_cards.extend(cards)

    def collect_value_cards(self, card, **kwargs):
        self.collected_value_cards.append(card)