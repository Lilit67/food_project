import os
from step import Step
from datetime import datetime, timedelta

from time_unit import TimeUnit as timeunit

class RecipeStepManager:
    def __init__(self, unit):
        self.time_unit = unit
        self.steps = []

    def add_step(self, recipe_id, name, interval, connected=False, active=True, explanation=''):
        """
        Add a Step to the step manager,
        Timeunit internally to step converted to seconds
        :param name:
        :param interval:
        :param connected:
        :param active:
        :return:
        """
        step = Step(recipe_id, name, interval, connected, active,
                    unit=self.time_unit, explanation=explanation)
        self.steps.append(step)

    def construct(self, recipe_id, recipe_schedule):
        """ Construct the class from initial info whatecer it is """
        for rep in recipe_schedule:
            self.recipe_id = recipe_id

            explanation = rep[4]
            self.add_step(self.recipe_id, rep[0], rep[1], rep[2], rep[3], explanation=explanation)

    def __str__(self):
        steplist = []
        for step in self.steps:
            steplist.append(step.step_name)

        return ', '.join(steplist)

    def total_duration(self, unit=timeunit.minutes):
        total = 0
        for step in self.steps:
            total += step.to_minutes(step.interval, unit=unit)

        return total

