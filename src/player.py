import numpy as np
from utils import *

class PlayerRandom:

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

    def _get_available_choices(self, shown_cards, lead_card, game_round):
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

    def render(self, shown_cards, previous, game_round, **kwargs):
        lead_card = None if len(previous) == 0 else previous[0]
        available_choices = self._get_available_choices(shown_cards, lead_card, game_round)
        card = np.random.choice(available_choices)
        self.cards.remove(card)
        return card

    def collect(self, cards, **kwargs):
        self.collected_cards.extend(cards)

    def collect_value_cards(self, card, **kwargs):
        self.collected_value_cards.append(card)


class PlayerHuman(PlayerRandom):

    def formulate_display(self, card_numbers):
        return str(dict(zip(card_numbers, decode_card_list(card_numbers))))

    def add_cards(self, card_list):
        self.cards = sorted(card_list)
        self.collected_cards = []
        self.collected_value_cards = []
        print("Player", self.name, "Get cards:\n" + self.formulate_display(self.cards))

    def show_card(self, **kwargs):
        availables = []
        for card in [PIG_CODE, SHEEP_CODE, MUL_CODE, REDA_CODE]:
            if card in self.cards:
                availables.append(card)

        if len(availables) > 0:
            decision = None
            while decision is None:
                choice = input("Available choices:" + self.formulate_display(availables) +
                               "\n Enter the number to show, separate by comma or press Enter to continue")
                if choice == '':
                    print("Decided not to show any.")
                    return []

                else:
                    try:
                        decision = []
                        choice = [int(x) for x in choice.split(",")]
                        for c in choice:
                            if c not in availables:
                                raise Exception
                            else:
                                decision.append(c)
                    except:
                        decision = None
                        print("Selection Error! Redo.")
            return decision

        else:
            print("Player", self.name, "No card to show")
            return []

    def render(self, shown_cards, previous, game_round, **kwargs):
        lead_card = None if len(previous) == 0 else previous[0]
        available_choices = self._get_available_choices(shown_cards, lead_card, game_round)
        card = None
        while card is None:
            print("Previous Component cards:" + self.formulate_display(previous))
            choice = input("Available choices:" + self.formulate_display(available_choices) +
                               "\n Enter the number to render your card")
            try:
                card = int(choice)
            except:
                card = None

            if card not in available_choices:
                card = None
                print("Selection Error! Redo.")

        self.cards.remove(card)
        return card

    def collect(self, cards, **kwargs):
        print("Player", self.name, "Get cards", self.formulate_display(cards))
        self.collected_cards.extend(cards)

    def collect_value_cards(self, card, **kwargs):
        # print("Player", self.name, "Get valued cards", self.formulate_display([card]))
        self.collected_value_cards.append(card)