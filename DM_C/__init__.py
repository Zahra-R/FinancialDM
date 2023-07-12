from otree.api import *
import numpy as np
import random
from random import choice as random_draw

doc = """
Read quiz quest 
"""


def read_csv():
    import csv

    f = open(__name__ + '/stimuliC.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    return rows


class C(BaseConstants):
    NAME_IN_URL = 'questions_from_csv_simple'
    PLAYERS_PER_GROUP = None
    QUESTIONS = read_csv()
    NUM_ROUNDS = len(QUESTIONS)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if subsession.round_number == 1:
            shuffledOrder = np.arange(C.NUM_ROUNDS)
            random.shuffle(shuffledOrder)
            player.participant.shuffledOrder = shuffledOrder
        current_question = C.QUESTIONS[player.participant.shuffledOrder[subsession.round_number-1]]
        player.moneyA = current_question['moA']
        player.moneyB = current_question['moB']
        player.carbonA = current_question['coA']
        player.carbonB = current_question['coB']
        player.stimulusID = current_question['sid']
        player.reverse = random_draw([0, 1])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    moneyA = models.IntegerField()
    moneyB = models.IntegerField()
    carbonA = models.IntegerField()
    carbonB = models.IntegerField()
    choice = models.StringField()
    input_keyboard = models.IntegerField()
    timedout = models.BooleanField(default=False)
    page_load = models.IntegerField(initial=0)
    page_submit = models.IntegerField(null=True)
    responsetime = models.IntegerField()
    stimulusID = models.IntegerField()
    reverse = models.IntegerField()
    @property
    def response_time(player):
        if player.page_submit != None:
            return player.page_submit - player.page_load
        
        





class choiceTask(Page):
    form_model = 'player'
    form_fields = ["choice","input_keyboard", "page_load", "page_submit"]
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'reverse': player.reverse
        }
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timedout = True
            player.choice = None
        player.responsetime = player.response_time

class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_players=player.in_all_rounds())


page_sequence = [choiceTask, Results]
