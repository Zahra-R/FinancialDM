from otree.api import *
import numpy as np
import random
from random import choice as draw_random_number
import csv

doc = """
Read quiz quest 
"""


def read_csvC():
    f = open(__name__ + '/stimuliC.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    return rows


def read_csvU():
    f = open(__name__ + '/stimuliU.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    print("new print with rows")
    return rows




class C(BaseConstants):
    NAME_IN_URL = 'fdmchoice'
    PLAYERS_PER_GROUP = None
    QUESTIONS_C = read_csvC()
    QUESTIONS_U = read_csvU()
    #NUM_ROUNDS = 16
    NUM_ROUNDS =  len(QUESTIONS_C) + len(QUESTIONS_U)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        player.certainFirst = player.participant.certainFirst
        if subsession.round_number == 1:
            ######### this is for the bonus payoff later on ########
            # 1 to 4 is practice ; 5 to 84 is part 1, 85 to 88 is practice, 89 to 164 is part 2) 
            seqa = range(5,85)
            print("seqa", seqa)
            seqb = range(89,165)
            seq = np.concatenate((seqa, seqb), axis = None)
            print("seq", seq)
            # this next line needs to be removed, was only for practice purposes
            #seq = [1,2,3,4]
            player.drawn_round = int(draw_random_number(seq))
            #############################################
            shuffledOrderC = np.arange(start = 4, stop=  len(C.QUESTIONS_C), step = 1) 
            random.shuffle(shuffledOrderC)
            print(shuffledOrderC)
            player.participant.shuffledOrderC = np.concatenate((range(0,4), shuffledOrderC), axis = None )
            print("this should be the entire sequence of trial ids ", player.participant.shuffledOrderC)
            print(len(player.participant.shuffledOrderC))
            shuffledOrderU = np.arange(start= 4, stop = len(C.QUESTIONS_U) , step = 1) 
            random.shuffle(shuffledOrderU)
            print(shuffledOrderU)
            player.participant.shuffledOrderU = np.concatenate((range(0,4), shuffledOrderU), axis = None)
            print("this should be the entire sequence of trial ids ", player.participant.shuffledOrderU)
            print(len(player.participant.shuffledOrderC))
            print("this is num rounds", C.NUM_ROUNDS)
        if player.participant.certainFirst == False:
            player.mod_round_number = (( subsession.round_number + int(C.NUM_ROUNDS/2) ) % C.NUM_ROUNDS)
            if player.mod_round_number == 0:
                player.mod_round_number = C.NUM_ROUNDS
        else: 
            player.mod_round_number = subsession.round_number
        print("subsession round number ", subsession.round_number-1)
        print("mod rd", player.mod_round_number)
        if player.mod_round_number <= int(C.NUM_ROUNDS/2): 
            #print("first if current Question index", player.participant.shuffledOrderC[((subsession.round_number) % (int(C.NUM_ROUNDS/2)))-1], subsession.round_number)
            current_questionC = C.QUESTIONS_C[player.participant.shuffledOrderC[((subsession.round_number) % (int(C.NUM_ROUNDS/2)))-1]]
            player.moneyA =  int(current_questionC['moA'])
            player.moneyB = int(current_questionC['moB'])
            player.carbonA = int(current_questionC['coA'])
            player.carbonB = int(current_questionC['coB'])
            player.stimulusIDC = int(current_questionC['sid'])
            player.OptionARight = draw_random_number([0, 1])
            player.practice = current_questionC['practice']
        else:
            #print(" else current Question index", player.participant.shuffledOrderU[((subsession.round_number) % (int(C.NUM_ROUNDS/2)))-1], subsession.round_number)
            current_questionU = C.QUESTIONS_U[player.participant.shuffledOrderU[(subsession.round_number) % (int(C.NUM_ROUNDS/2))-1]]
            player.moneyA1 = int(current_questionU['moA1'])
            player.moneyA2 = int(current_questionU['moA2'])
            player.carbonA1 = int(current_questionU['coA1'])
            player.carbonA2 = int(current_questionU['coA2'])
            player.probA1 = 100* float(current_questionU['pA1'])
            player.probA2 = 100* float(current_questionU['pA2'])
            #player.probA2 = 100 -  (100* float(current_questionU['pA1']))
            
            player.moneyB1 = int(current_questionU['moB1'])
            player.moneyB2 = int(current_questionU['moB2'])
            player.carbonB1 = int(current_questionU['coB1'])
            player.carbonB2 = int(current_questionU['coB2'])
            player.probB1 =   100* float(current_questionU['pB1'])
            player.probB2 =   100* float(current_questionU['pB2'])
            #player.probB2 = 100 - (100* float(current_questionU['pB1']))
            player.OptionAoutcomeOneTop = draw_random_number([True, False])
            player.OptionBoutcomeOneTop = draw_random_number([True, False])
            player.practice = current_questionU['practice']
            
            player.stimulusIDU = int(current_questionU['sid'])
            player.OptionARight = draw_random_number([0, 1])




class Group(BaseGroup):
    pass

def make_field(label):
        return models.IntegerField(
            choices=[1,2,3,4,5],
            label=label,
            widget=widgets.RadioSelect,
            )


class Player(BasePlayer):
    mod_round_number = models.IntegerField()
    practice = models.StringField()
    stimulusIDC = models.IntegerField()
    stimulusIDU = models.IntegerField()

    moneyA = models.IntegerField()
    moneyB = models.IntegerField()
    carbonA = models.IntegerField()
    carbonB = models.IntegerField()
    choice = models.StringField()
    

    moneyA1 = models.IntegerField()
    moneyA2 = models.IntegerField()
    moneyB1 = models.IntegerField()
    moneyB2 = models.IntegerField()
    carbonA1 = models.IntegerField()
    carbonA2 = models.IntegerField()
    carbonB1 = models.IntegerField()
    carbonB2 = models.IntegerField()
    probA1 = models.FloatField() 
    probA2 = models.FloatField()
    probB1 = models.FloatField()
    probB2 = models.FloatField()


    input_keyboard = models.IntegerField()
    timedout = models.BooleanField(default=False)
    page_load = models.StringField(initial = '0', default = '0')
    page_submit = models.StringField(null=True)
    responsetime = models.IntegerField()
    OptionARight = models.IntegerField()
    newResponseTime = models.FloatField()
    carbonLeft = models.BooleanField()
    certainFirst = models.BooleanField()
    OptionAoutcomeOneTop = models.BooleanField()
    OptionBoutcomeOneTop = models.BooleanField()


    drawn_round = models.IntegerField()
    outcome_bonus_points = models.FloatField()
    outcome_carbon = models.FloatField()
    outcome_bonus_pound = models.FloatField()

    comprehensions_C1 = models.StringField(choices=[ [1, "15 lbs. CO2"], [2, "30 lbs. CO2"], [3, "50 lbs. CO2"]], label ="Which amount of carbon would be emitted if you chose Option B?",  widget = widgets.RadioSelect )
    comprehensions_C2 = models.StringField(choices=[[1, "$20"], [2,"$45"], [3, "$50"]], label ="What is the highest monetary amount you can get in this choice situation? ",  widget = widgets.RadioSelect )
    comprehensions_U1 = models.StringField(choices=[ [1, "45 lbs. CO2"], [2, "50 lbs. CO2"], [3, "55 lbs. CO2"]], label ="What is the maximum amount of carbon that could be emitted if you chose Option A?",  widget = widgets.RadioSelect )
    comprehensions_U2 = models.StringField(choices=[[1, "30%"], [2,"50%"], [3, "70%"]], label ="What is the probability of receiving a monetary bonus of $40 when you choose Option A?",  widget = widgets.RadioSelect )

   

    ccc1 = make_field('We must protect the climate’s delicate equilibrium.') ## concern 4 items
    ccc2 = make_field('Climate protection is important for our future.')
    ccc3 = make_field('I worry about the climate’s state.')
    ccc4 = make_field('Climate change has severe consequences for humans and nature.')
    ccc5 = make_field('Climate protection measures are determined by a few powerful persons; as a single citizen, I have no effect.') ## powerlessness 5 items
    ccc6 = make_field('With my behavior, I cannot influence the climate, as, in fact, it rests in the hands of the industry.')
    ccc7 = make_field('As an ordinary citizen, I can influence governmental decisions regarding climate protection.')
    ccc8 = make_field('I feel able to contribute to climate protection.')
    ccc9 = make_field('If I tried to behave in a climate-friendly way, that would surely have a positive effect on the climate.')
    ccc10 = make_field('Climate change and its consequences are being exaggerated in the media.')     ### skepticism 7 items 
    ccc11 = make_field('Climate change is a racket.')
    ccc12 = make_field('As long as meteorologists are not even able to accurately forecast weather, climate cannot be reliably predicted either.')
    ccc13 = make_field('There are larger problems than climate protection.')
    ccc14 = make_field('I do not feel threatened by climate change.')
    ccc15 = make_field('The impacts of climate change are unpredictable; thus, my climate-friendly behavior is futile.')
    ccc16 = make_field('Climate protection needlessly impedes economic growth.')

    prolific_id = models.StringField()

    # @property
    # def response_time(player):
    #     if player.page_submit != None:
    #         return player.page_submit - player.page_load
        

class InstructionC1(Page): 
    form_model = 'player'
    form_fields = ["comprehensions_C1", "comprehensions_C2"]
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'carbonLeft': player.participant.carbonLeft,
            'modRoundNumber': player.mod_round_number,
            'totalRounds': C.NUM_ROUNDS
        }
    @staticmethod
    def is_displayed(player: Player):
        #show = (player.participant.certainFirst & player.round_number <=80) | (not player.participant.certainFirst & player.round_number >80 )
        return player.mod_round_number == 1
    

class InstructionU1(Page): 
    form_model = 'player'
    form_fields = ["comprehensions_U1", "comprehensions_U2"]
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'carbonLeft': player.participant.carbonLeft,
            'modRoundNumber': player.mod_round_number,
            'totalRounds': C.NUM_ROUNDS,
            'halftotalRounds': int(C.NUM_ROUNDS/2)
        }
    @staticmethod
    def is_displayed(player: Player):
        return player.mod_round_number -1  == int(C.NUM_ROUNDS/2)
    
    
                   

