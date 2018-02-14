import numpy as np


DIGIT_DECODE = {9: "J",
                10: "Q",
                11: "K",
                12: "A"}
DIGIT_DECODE.update({i: str(i + 2) for i in range(9)})

SHAPE_DECODE = {0: "club",
                1: "spade",
                2: "diamond",
                3: "heart"}

PIG_CODE = 23
SHEEP_CODE = 35
MUL_CODE = 8
REDA_CODE = 51

SCORE_PIG = lambda x: x + 100
SCORE_SHEEP = lambda x: x - 100
SCORE_ADD = {REDA_CODE: 50,
             50: 40,
             49: 30,
             48: 20}

SCORE_ADD.update({i: 10 for i in range(42, 48, 1)})

SCORE_MUL = lambda x: x * 2

VALUE_CARDS = [23, 35, 8] + list(range(39, 52))


def reverse_dict(dic):
    return {v: k for k, v in dic.items()}


DIGIT_ENCODE = reverse_dict(DIGIT_DECODE)
SHAPE_ENCODE = reverse_dict(SHAPE_DECODE)


def get_starter_player_by_holding_card(all_cards, starter_card=0):
    return np.where(all_cards == starter_card)[0].tolist()[0] // 13


def who_get_pig(players_cards, pig_card=23):
    for pl, cards in players_cards.items():
        if 23 in cards:
            return pl


def isSameType(c1, c2):
    return c1 // 13 == c2 // 13


def who_collect(c1, c2, c3, c4):
    matched_cards = [c1]
    matched_cards.append(c2 if isSameType(c1, c2) else -1)
    matched_cards.append(c3 if isSameType(c1, c3) else -1)
    matched_cards.append(c4 if isSameType(c1, c4) else -1)
    return np.argmax(matched_cards)


def card_decode(n):
    if n < 0 or n > 51:
        raise ValueError("N must be [0,51] inclusive")
    shape = n // 13
    digit = n % 13
    return SHAPE_DECODE[shape] + "-" + DIGIT_DECODE[digit]


def decode_card_list(ns):
    return [card_decode(n) for n in ns]


def card_encode(card):
    shape, digit = card.split("-")
    # if shape in SHAPE_ENCODE and digit in DIGIT_ENCODE:
    return SHAPE_ENCODE[shape] * 13 + DIGIT_ENCODE[digit]
    # else:
    #     raise KeyError("Card name definition error")


def encode_card_list(cards):
    return [card_encode(card) for card in cards]


def all_heart(cards):
    for i in range(39, 52, 1):
        if i not in cards:
            return False
    return True


def all_collected(cards):
    if len(cards) < 16:
        return False

    if all_heart(cards):
        if 8 in cards:
            if 23 in cards:
                if 35 in cards:
                    return True
    return False


def calculate_scores(player_cards, shown_cards):
    scores = {pl: {PIG_CODE: 0, SHEEP_CODE: 0, MUL_CODE: 1, REDA_CODE: 0}
            for pl in player_cards}

    for pl, cards in player_cards.items():
        if all_collected(cards):
            pig = 200 if PIG_CODE in shown_cards else 100
            sheep = 200 if SHEEP_CODE in shown_cards else 100
            heart = 400 if REDA_CODE in shown_cards else 200
            mul = 4 if MUL_CODE in shown_cards else 2
            score = (pig + sheep + heart) * mul
            final_score = {p: score for p in player_cards}
            final_score[pl] = 0
            return final_score

        for card in cards:
            if card == PIG_CODE:
                scores[pl][PIG_CODE] = 200 if card in shown_cards else 100
            elif card == SHEEP_CODE:
                scores[pl][SHEEP_CODE] = -200 if card in shown_cards else -100
            elif card == MUL_CODE:
                scores[pl][MUL_CODE] = 4 if card in shown_cards else 2
            elif card in SCORE_ADD:
                scores[pl][REDA_CODE] += SCORE_ADD[card]

        if REDA_CODE in shown_cards:
            scores[pl][REDA_CODE] *= 2

        if all_heart(cards):
            scores[pl][REDA_CODE] *= -1

    return {pl: (score_dict[PIG_CODE] + score_dict[SHEEP_CODE] + score_dict[REDA_CODE]) * score_dict[MUL_CODE]
            for pl, score_dict in scores.items()}

