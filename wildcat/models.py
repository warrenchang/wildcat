from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import numpy as np

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'wildcat'
    players_per_group = None
    values = np.random.random((100,100))*100

    treatments = ['non', 'avg', 'min', 'max']

    ## below is just for debug
    interactions = [
        1, 1, 1,
        2, 2, 2,
        3, 3, 3,
        4, 4, 4,
    ]
    round_in_interactions = [
        1, 2, 3,
        1, 2, 3,
        1, 2, 3,
        1, 2, 3,
    ]
    interaction_length = [3, 3, 3, 3]

    # interactions = [
    #     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    #     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    #     3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    #     4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    # ]
    # round_in_interactions = [
    #     1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    #     1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    #     1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    #     1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    # ]
    # interaction_length = [15, 15, 15, 15]


    num_rounds = sum(interaction_length) # change num_rounds for testing purpose, but need to make sure that number_sequence


class Subsession(BaseSubsession):

    def creating_session(self):
        # this is run before the start of every round
        round_in_interaction = Constants.round_in_interactions[self.round_number-1]
        interaction_number = Constants.interactions[self.round_number-1]
        treatment = Constants.treatments[interaction_number-1]

        for p in self.get_players(): # set interaction number and round number
            p.interaction_number = interaction_number
            p.round_in_interaction = round_in_interaction
            p.treatment = treatment
            print((p.participant.id_in_session, p.interaction_number, p.round_in_interaction, p.treatment))



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    interaction_number = models.PositiveIntegerField()
    round_in_interaction = models.PositiveIntegerField()
    treatment = models.StringField()
    x = models.IntegerField(min=1, max=100)
    y = models.IntegerField(min=1, max=100)
    value = models.IntegerField()
    cum_value = models.IntegerField()
    info = models.IntegerField()

