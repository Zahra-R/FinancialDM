from otree.api import *
import numpy as np
import random
from random import choice as random_draw

doc = """
Read quiz quest 
"""

class C(BaseConstants):
    NAME_IN_URL = 'FMD_Intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    import itertools
    carbonLeftCycle = itertools.cycle([True, True,  False, False])
    certainFirstCycle = itertools.cycle([True, False])
    for player in subsession.get_players():
        if subsession.round_number == 1:
            if 'carbonLeft' in player.session.config:
                player.participant.carbonLeft = player.session.config['carbonLeft']
            else:
                player.participant.carbonLeft = next(carbonLeftCycle) 
            if 'certainFirst' in player.session.config:
                player.participant.certainFirst = player.session.config['certainFirst']
            else:
                player.participant.certainFirst = next(certainFirstCycle)     


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent1 = models.BooleanField(initial=False)
    consent2 = models.BooleanField(initial=False)
    



class Consent(Page):
    form_model = 'player'
    form_fields = ["consent1","consent2"]

class Introduction(Page):
    form_model = 'player'

class Introduction2(Page):
    form_model = 'player'
 
 
page_sequence = [Consent, Introduction, Introduction2]
