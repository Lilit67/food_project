import json
import os
import argparse
import sched
import time
from pydoc import locate
from datetime import datetime, timedelta, date
from collections import OrderedDict

from recipe_step_manager import RecipeStepManager
from time_unit import TimeUnit as timeunit
from charting import Chart

# interval, connected, active
# if connected to previous and active, cannot take the next user timeslot
recipe_schedule2 = [('premix', 10, 50, True, "mixing the dough until incorporated, but not more"),
                    ('autolyze', 8 * 60, 90, True, 'Leave the dough for some time for gluten to develop'),
                   ('StretchFold', 150, 200, True, 'Stretch the dough from one side and fold on top. Do from each side'),
                   ('bulk fermentation', 14*60, 90, False, 'Leave unportioned dough for some time to ferment'),
                   ('bench rest', 30, 60, True, 'Leave portioned dough to relax for some time before shaping'),
                   ('shape', 30, 0, True, 'Shape the dough to final form'),
                   ('proof', 4*60, 8*60, False, 'Proof the dough in the form'),
                   ('bake', 40, 0, True, 'Bake')]

recipe_schedule3 = [('premix', 10, 50, True, 'mixing dough thoroughly but no kneading'),
                    ('autolyze', 30, 90, False, 'leave dough to develop gluten'),
                   ('StretchFold', 150, 200, True, 'develop gluten'),
                   ('bulk fermentation', 8*60, 90, False, 'ferment the bulk dough'),
                   ('bench rest', 30, 60, True, 'portion dough and leave shortly for the dough to relax'),
                   ('shape', 30, 0, True, 'shape dough'),
                   ('proof', 4*60, 8*60, False, 'leave dough to rise'),
                   ('bake', 40, 0, True, 'bake')]

croissant_schedule = [('premix', 10, 50, True),
                    ('autolyze', 30, 90, True),
                   ('Knead with salt and butter', 10, 5, True),
                   ('proof', 60, 90, False),
                   ('ferment', 8*60, 8*60, True),
                   ('butter packet', 30, 60, True),
                   ('first turn', 60, 0, True),
                   ('second turn', 30, 0, True),
                   ('third turn', 30, 0, True),
                   ('proof', 8*60, 8*60, False),
                   ('bake', 25, 5, True)]

