import random
import json
import itertools
import time
from otree.api import *
import numpy as np

doc = """
OTFE Lukas Bolte: lukas.bolte@outlook.com. 
"""


class C(BaseConstants):
    NAME_IN_URL = 'risk'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    APPROX_TIME = "40-50 minutes"
    AVG_TOTAL_PAYMENT = "$16"
    PARTICIPATION_FEE = 6.50
    ROW_PAYMENT = 15
    MAX_MISTAKES = 5
    BELIEF_BONUS = 1
    TAX_RATES = {
            'C-Info': [.25,.25,.25],
            'C-NoInfo': [.25,.25,.25],
            'T1-T-Info': [.5,.25,.25],
            'T1-T-NoInfo': [.5,.25,.25],
            'T1-P': [.5,.5,.5],
            'T2-T': [.90,.25,.25]
        }

    WORK_PERIOD_LENGTH = 10 # change to 10 for real experiment

    INSTRUCTIONS_BELIEFS = 'otfe/Review-instructionsBeliefs.html'
    INSTRUCTIONS = 'otfe/Review-instructions.html'
    INSTRUCTIONS2 = 'otfe/Review-instructions2.html'
    TAX_INSTRUCTIONS = 'otfe/Review-instructionsTax.html'

class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        treatments = ['C-Info','C-NoInfo', 'T1-T-Info', 'T1-T-NoInfo','T1-P','T2-T'] 
        random.shuffle(treatments)
        treatments = itertools.cycle(treatments)
        i=1
        for p in subsession.get_players():
            el = next(treatments)
            p.participant.treatment = el
            p.participant.cq_1_mistakes = 0
            p.participant.cq_2_mistakes = 0
            p.participant.cq_3_mistakes = 0
            p.participant.which_belief = random.choice(["1","2","3","1_2","1_3","2_3"])
            i+=1

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    data_dummy = models.StringField(blank=True)

    beliefs1 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate (%, between 0 and 100):</b>')
    beliefs2 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate (%, between 0 and 100):</b>')
    beliefs3 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate (%, between 0 and 100):</b>')
    beliefs4 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate (%, between 0 and 100):</b>')

    beliefs1_2 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate (%, between 0 and 100):</b>')
    beliefs1_3 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate (%, between 0 and 100):</b>')
    beliefs2_3 = models.IntegerField(min=0, max=100, label='<b>Expected tax rate (%, between 0 and 100):</b>')

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
            [2, 'No. I decide for how long and how intensively I want to work each work period. I can take breaks whenever I want.']
        ],
        widget=widgets.RadioSelect,
        label='<strong>Do you have to work throughout the entirety of each ' + str(C.WORK_PERIOD_LENGTH) + '-minute work period? </strong>'
        )

    cq_3 = models.IntegerField(blank=True,
        choices=[
            [1, 'One transcription task.'],
            [2, 'I can complete as many transcription tasks as I would like during each work period. After I complete a transcription, a new transcription task will appear.']
        ],
        widget=widgets.RadioSelect,
        label='<strong>How many transcription tasks are you able to complete per work period?</strong>'
        )

    survey_student_loans_with = models.IntegerField(min=0, max=100, label='<b>What probability (%, between 0 and 100) would you assign to you taking out a student loan to afford university tuition?</b>')

    survey_student_loans_without = models.IntegerField(min=0, max=100, label='<b>What probability (%, between 0 and 100) would you assign to you taking out a student loan to afford university tuition?</b>')

    survey_student_loans_with_likert = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Very unlikely',),
            (2, 'Unlikely'),
            (3, 'Likely'),
            (4, 'Very likely'),
            ],
        label='<b>How likely would you take out a student loan to afford university tuition for yourself or a family member?</b>',
        widget=widgets.RadioSelectHorizontal,
    )

    survey_student_loans_without_likert = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Very unlikely',),
            (2, 'Unlikely'),
            (3, 'Likely'),
            (4, 'Very likely'),
            ],
        label='<p>Assuming that such efforts to cancel pre-existing, outstanding student had been <i>successful</i> in the recent past, <b>how likely would you take out a student loan to afford university tuition for yourself or a family member?</b></p>',
        widget=widgets.RadioSelectHorizontal,
    )

    survey_pandemic = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely less willing'),
            (2, 'Less willing'),
            (3, 'No change'),
            (4, 'More willing'),
            (5, 'Definitely more willing'),
        ],
        label="During the Coronavirus Pandemic, the US government engaged in a one-time cancellation of small business loan debt for businesses that took on a PPP loan from the federal government. Having knowledge that this occurred, if you were a small business owner, <b>would knowledge of this past event make you more or less willing to obtain a small business loan from the federal government?</b>",
        widget=widgets.RadioSelectHorizontal,
    )

    survey_wealth_tax_savings = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Spend/consume much less',),
            (2, 'Spend/consume somewhat less'),
            (3, 'No change'),
            (4, 'Spend/consume somewhat more'),
            (5, 'Spend/consume much more'),
            ],
        label="<p>If your government had implemented one of these one-time wealth taxes in the recent past, <b>would knowledge of this event lead you to change the <i>amount you normally spend/consume out of your existing savings/wealth?</i></b></p>",
        widget=widgets.RadioSelect,
    )

    survey_wealth_tax_savings_number = models.IntegerField(min=0, label='',blank=True)

    survey_wealth_tax_consumption = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Increase spending by 20% of wealth'),  
            (2, 'Increase spending by 15% of wealth'),  
            (3, 'Increase spending by 10% of wealth'),  
            (4, 'Increase spending by 5% of wealth'),  
            (5, 'No change in spending'),  
            (6, 'Reduce spending by 5% of wealth'),  
            (7, 'Reduce spending by 10% of wealth'),  
            (8, 'Reduce spending by 15% of wealth'),  
            (9, 'Reduce spending by 20% of wealth')  
        ],
        label="<p>If your government had implemented one of these one-time wealth taxes in the recent past, <b>would knowledge of this event lead you to increase or reduce the amount you normally <I>spend/consume out of your existing savings/wealth?</i></b></p>",
        widget=widgets.RadioSelect,
    )

    survey_wealth_tax_personal_savings = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely save less'),
            (2, 'Save less'),
            (3, 'No change'),
            (4, 'Save more'),
            (5, 'Definitely save more'),
        ], 
        label = "<p><b>How would your <i>savings out of income</i> change if you were personally affected by such a one-time wealth tax?</b></p>",
        widget=widgets.RadioSelectHorizontal,
    )
    
    survey_wealth_tax_personal_consumption = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely spend less'),
            (2, 'Spend less'),
            (3, 'No change'),
            (4, 'Spend more'),
            (5, 'Definitely spend more'),
        ], 
        label = "<p><b>How would your <i>spending out of existing wealth</i> change if you were personally affected by such a one-time wealth tax?</b></p>",
        widget=widgets.RadioSelectHorizontal,
    )  
    
    survey_repatriation = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Definitely discourage'),
            (2, 'Discourage'),
            (3, 'No change'),
            (4, 'Encourage'),
            (5, 'Definitely encourage')
        ],
        label='<p>High-earning and high-wealth taxpayers often hide their money abroad in order to avoid and evade domestic taxes. However, in the past, many governments have offered programs called "repatriation amnesties" that allow people to "repatriate" their money domestically from abroad at no or reduced penalties. That is, under these "repatriation amnesties," high-earning and high-wealth taxpayers can bring their income and wealth back home while paying reduced taxes and/or penalties than they would if they were caught.</p><p>If you were a high-earning or high-wealth taxpayer, <b>would knowledge that the government has offered these programs in the past discourage or encourage you from hiding money abroad to avoid/evade taxes in the future?</b></p>',
        widget=widgets.RadioSelectHorizontal,
    )
   
    # survey_one_time_policies = models.IntegerField(
    #     blank=True,
    #     choices=[
    #         (1, 'Definitely rely less'),
    #         (2, 'Rely less'),
    #         (3, 'No change'),
    #         (4, 'Rely more'),
    #         (5, 'Definitely rely more'),
    #     ],
    #     label='<b>Do you think countries should rely more on one-time policies rather than permanent, typically annual, policies?</b>',
    #     widget=widgets.RadioSelectHorizontal,
    # )

    survey_tax_rates_1 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Very unlikely'),  
            (2, 'Unlikely'),  
            (3, 'Likely'),  
            (4, 'Very likely')
            ],
        label='<p><b>...in the next 3 months?</b></p>',
        widget=widgets.RadioSelect,
    )

    survey_tax_rates_2 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Very unlikely'),  
            (2, 'Unlikely'),  
            (3, 'Likely'),  
            (4, 'Very likely')
            ],
        label='<p><b>...in the next 6 months?</b></p>',
        widget=widgets.RadioSelect,
    )

    survey_tax_rates_3 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Very unlikely'),  
            (2, 'Unlikely'),  
            (3, 'Likely'),  
            (4, 'Very likely')
            ],
        label='<p><b>...in the next year?</b></p>',
        widget=widgets.RadioSelect,
    )

    survey_tax_rates_4 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Very unlikely'),  
            (2, 'Unlikely'),  
            (3, 'Likely'),  
            (4, 'Very likely') 
            ],
        label='<p><b>...in the next 5 years?</b></p>',
        widget=widgets.RadioSelect,
    )

    survey_tax_rates_5 = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Very unlikely'),  
            (2, 'Unlikely'),  
            (3, 'Likely'),  
            (4, 'Very likely') 
            ],
        label='<p><b>...in the next 10 years?</b></p>',
        widget=widgets.RadioSelect,
    )

    survey_tax_rates_1_prob = models.IntegerField(min=0, max=100, label='<b>With what probability (%, between 0 and 100)?</b>')
    survey_tax_rates_2_prob = models.IntegerField(min=0, max=100, label='<b>With what probability (%, between 0 and 100)?</b>')
    survey_tax_rates_3_prob = models.IntegerField(min=0, max=100, label='<b>With what probability (%, between 0 and 100)?</b>')
    survey_tax_rates_4_prob = models.IntegerField(min=0, max=100, label='<b>With what probability (%, between 0 and 100)?</b>')
    survey_tax_rates_5_prob = models.IntegerField(min=0, max=100, label='<b>With what probability (%, between 0 and 100)?</b>')


    annual_income = models.IntegerField(
        blank=True,
        choices=[
            (1, 'Less than $10,000'),
            (2, '$10,000 - $19,999'),
            (3, '$20,000 - $29,999'),
            (4, '$30,000 - $39,999'),
            (5, '$40,000 - $49,999'),
            (6, '$50,000 - $59,999'),
            (7, '$60,000 - $69,999'),
            (8, '$70,000 - $79,999'),
            (9, '$80,000 - $89,999'),
            (10, '$90,000 - $99,999'),
            (11, '$100,000 - $149,999'),
            (12, 'More than $150,000')
        ],
        label='<p><b>What is your current annual personal income (in USD)?</b></p>',
        widget=widgets.RadioSelect,
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
    form_fields = ['cq_1', 'cq_2', 'cq_3']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            solutions = dict(
                cq_1=2,
                cq_2=2,
                cq_3=2
                )
            
            error_explanations = {
                'cq_1': 'Your answer is incorrect. The default tax rate is 25%. Please correct your answer.',
                'cq_2': 'Your answer is incorrect. You do not have to work throughout the ' + str(C.WORK_PERIOD_LENGTH) + '-minute work period. Please correct your answer!',
                'cq_3': 'Your answer is incorrect. You can complete as many transcription tasks as you would like for the duration of the work period. As soon as you complete a transcription task, a new one will appear. Please correct your answer!'
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
    form_fields = ['beliefs1','beliefs1_2','beliefs1_3']
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.beliefs1 = player.beliefs1
        player.participant.beliefs1_2 = player.beliefs1_2
        player.participant.beliefs1_3 = player.beliefs1_3

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

        if player.participant.treatment in ['C-Info','C-NoInfo']:  
            tax_info = "<b>Your tax rate is 25%</b>. This tax rate is imposed on your earnings only for the last work period. Your default tax rate for future work periods is still 25%."
        elif player.participant.treatment in ['T1-T-Info','T1-T-NoInfo']:
            tax_info = "<b>The tax rate for Work Period 1 was changed to a final tax rate of 50%</b>. This tax rate is imposed on your earnings only for the last work period. Your default tax rate for future work periods is still 25%."
        elif player.participant.treatment == 'T1-P':
            tax_info = "<b>Your tax rate has been permanently changed to 50%</b>. This new tax rate applies to earnings from the last work period and to future earnings. It will not change from 50%."
        elif player.participant.treatment == 'T2-T':
            tax_info = "<b>The tax rate for Work Period 1 was changed to a final tax rate of 90%</b>. This tax rate is imposed on your earnings only for the last work period. Your default tax rate for future work periods is still 25%."

        tax_rate = C.TAX_RATES[player.participant.treatment][0] 
        net_earnings = initial_gross_earnings*(1-tax_rate)

        return {
            'correct_attempts': correct_attempts,
            'initial_gross_earnings': initial_gross_earnings,   
            'tax_info': tax_info,
            'net_earnings': net_earnings
        }
    
class TaxInfo1(Page):
    @staticmethod
    def vars_for_template(player):
        
        tax_info = ""

        if player.participant.treatment == 'C-Info':
            tax_info = "<p>Here is some information that you may want to take into account when thinking about future tax rates:</p> <p style='text-align: center; max-width: 90%; margin: auto;'>Other individuals were randomly selected for a <b>one-time</b> tax shock on last period’s earnings that <b>changed their tax rate to 50%</b>. As initially established, your <b>default tax rate for future work periods is still 25%</b>.</p>"
        elif player.participant.treatment == 'T1-1-Info':
            tax_info = "<p>Here is some information that you may want to take into account when thinking about future tax rates:</p> <p style='text-align: center; max-width: 90%; margin: auto;'>Other individuals were also randomly selected for a <b>one-time</b> tax shock on last period’s earnings that <b>changed their tax rate to 50%</b>. As initially established, your <b>default tax rate for future work periods is still 25%</b>.</p>"

        return { 
            'tax_info': tax_info,
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.treatment in ['C-Info','T1-1-Info']


class Beliefs2(Page):
    form_model = 'player'
    form_fields = ['beliefs2','beliefs2_3']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.beliefs2 = player.beliefs2
        player.participant.beliefs2_3 = player.beliefs2_3

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

        if player.participant.treatment in ['C-Info','C-NoInfo','T1-T-Info','T1-T-NoInfo', 'T2-T']:  
            tax_info = "<b>Your tax rate is 25%</b>. This tax rate is imposed on your earnings <b>only</b> for the last work period. Your default tax rate for future work periods is still 25%." 
        elif player.participant.treatment == 'T1-P':
            tax_info = "<b>Your tax rate is 50%</b>. This tax rate is imposed on your earnings for the last work period as well as for future earnings."
       
        tax_rate = C.TAX_RATES[player.participant.treatment][1] 
        net_earnings = initial_gross_earnings*(1-tax_rate)

        return {
            'correct_attempts': correct_attempts,
            'initial_gross_earnings': initial_gross_earnings,   
            'tax_info': tax_info,
            'net_earnings': net_earnings
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

        if player.participant.treatment in ['C-Info','C-NoInfo','T1-T-Info','T1-T-NoInfo', 'T2-T']:  
            tax_info = "<b>Your tax rate is 25%</b>. This tax rate is imposed on your earnings <b>only</b> for the last work period. Your default tax rate for future work periods is still 25%." 
        elif player.participant.treatment == 'T1-P':
            tax_info = "<b>Your tax rate is 50%</b>. This tax rate is imposed on your earnings for the last work period as well as for future earnings."

        tax_rate = C.TAX_RATES[player.participant.treatment][2] 
        net_earnings = initial_gross_earnings*(1-tax_rate)

        return {
            'correct_attempts': correct_attempts,
            'initial_gross_earnings': initial_gross_earnings,   
            'tax_info': tax_info,
            'net_earnings': net_earnings
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
    form_model = 'player'
    form_fields = ['data_dummy']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.attention_check = player.data_dummy


class Survey(Page):
    form_model = 'player'
    form_fields = ['survey_student_loans_with', 'survey_student_loans_without', 'survey_student_loans_with_likert', 'survey_student_loans_without_likert']

    @staticmethod
    def error_message(player, values):

        if not player.session.config['development']:
            error_messages = dict()
            for field_name in ['survey_student_loans_with', 'survey_student_loans_without', 'survey_student_loans_with_likert', 'survey_student_loans_without_likert']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question'
            return error_messages
    




class Survey2(Page):
    form_model = 'player'
    form_fields = ['survey_wealth_tax_savings','survey_wealth_tax_savings_number']

    @staticmethod
    def error_message(player, values):

        if not player.session.config['development']:
            error_messages = dict()
            for field_name in ['survey_wealth_tax_savings','survey_wealth_tax_savings_number']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question'
                    if values['survey_wealth_tax_savings'] == 3:
                        del error_messages['survey_wealth_tax_savings_number']
            return error_messages
    



        
class Survey3(Page):
    form_model = 'player'
    form_fields = [ 'survey_repatriation']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            error_messages = dict()
            for field_name in ['survey_repatriation']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question'
            return error_messages
        


class Survey4(Page):
    form_model = 'player'
    form_fields = ['survey_tax_rates_1','survey_tax_rates_2','survey_tax_rates_3','survey_tax_rates_4','survey_tax_rates_5','survey_tax_rates_1_prob','survey_tax_rates_2_prob','survey_tax_rates_3_prob','survey_tax_rates_4_prob','survey_tax_rates_5_prob']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            error_messages = dict()
            for field_name in ['survey_tax_rates_1','survey_tax_rates_2','survey_tax_rates_3','survey_tax_rates_4','survey_tax_rates_5','survey_tax_rates_1_prob','survey_tax_rates_2_prob','survey_tax_rates_3_prob','survey_tax_rates_4_prob','survey_tax_rates_5_prob']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please answer the question'
            return error_messages



class Survey5(Page):
    form_model = 'player'
    form_fields = ['annual_income']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            error_messages = dict()
            for field_name in ['annual_income']:
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

        tax_rates = C.TAX_RATES
        
        tax_rate = tax_rates[player.participant.treatment]
        tax_rate = np.array(tax_rate) 
        total_post_tax_earnings = np.dot(1-tax_rate, initial_gross_earnings)

        correct_beliefs = C.TAX_RATES 

        participant_belief = f'beliefs{player.participant.which_belief}'
        participant_belief = int(getattr(player.participant, participant_belief))/100
        belief_dict = {
            "1": 0,
            "2": 1,
            "3": 2,
            "1_2": 1,
            "1_3": 2,
            "2_3": 2
        }
        correct_belief = correct_beliefs[player.participant.treatment][belief_dict[player.participant.which_belief]]

        delta = 0.025
        belief_bonus = abs(correct_belief - participant_belief) < delta

        player.participant.belief_bonus = belief_bonus

        if belief_bonus:
            belief_bonus_text = 'You have earned a bonus of <b>$'+ str(C.BELIEF_BONUS) +'</b> for your accurate beliefs about the tax rate.'
        else:
            belief_bonus_text = 'You have not earned a bonus for your beliefs about the tax rate.'

        player.participant.payoff  = total_post_tax_earnings

        if belief_bonus:
            player.participant.payoff += C.BELIEF_BONUS

        total_payment = player.participant.payoff + C.PARTICIPATION_FEE
        return {
            'total_post_tax_earnings': total_post_tax_earnings,
            'belief_bonus_text': belief_bonus_text,
            'total_payment': total_payment
        }

class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback','feedback_difficulty','feedback_understanding','feedback_satisfied','feedback_pay']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            error_messages = dict()
            for field_name in ['feedback_difficulty','feedback_understanding','feedback_satisfied','feedback_pay']:
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
    @staticmethod
    def vars_for_template(player):

       

        total_payment = player.participant.payoff + C.PARTICIPATION_FEE
        return {
            'total_payment': total_payment
        }

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
    Survey2,
    Survey3,
    Survey4,
    Survey5,
    Outcome,
    Feedback,
    Finished,
    Redirect
]