class InstructionC2(Page): 
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        Q1correct = True if player.comprehensions_C1 == "3" else False
        Q2correct = True if  player.comprehensions_C2 == "2" else False
        player.participant.comprehension_C1_correct = Q1correct
        player.participant.comprehension_C2_correct = Q2correct
        bothcorrect = True if (Q1correct == True) & (Q2correct == True) else False
        nonecorrect = True if (Q1correct == False) & (Q2correct == False) else False
        return {
            'Q1correct': Q1correct, 
            'Q2correct': Q2correct,
            'bothcorrect': bothcorrect,
            'nonecorrect': nonecorrect,
            'carbonLeft': player.participant.carbonLeft
        }
    @staticmethod
    def is_displayed(player: Player):
        return player.mod_round_number == 1
    
                  

class InstructionU2(Page): 
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        Q1correct = True if player.comprehensions_U1 == "1" else False
        Q2correct = True if  player.comprehensions_U2 == "1" else False
        player.participant.comprehension_U1_correct = Q1correct
        player.participant.comprehension_U2_correct = Q2correct
        bothcorrect = True if (Q1correct == True) & (Q2correct == True) else False
        nonecorrect = True if (Q1correct == False) & (Q2correct == False) else False
        return {
            'Q1correct': Q1correct, 
            'Q2correct': Q2correct,
            'bothcorrect': bothcorrect,
            'nonecorrect': nonecorrect,
            'carbonLeft': player.participant.carbonLeft
        }
    @staticmethod
    def is_displayed(player: Player):
        return player.mod_round_number -1 == int(C.NUM_ROUNDS/2)
    

