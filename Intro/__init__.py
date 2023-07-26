from otree.api import *
import numpy as np
import random
from random import choice as random_draw

doc = """
Read quiz quest 
"""

class C(BaseConstants):
    NAME_IN_URL = 'Intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    import itertools
    carbonLeftCycle = itertools.cycle([True, True,  False, False])
    outcomeOneTopCycle = itertools.cycle([False, True, False, True])
    for player in subsession.get_players():
        if subsession.round_number == 1:
            if 'carbonLeft' in player.session.config:
                player.participant.carbonLeft = player.session.config['carbonLeft']
            else:
                player.participant.carbonLeft = next(carbonLeftCycle) 
            if 'outcomeOneTop' in player.session.config:
                player.participant.outcomeOneTop = player.session.config['outcomeOneTop']
            else:
                player.participant.outcomeOneTop = next(outcomeOneTopCycle)     


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    dataScience = models.BooleanField(initial=False)
    dataTeach = models.BooleanField(initial=False)
    



class Consent(Page):
    form_model = 'player'
    #form_fields = ["dataScience","dataTeach"]

class Introduction(Page):
    form_model = 'player'
 
page_sequence = [Consent, Introduction]