class SimpleScheduler:
    def __init__(self, recipe_id, steps, enddate, timeunit=timeunit.minutes):
        self.recipe_id = recipe_id
        self.steps = steps
        self.enddate = enddate
        self.starttime = None
        self.schedule = None
        self.step_mgr = RecipeStepManager(timeunit)
        self.timeunit = timeunit
        self.step_mgr.construct(self.recipe_id, steps)

    def simple_schedule(self):
        """
        Calculate the start time, and print
        all the times of action items
        :return:
        """
        # total duration
        datetime_end = datetime.strptime(self.enddate, '%b %d %Y %I:%M%p')

        current = datetime_end
        self.step_mgr.steps.reverse()

        for step in self.step_mgr.steps:
            step.set_start(current)
            step.set_timeback(current)
            current = step.timeback
        # our schedule is reverted now...
        # TODO keep in normal order
        self.starttime = self.step_mgr.steps[-1].timeback


    def custom_schedule(self, recipe_schedule, baker_schedule):
        """
        This method is to create a custom
        schedule when user has a limited time
        intervals for preparation
        Behavior is to go over actual
        and recipe timings in parallel and find out if
        the recipe timing can fit into user's schedule
        If not, return None and ask for different times
        If yes, return the schedule.
        :return:
        """
        # init
        step_mgr = self.step_mgr

        time_mgr = BakerTimeManager(baker_schedule)
        adjustment = {}
        print('\nStart at this time {}'.format(time_mgr.start_time))

        step_index = 0

        number_of_steps = len(step_mgr.steps)
        start, end = time_mgr.start_time, time_mgr.end_time
        current_time = start
        while step_index < number_of_steps:
            if current_time > end:
                raise Exception("No time left in my schedule to complete recipe!")
            step = step_mgr.steps[step_index]
            delta = timedelta(seconds=step_mgr.steps[step_index].interval)
            stretch = timedelta(seconds=step_mgr.steps[step_index].stretch)

            print('Starting time {}, time delta: {}'.format(current_time, delta))
            current_time = current_time + delta
            can_jump = True if not step.active_step else False
            print("Step #{}: {} will be completed by: {}".format(step_index, step.step_name, current_time))

            if time_mgr.inside(step, current_time, stretch=stretch):
                #print("Step #{}: {} will be completed by: {}".format(step_index, step.step_name, current_time))
                adjustment[step.step_name] = current_time
                #print('Completed step # {}. {}'.
                #      format(step_index, step_mgr.steps[step_index].step_name))
                step_index += 1
                continue

            else:
                print('Oh NO! Do not have time for step {}'.format(step.step_name))
                break
        if step_index < number_of_steps:
            msg = 'This recipe schedule CANNOT be completed within the constraints, profpose another schedule'
            raise Exception(msg)
            return None
        else:
            print('You CAN complete this recipe at following times {}'.format(adjustment))
            return adjustment

    def print_schedule(self):
        if not self.step_mgr.steps:
            return ''
        schedule_str = ''
        schedule = self.step_mgr.steps
        schedule.reverse()
        schedule_str += 'Start at: {}\n'.format(schedule[0].timeback)

        print('To end on time you need to start at {}'.format(self.starttime))

        for step in schedule:

            schedule_str += 'Step: "{}" needs {} minutes to complete, start the ' \
                  'step at "{}"\n'.format(step.explanation,
                                        step.interval,
                                        step.timeback)
        return schedule_str

    def alert(self, tm, event):
        print('Alerted at {}:{}'.format(tm, event))

    def execute(self, schedule):

        for ev in schedule:
            scheduler.enterabs(ev.time, priority,
                               action=self.alert,
                               argument=(),
                               kwargs={tm: ev.time, event: ev.step_name})

    def get_timedelta(self, start_date, end_date):
        """
        For custom scheduling
        :param start_date:
        :param end_date:
        :return:
        """
        try:
            datetime_object = datetime.strptime(start_date, '%b %d %Y %I:%M%p')

            datetime_object2 = datetime.strptime(end_date, '%b %d %Y %I:%M%p')

            start_bake = datetime_object.timestamp()
            end_bake = datetime_object2.timestamp()

            dd = end_bake - start_bake
            timed = timedelta(seconds=dd)
            return timed
        except ValueError as e:
            print('Wrong date time format input'.format(e))


def parse_options():
    example = '''python3 scheduling/simple_scheduler.py 
    --steps simple_scheduler.croissant_schedule'''
    parser = argparse.ArgumentParser(description='Schedule baking', epilog=example)
    parser.add_argument('-d', "--enddate",
                        metavar='enddate',
                        default='Nov 22 2018 2:30PM',
                        required=False,
                        help='endtime string, example: Nov 22 2018 2:30PM')
    parser.add_argument('--steps', required=False,
                        default=recipe_schedule2,
                        help='steps list')
    parser.add_argument('--recipe-id', required=True,
                        help='Unique recipe identificator, example: croissant_3')
    parser.add_argument('--schedule', required=False,
                        help='schedule')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    return args


def main():
    args = parse_options()
    steps_object = locate(args.steps)
    sch = SimpleScheduler(recipe_id=args.recipe_id,
                          steps=steps_object,
                          enddate=args.enddate)

    schedule = sch.simple_schedule()
    print(sch.print_schedule())
    starttime = sch.starttime
    chart = Chart()
    chart.local_gantt(sch.step_mgr.steps)



if __name__ == '__main__':
    main()








