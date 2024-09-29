import random
import json
import itertools
import time
from otree.api import *
import numpy as np

doc = """
risk
Lukas Bolte: lukas.bolte@outlook.com. 
"""


class C(BaseConstants):
    NAME_IN_URL = 'risk'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    APPROX_TIME = "30-40 minutes"
    AVG_TOTAL_PAYMENT = "$16"
    PARTICIPATION_FEE = 5
    ROW_PAYMENT = 25
    BELIEF_BONUS = 1
    WORK_PERIOD_LENGTH = 10

    INSTRUCTIONS_BELIEFS = 'otfe/Review-instructionsBeliefs.html'
    INSTRUCTIONS = 'otfe/Review-instructions.html'
    INSTRUCTIONS2 = 'otfe/Review-instructions2.html'
    TAX_INSTRUCTIONS = 'otfe/Review-instructionsTax.html'

class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:

        treatments = ['C-Info','C-NoInfo', 'T1-T-Info', 'T1-T-NoInfo','T1-P','T2-T']
        
        # random.shuffle(treatments)
        treatments = itertools.cycle(treatments)

        i=1
        for p in subsession.get_players():
            
            el = next(treatments)
            p.participant.treatment = el

            p.participant.cq_1_mistakes = 0
            p.participant.cq_2_mistakes = 0
            p.participant.which_belief = random.choice([1,2,3])



            # p.participant.cqs_find_out_mistakes = 0
            # p.participant.cq1_who_mistakes = 0
            # p.participant.cq1_what_mistakes = 0
            # p.participant.cq1_find_out_mistakes = 0
            # p.participant.cq2_who_mistakes = 0
            # p.participant.cq2_what_mistakes = 0
            # p.participant.cq2_find_out_mistakes = 0

            print(p.participant.treatment)
            i+=1

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    data_dummy = models.StringField(blank=True)

    beliefs1 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate:</b>')
    beliefs2 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate:</b>')
    beliefs3 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate:</b>')
    beliefs4 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate:</b>')

    cq_1 = models.IntegerField(blank=True,
        choices=[
            [1, 'There is no default tax rate (0%).'],
            [2, 'The default tax rate is 25%.'],
            [3, 'The default tax rate is 50%.'],
            [4, 'The default tax rate is 100%.']
        ],
        widget=widgets.RadioSelect,
        label='<strong>What is your default tax rate?</strong>'
        )
    

    cq_2 = models.IntegerField(blank=True,
        choices=[
            [1, 'Yes.'],
            [2, 'No. I decide for how long and how intensively I want to work each work period.']
        ],
        widget=widgets.RadioSelect,
        label='<strong>Do you have to work throughout the entirety of each 10-minute work period? </strong>'
        )
    


    survey_student_loans = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely less willing'),
            (2, 'Less willing'),
            (3, 'Neutral'),
            (4, 'More willing'),
            (5, 'Definitely more willing'),
        ],
        label="The Biden administration in the US has attempted to eliminate student debt among those with outstanding student loan debt. Assuming that the administration's efforts had been successful, would knowledge of this hypothetical past event make you more or less willing to take on a student loan to afford university tuition for yourself or a family member?",
        widget=widgets.RadioSelectHorizontal,
    )

    survey_pandemic = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely less willing'),
            (2, 'Less willing'),
            (3, 'Neutral'),
            (4, 'More willing'),
            (5, 'Definitely more willing'),
        ],
        label="During the Coronavirus Pandemic, the US government engaged in a one-time cancellation of small business loan debt for businesses that took on a PPP loan from the federal government. Having knowledge that this occurred, if you were a small business owner, <b>would knowledge of this past event make you more or less willing to obtain a small business loan from the federal government?</b>",
        widget=widgets.RadioSelectHorizontal,
    )

    survey_wealth_tax = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely consume more'),
            (2, 'Consume more'),
            (3, 'Neutral'),
            (4, 'Save more'),
            (5, 'Definitely save more'),
        ],
        label="<p>Some countries have implemented one-time wealth taxes—taxes on real and/or financial assets that only apply for a single year.</p><p>For example, in 2013, the government of Cyprus decided to tax all domestic bank account deposits only a single time at a rate up to 9.9%.</p><p>As another example, during the Coronavirus pandemic, the government of Argentina decided to tax high-wealth individuals a one-time rate of 3.5% of their assessed wealth.</p><p>If your government had implemented one of these one-time wealth taxes in the past, <b>would knowledge of this event lead you to increase or reduce the amount you normally save or even consume some of your wealth?</b></p>",
        widget=widgets.RadioSelectHorizontal,
    )

    survey_wealth_tax_personal = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely consume more'),
            (2, 'Consume more'),
            (3, 'Neutral'),
            (4, 'Save more'),
            (5, 'Definitely save more'),
        ], 
        label = "<b>What about if you were personally affected by such a one-time wealth tax?</b>",
        widget=widgets.RadioSelectHorizontal,
    )

    survey_repatriation = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely discourage'),
            (2, 'Discourage'),
            (3, 'Neutral'),
            (4, 'Encourage'),
            (5, 'Definitely encourage')
        ],
        label='<p>High-earning and high-wealth taxpayers often hide their money abroad in order to avoid and evade domestic taxes. However, in the past, the many governments have offered programs called "repatriation amnesties" that allow people to "repatriate" their money domestically from abroad at no or reduced penalties. That is, under these "repatriation amnesties," high-earning and high-wealth taxpayers can bring their income and wealth back home while paying reduced taxes and/or penalties than they would if they were caught.</p><p>If you were a high-earning or high-wealth taxpayer, <b>would knowledge that the government has offered these programs in the past discourage or encourage you from hiding money abroad to avoid/evade taxes in the future?</b></p>',
        widget=widgets.RadioSelectHorizontal,
    )
   
    survey_one_time_policies = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely rely more'),
            (2, 'Rely more'),
            (3, 'Neutral'),
            (4, 'Rely less'),
            (5, 'Definitely rely less'),
        ],
        label='<b>Do you think countries should rely more on one-time policies rather than permanent, typically annual, policies?</b>',
        widget=widgets.RadioSelectHorizontal,
    )

    survey_tax_rates_1 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'very unlikely',),
            (2, 'unlikely'),
            (3, 'neutral'),
            (4, 'likely'),
            (5, 'very likely'),
            ],
        label='<p>The above table shows the US personal income tax schedule for a single filer in 2023. What do you this the probability is that the US personal income tax rate schedule will substantially change...</p><p><b>...in the next 3 months?</b></p>',
        widget=widgets.RadioSelectHorizontal,
    )

    survey_tax_rates_2 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'very unlikely',),
            (2, 'unlikely'),
            (3, 'neutral'),
            (4, 'likely'),
            (5, 'very likely'),
            ],
        label='<p><b>...in the next 6 months?</b></p>',
        widget=widgets.RadioSelectHorizontal,
    )

    survey_tax_rates_3 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'very unlikely',),
            (2, 'unlikely'),
            (3, 'neutral'),
            (4, 'likely'),
            (5, 'very likely'),
            ],
        label='<p><b>...in the next year?</b></p>',
        widget=widgets.RadioSelectHorizontal,
    )

    survey_tax_rates_4 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'very unlikely',),
            (2, 'unlikely'),
            (3, 'neutral'),
            (4, 'likely'),
            (5, 'very likely'),
            ],
        label='<p><b>...in the next 5 years?</b></p>',
        widget=widgets.RadioSelectHorizontal,
    )

    survey_tax_rates_5 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'very unlikely',),
            (2, 'unlikely'),
            (3, 'neutral'),
            (4, 'likely'),
            (5, 'very likely'),
            ],
        label='<p><b>...in the next 10 years?</b></p>',
        widget=widgets.RadioSelectHorizontal,
    )


    feedback = models.LongStringField(label='<strong>Feedback:</strong>', blank=True)
    
    feedback_difficulty = models.IntegerField(label="<b>How clear were the instructions?</b> <br>Please answer on a scale of 1 to 10, with 10 being the clearest.",
        blank=True,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal)
    
    feedback_understanding = models.IntegerField(label="<b>How well did you understand what you were asked to do?</b> <br>Please answer on a scale of 1 to 10, with 10 being the case when you understood perfectly.",
        blank=True,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal)
    
    feedback_satisfied = models.IntegerField(label="<b>How satisfied are you with this study overall?</b> <br>Please answer on a scale of 1 to 10, with 10 being the most satisfied.",
        blank=True,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal)
    
    feedback_pay = models.IntegerField(label="<b>How appropriate do you think the payment for this study is relative to other ones on Prolific?</b> <br>Please answer on a scale of 1 to 10, with 10 being the most appropriate.",
        blank=True,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal)
    