class choiceTaskC(Page):
    form_model = 'player'
    form_fields = ["choice","input_keyboard", "page_load", "page_submit", "newResponseTime"]
    @staticmethod
    def vars_for_template(player: Player):
        print("--------------------------HIiiiiiiii------------")
        print(player.mod_round_number)
        print(player.participant.certainFirst)
        player.carbonLeft = player.participant.carbonLeft
        player.prolific_id = player.participant.participant_label
        return {
            'reverse': player.OptionARight,
            'carbonLeft': player.participant.carbonLeft,
            'game_round': player.round_number,
            'modRoundNumber': player.mod_round_number,
            'totalRounds': C.NUM_ROUNDS,
            'halftotalRounds': int(C.NUM_ROUNDS/2)
        }
    @staticmethod
    def before_next_page(player, timeout_happened):
        print("made it till here")
        if player.page_submit != None:
            player.responsetime = int(player.page_submit) - int(player.page_load)
    @staticmethod
    def is_displayed(player: Player):
        #show = (player.participant.certainFirst & player.round_number <=80) | (not player.participant.certainFirst & player.round_number >80 )
        return player.mod_round_number <= int(C.NUM_ROUNDS/2)


   
class choiceTaskU(Page):
    form_model = 'player'
    #form_fields = ["choice","input_keyboard", "page_load", "page_submit"]
    form_fields = ["choice","input_keyboard", "page_load", "page_submit", "newResponseTime"]
    @staticmethod
    def vars_for_template(player: Player):
        print("--------------------------Uuuuuuuuuncertain------------")
        print(player.mod_round_number)
        print(player.participant.certainFirst)
        player.carbonLeft = player.participant.carbonLeft
        player.prolific_id = player.participant.label
        return {
            'reverse': player.OptionARight,
            'carbonLeft': player.participant.carbonLeft,
            'AoutcomeOneTop': player.OptionAoutcomeOneTop,
            'BoutcomeOneTop': player.OptionBoutcomeOneTop,
            'game_round': player.round_number, 
            'modRoundNumber': player.mod_round_number,
            'totalRounds': C.NUM_ROUNDS,
            'halftotalRounds': int(C.NUM_ROUNDS/2)
        }
    @staticmethod
    def before_next_page(player, timeout_happened):
        print("made it till here")
        if player.page_submit != None:
            player.responsetime = int(player.page_submit) - int(player.page_load)
    @staticmethod
    def is_displayed(player: Player):
        return player.mod_round_number > int(C.NUM_ROUNDS/2)
    


