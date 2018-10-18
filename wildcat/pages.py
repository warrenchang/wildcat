from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np


class Introduction(Page):
    timeout_seconds = 90

    def is_displayed(self):
        return self.player.round_in_interaction == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['x', 'y']

    def get_timeout_seconds(self):
        if self.player.round_number <=2:
            return 60
        else:
            return 30

    def before_next_page(self):
        if self.timeout_happened:
            self.player.x = 0
            self.player.y = 0
            self.player.value = 0
        else:
            self.player.value = Constants.values[self.player.x-1][self.player.y-1]
        self.player.payoff = self.player.value/Constants.values.max()
        self.player.cum_value = sum([p.value for p in self.player.in_all_rounds()
                             if p.interaction_number == self.player.interaction_number])

    def vars_for_template(self):
        v = {
            'xs': [p.x for p in self.player.in_previous_rounds() if p.interaction_number == self.player.interaction_number],
            'ys': [p.y for p in self.player.in_previous_rounds() if p.interaction_number == self.player.interaction_number],
            'values': [p.value for p in self.player.in_previous_rounds() if p.interaction_number == self.player.interaction_number],
        }
        return v


class DecisionWaitPage(WaitPage):
    template_name = 'wildcat/DecisionWaitPage.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.player.treatment != 'non'

    def vars_for_template(self):
        v = {
            'xs': [p.x for p in self.player.in_all_rounds() if p.interaction_number == self.player.interaction_number],
            'ys': [p.y for p in self.player.in_all_rounds() if p.interaction_number == self.player.interaction_number],
            'values': [p.value for p in self.player.in_all_rounds() if p.interaction_number == self.player.interaction_number],
        }
        return v

    def after_all_players_arrive(self):
        values = np.array([p.value for p in self.subsession.get_players()])
        for p in self.subsession.get_players():
            if p.treatment=="avg":
                p.info = values.mean()
            elif p.treatment=="min":
                p.info = values.min()
            elif p.treatment=="max":
                p.info = values.max()


page_sequence = [
    Introduction,
    Decision,
    DecisionWaitPage,
]
