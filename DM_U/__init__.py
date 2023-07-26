from otree.api import *
import numpy as np
import random
from random import choice as random_draw

doc = """
Read quiz quest 
"""


def read_csv():
    import csv

    f = open(__name__ + '/stimuliU.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    return rows


class C(BaseConstants):
    NAME_IN_URL = 'riskychoice'
    PLAYERS_PER_GROUP = None
    QUESTIONS_U = read_csv()
    NUM_ROUNDS = len(QUESTIONS_U)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if subsession.round_number == 1:
            shuffledOrderU = np.arange(len(C.QUESTIONS_U)) 
            random.shuffle(shuffledOrderU)
            player.participant.shuffledOrderU = shuffledOrderU   
        current_question = C.QUESTIONS_U[player.participant.shuffledOrderU[subsession.round_number-1]]
        print(current_question)
        player.moneyA1 = current_question['moA1']
        player.moneyA2 = current_question['moA2']
        player.carbonA1 = current_question['coA1']
        player.carbonA2 = current_question['coA2']
       
        player.probB1 = current_question['pB1']
        player.moneyB1 = current_question['moB1']
        player.moneyB2 = current_question['moB2']
        player.carbonB1 = current_question['coB1']
        player.carbonB2 = current_question['coB2']
        player.probB1 = current_question['pB1']
        
        player.stimulusID = current_question['sid']
        player.reverse = random_draw([0, 1])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    moneyA1 = models.IntegerField()
    moneyA2 = models.IntegerField()
    moneyB1 = models.IntegerField()
    moneyB2 = models.IntegerField()
    carbonA1 = models.IntegerField()
    carbonA2 = models.IntegerField()
    carbonB1 = models.IntegerField()
    carbonB2 = models.IntegerField()
    probA1 = models.FloatField()
    probB1 = models.FloatField()
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


page_sequence = [choiceTask]