###############################################  FUNCTIONS   ###########################################################

        
######################################################  PAGES   ########################################################


class Welcome(Page):
    form_model = 'player'
    form_fields = ['data_dummy']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.browser = player.data_dummy
        player.participant.start_time = time.time()
        pass 


class Consent(Page):
    pass

class About(Page):
    pass

class Instructions(Page):
    form_model = 'player'
    form_fields = ['data_dummy']

    @staticmethod
    def vars_for_template(player):
        return {
            'participant_code': player.participant.code,
        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.attempts_training = player.data_dummy  


class Instructions2(Page):
    pass

class TaxInstructions(Page):
    pass

class CQS(Page):
    form_model = 'player'
    form_fields = ['cq_1', 'cq_2']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            solutions = dict(
                cq_1=2,
                cq_2=2
                )
            
            error_explanations = {
                'cq_1': 'Your answer is incorrect. The default tax rate is 25%. Please correct your answer.',
                'cq_2': 'Your answer is incorrect. You do not have to work throughout the 10-minute work period. Please correct your answer!'
            }
            error_messages = dict()
            for field_name in solutions:
                if field_name in values.keys():
                    if values[field_name] is None:
                        error_messages[field_name] = 'Please answer the question.'
                    elif values[field_name] != solutions[field_name]:
                        error_messages[field_name] = error_explanations[field_name]
                        name = 'player.participant.' + str(field_name) + '_mistakes'
                        exec("%s += 1" % name)
            return error_messages
        

class InstructionsBeliefs(Page):
    pass



class Beliefs1(Page):
    form_model = 'player'
    form_fields = ['beliefs1']
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.beliefs1 = player.beliefs1


class Transition1(Page):
    pass


class Work1(Page):
    form_model = 'player'
    form_fields = ['data_dummy']
    timeout_seconds = 60*C.WORK_PERIOD_LENGTH

    @staticmethod
    def vars_for_template(player):
        return {
            'participant_code': player.participant.code,
        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.attempts_work_1 = player.data_dummy  



class EndOfWork1(Page):

    @staticmethod
    def vars_for_template(player):
        attempts = json.loads(player.participant.attempts_work_1)

        correct_attempts = attempts['correctAttempts']

        initial_gross_earnings = correct_attempts*C.ROW_PAYMENT/100
   

        tax_info = ""

        # 'C-Info','C-NoInfo', 'T1-T-Info', 'T1-T-NoInfo','T1-P','T2-T'

        if player.participant.treatment in ['C-Info','C-NoInfo']:  
            tax_info = "Your tax rate is 25%. This tax rate is imposed on your earnings only for the last work period. Your default tax rate for future work periods is still 25%."
        elif player.participant.treatment in ['T1-T-Info','T1-T-NoInfo']:
            tax_info = "The tax rate for Work Period 1 was changed to a final tax rate of 50%. This tax rate is imposed on your earnings only for the last work period. Your default tax rate for future work periods is still 25%."
        elif player.participant.treatment == 'T1-P':
            tax_info = "Your tax rate has been permanently changed to 50%. This new tax rate applies to earnings from the last work period and to future earnings. It will not change."
        elif player.participant.treatment == 'T2-T':
            tax_info = "The tax rate for Work Period 1 was changed to a final tax rate of 75%. This tax rate is imposed on your earnings only for the last work period. Your default tax rate for future work periods is still 25%."


        return {
            'correct_attempts': correct_attempts,
            'initial_gross_earnings': initial_gross_earnings,   
            'tax_info': tax_info,
        }
    

class TaxInfo1(Page):
    @staticmethod
    def vars_for_template(player):
        
        tax_info = ""

        # 'C-Info','C-NoInfo', 'T1-T-Info', 'T1-T-NoInfo','T1-P','T2-T'

        if player.participant.treatment == 'C-Info':
            tax_info = "<p>Here is some information that you may want to take into account when thinking about future tax rates:</p> <p style='text-align: center; max-width: 90%; margin: auto;'>Other individuals were randomly selected for a <b>one-time</b> tax shock on last period’s earnings that changed their tax rate to 50%. As initially established, your default tax rate for future work periods is still 25%.</p>"
        elif player.participant.treatment == 'T1-1-Info':
            tax_info = "<p>Here is some information that you may want to take into account when thinking about future tax rates:</p> <p style='text-align: center; max-width: 90%; margin: auto;'>Other individuals were also randomly selected for a <b>one-time</b> tax shock on last period’s earnings that changed their tax rate to 50%. As initially established, your default tax rate for future work periods is still 25%.</p>"

        return { 
            'tax_info': tax_info,
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.treatment in ['C-Info','T1-1-Info']


class Beliefs2(Page):
    form_model = 'player'
    form_fields = ['beliefs2']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.beliefs2 = player.beliefs2


class Transition2(Page):
    pass


class Work2(Page):
    form_model = 'player'
    form_fields = ['data_dummy']
    timeout_seconds = 60*C.WORK_PERIOD_LENGTH

    @staticmethod
    def vars_for_template(player):
        return {
            'participant_code': player.participant.code,
        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.attempts_work_2 = player.data_dummy  



class EndOfWork2(Page):

    @staticmethod
    def vars_for_template(player):
    

        attempts = json.loads(player.participant.attempts_work_2)

        correct_attempts = attempts['correctAttempts']

        initial_gross_earnings = correct_attempts*C.ROW_PAYMENT/100
   

        tax_info = ""

        # 'C-Info','C-NoInfo', 'T1-T-Info', 'T1-T-NoInfo','T1-P','T2-T'

        if player.participant.treatment in ['C-Info','C-NoInfo','T1-T-Info','T1-T-NoInfo', 'T2-T']:  
            tax_info = "Your tax rate is 25%. This tax rate is imposed on your earnings <b>only</b> for the last work period. Your default tax rate for future work periods is still 25%." 
        elif player.participant.treatment == 'T1-P':
            tax_info = "Your tax rate is 50%. This tax rate is imposed on your earnings for the last work period as well as for future earnings."
       


        return {
            'correct_attempts': correct_attempts,
            'initial_gross_earnings': initial_gross_earnings,   
            'tax_info': tax_info,
        }




class Beliefs3(Page):
    form_model = 'player'
    form_fields = ['beliefs3']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.beliefs3 = player.beliefs3

class Transition3(Page):
    pass


class Work3(Page):
    form_model = 'player'
    form_fields = ['data_dummy']
    timeout_seconds = 60*C.WORK_PERIOD_LENGTH

    @staticmethod
    def vars_for_template(player):
        return {
            'participant_code': player.participant.code,
        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.attempts_work_3 = player.data_dummy  



class EndOfWork3(Page):

    @staticmethod
    def vars_for_template(player):
    

        attempts = json.loads(player.participant.attempts_work_3)

        correct_attempts = attempts['correctAttempts']

        initial_gross_earnings = correct_attempts*C.ROW_PAYMENT/100
   

        tax_info = ""

        # 'C-Info','C-NoInfo', 'T1-T-Info', 'T1-T-NoInfo','T1-P','T2-T'

        if player.participant.treatment in ['C-Info','C-NoInfo','T1-T-Info','T1-T-NoInfo', 'T2-T']:  
            tax_info = "Your tax rate is 25%. This tax rate is imposed on your earnings <b>only</b> for the last work period. Your default tax rate for future work periods is still 25%." 
        elif player.participant.treatment == 'T1-P':
            tax_info = "Your tax rate is 50%. This tax rate is imposed on your earnings for the last work period as well as for future earnings."


        return {
            'correct_attempts': correct_attempts,
            'initial_gross_earnings': initial_gross_earnings,   
            'tax_info': tax_info,
        }




class TaxInfo3(Page):
    pass



class Beliefs4(Page):
    form_model = 'player'
    form_fields = ['beliefs4']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.beliefs4 = player.beliefs4


class Transition4(Page):
    pass




class Survey(Page):
    form_model = 'player'
    form_fields = ['survey_student_loans', 'survey_pandemic', 'survey_wealth_tax' ,'survey_wealth_tax_personal', 'survey_repatriation', 'survey_one_time_policies','survey_tax_rates_1','survey_tax_rates_2','survey_tax_rates_3','survey_tax_rates_4','survey_tax_rates_5']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            error_messages = dict()
            for field_name in ['survey_student_loans', 'survey_pandemic', 'survey_wealth_tax' ,'survey_wealth_tax_personal', 'survey_repatriation', 'survey_one_time_policies','survey_tax_rates_1','survey_tax_rates_2','survey_tax_rates_3','survey_tax_rates_4','survey_tax_rates_5']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question'
            return error_messages




class Outcome(Page):

    @staticmethod
    def vars_for_template(player):

        initial_gross_earnings = []
        for el in ["1", "2", "3"]:
            # Construct the attribute name dynamically
            attempts_attr = f'attempts_work_{el}'
            # Use getattr to get the attribute from player.participant
            attempts = json.loads(getattr(player.participant, attempts_attr))
            correct_attempts = attempts['correctAttempts']
            initial_gross_earning = correct_attempts*C.ROW_PAYMENT/100
            initial_gross_earnings.append(initial_gross_earning)

        
   

    

        # 'C-Info','C-NoInfo', 'T1-T-Info', 'T1-T-NoInfo','T1-P','T2-T'

        tax_rates = {
            'C-Info': [.25,.25,.25],
            'C-NoInfo': [.25,.25,.25],
            'T1-T-Info': [.5,.25,.25],
            'T1-T-NoInfo': [.5,.25,.25],
            'T1-P': [.5,.5,.5],
            'T2-T': [.75,.25,.25]
        }

        tax_rate = tax_rates[player.participant.treatment]
        tax_rate = np.array(tax_rate) 
        total_post_tax_earnings = np.dot(1-tax_rate, initial_gross_earnings)

        

        correct_beliefs = tax_rates = {
            'C-Info': [.25,.25,.25],
            'C-NoInfo': [.25,.25,.25],
            'T1-T-Info': [.5,.25,.25],
            'T1-T-NoInfo': [.5,.25,.25],
            'T1-P': [.5,.5,.5],
            'T2-T': [.75,.25,.25]
        }


        participant_belief = f'beliefs{player.participant.which_belief}'
        # Use getattr to get the attribute from player.participant
        participant_belief = int(getattr(player.participant, participant_belief))/100

        print(participant_belief)
        correct_belief = correct_beliefs[player.participant.treatment][player.participant.which_belief-1]

        delta = 0.025
        belief_bonus = abs(correct_belief - participant_belief) < delta

        if belief_bonus:
            belief_bonus_text = 'You have earned a bonus of $'+ C.BELIEF_BONUS +' for your accurate beliefs about the tax rate.'
        else:
            belief_bonus_text = 'You have not earned a bonus for your beliefs about the tax rate.'

        if belief_bonus:
            total_post_tax_earnings += C.BELIEF_BONUS
        
        player.participant.payoff  = total_post_tax_earnings + C.PARTICIPATION_FEE
        return {
            'total_post_tax_earnings': total_post_tax_earnings,
            'belief_bonus_text': belief_bonus_text,
            'total_payment': player.participant.payoff
        }
    




class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback', 'feedback_difficulty', 'feedback_understanding', 'feedback_satisfied', 'feedback_pay']

    @staticmethod
    def vars_for_template(player):
        return {
            # 'GAMBLE_DATA': C.GAMBLE_DATA
        }

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            error_messages = dict()
            for field_name in ['feedback_difficulty', 'feedback_understanding', 'feedback_satisfied',
                               'feedback_pay']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question'
            return error_messages
        
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.feedback = player.field_maybe_none('feedback')
        player.participant.feedback_difficulty = player.field_maybe_none('feedback_difficulty')
        player.participant.feedback_understanding = player.field_maybe_none('feedback_understanding')
        player.participant.feedback_satisfied = player.field_maybe_none('feedback_satisfied')
        player.participant.feedback_pay = player.field_maybe_none('feedback_pay')

        player.participant.end_time = time.time()
        player.participant.finished = True
        pass

class Finished(Page):
    pass


class Redirect(Page):
    pass

page_sequence = [
    Welcome,
    Consent,
    About,
    Instructions,
    Instructions2,
    TaxInstructions,
    CQS,
    InstructionsBeliefs,
    Beliefs1,
    Transition1,
    Work1,
    EndOfWork1,
    TaxInfo1,
    Beliefs2,
    Transition2,
    Work2,
    EndOfWork2,
    Beliefs3,
    Transition3,
    Work3,
    EndOfWork3,
    Beliefs4,
    Transition4,
    Survey,
    Outcome,
    Feedback,
    Finished,
    Redirect
]