class betweenGames(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number == int(C.NUM_ROUNDS/2)
        )  

class afterPractice(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number %(int(C.NUM_ROUNDS/2)) == 4
        )



class questionnaire(Page):
    form_model = 'player'
    form_fields= ['ccc1', 'ccc2', 'ccc3', 'ccc4','ccc5', 'ccc6', 'ccc7', 'ccc8',  'ccc9', 'ccc10', 'ccc11', 'ccc12', 'ccc13', 'ccc14', 'ccc15', 'ccc16'  ]
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS



def outcome_certain(player: Player, drawn_round):
    round_choice = player.in_round(drawn_round).choice 
    if round_choice == "A":
        outcome_bonus_points = player.in_round(drawn_round).moneyA
        outcome_carbon = player.in_round(drawn_round).carbonA
    else: 
        outcome_bonus_points = player.in_round(drawn_round).moneyB
        outcome_carbon = player.in_round(drawn_round).carbonB

    ### recode for participants if what they saw was reversed  
    if player.in_round(drawn_round).OptionARight == 1 :
        if round_choice == "A":
            round_choice = "B"
        else: 
            round_choice = "A"
    return round_choice, outcome_bonus_points, outcome_carbon


def outcome_risky(player:Player, drawn_round):
    round_choice = player.in_round(drawn_round).choice 
    if round_choice == "A":
        rnd = random.random()
        if rnd < player.in_round(drawn_round).probA1:
            outcome_bonus_points = player.in_round(drawn_round).moneyA1
            outcome_carbon = player.in_round(drawn_round).carbonA1
        else:
            outcome_bonus_points = player.in_round(drawn_round).moneyA2
            outcome_carbon = player.in_round(drawn_round).carbonA2

    else: 
        rnd = random.random()
        if rnd < player.in_round(drawn_round).probB1:
            outcome_bonus_points = player.in_round(drawn_round).moneyB1
            outcome_carbon = player.in_round(drawn_round).carbonB1
        else:
            outcome_bonus_points = player.in_round(drawn_round).moneyB2
            outcome_carbon = player.in_round(drawn_round).carbonB2
    
    ### recode for participants if what they saw was reversed  
    if player.in_round(drawn_round).OptionARight == 1 :
        if round_choice == "A":
            round_choice = "B"
        else: 
            round_choice = "A"
    return round_choice, outcome_bonus_points, outcome_carbon


class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        sum_correct = player.participant.comprehension_C1_correct + player.participant.comprehension_C2_correct +player.participant.comprehension_U1_correct + player.participant.comprehension_U2_correct
        drawn_round = player.in_round(1).drawn_round
        drawn_game= "certain"
        if drawn_round > int(C.NUM_ROUNDS/2) and player.participant.certainFirst == True:
            drawn_game = "risky"
        if drawn_round <= int(C.NUM_ROUNDS/2) and player.participant.certainFirst == False:
            drawn_game = "risky"
        if(drawn_game == "risky"):
            relevant_round_choice, player.outcome_bonus_points, player.outcome_carbon = outcome_risky(player, drawn_round)
        else:
            relevant_round_choice, player.outcome_bonus_points, player.outcome_carbon = outcome_certain(player, drawn_round)
        if sum_correct >= 3:
            player.outcome_bonus_pound = player.outcome_bonus_points / 25
        else:
            player.outcome_bonus_pound = 0
        drawn_block = 1
        if drawn_round > int(C.NUM_ROUNDS/2):
            drawn_round_display = drawn_round - C.NUM_ROUNDS/2
            drawn_block = 2
        return{
            'drawn_round': drawn_round_display,
            'drawn_block': drawn_block,
            'drawn_game': drawn_game,
            'relevant_round_choice': relevant_round_choice,
            'outcome_bonus_points': player.outcome_bonus_points,
            'outcome_bonus_pound': player.outcome_bonus_pound,
            'outcome_carbon': player.outcome_carbon,
            'sum_correct': sum_correct
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    

page_sequence = [ InstructionC1, InstructionC2, InstructionU1, InstructionU2, choiceTaskU, choiceTaskC, afterPractice, betweenGames, questionnaire, Results]
