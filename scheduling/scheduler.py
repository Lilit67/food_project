import logging
from datetime import datetime, timedelta
from collections import OrderedDict
import logging
import argparse
import json

# interval, connected, active
recipe_schedule = [('premix', 30, False, True),
                   ('StretchFold', 150, True, True),
                   ('bulk fermentation', 14*60, True, False),
                   ('rest', 30, False, True),
                   ('shape', 30, True, True),
                   ('proof', 4*60, False, False),
                   ('bake', 40, False, True)]

# interval, connected, active
# if connected to preious and active, cannot take the next user timeslot
recipe_schedule2 = [('premix', 10, True, True),
                    ('autolyze', 8 * 60, False, True),
                   ('StretchFold', 150, True, True),
                   ('bulk fermentation', 14*60, True, False),
                   ('rest', 30, False, True),
                   ('shape', 30, True, True),
                   ('proof', 4*60, False, False),
                   ('bake', 40, False, True)]

# interval, connected, active
recipe_schedule_impossible = [('premix', 100, True, True),
                    ('autolyze', 8 * 60, True, True),
                   ('StretchFold', 150, True, True)]


my_schedule = [('Nov 22 2018  5:30PM', 'Nov 22 2018  10:30PM'),
('Nov 23 2018  5:30PM', 'Nov 23 2018  11:30PM')]

my_schedule2 = [('Nov 22 2018  5:30PM', 'Nov 22 2018  10:30PM'),
('Nov 23 2018  5:30PM', 'Nov 23 2018  11:30PM'),
               ('Nov 26 2018  5:30PM', 'Nov 23 2018  11:30PM')]

class Step:
    def __init__(self, step_name, interval, connected, active):
        self.step_name = step_name
        self.interval = self.to_seconds(interval)
        self.next_step = None
        self.connected = connected
        self.active_step = active
        self.completed = False

    def __str__(self):
        return self.step_name

    def to_seconds(self, input, unit='min'):
        """
        Convert to seconds
        :param input:
        :param unit:
        :return:
        """
        if unit == 'min':
            return input * 60
        elif unit == 'seconds':
            return input
        elif unit == 'hours':
            return input * 60 * 60
        elif unit == 'days':
            return input * 60 * 60 * 24
        else:
            raise Exception('Larger than days input is not supported')

class RecipeStepManager:
    def __init__(self):
        self.time_unit = 'minutes'
        self.steps = []


    def to_seconds(self, input, unit='min'):
        """
        Convert to seconds
        :param input:
        :param unit:
        :return:
        """
        if unit == 'min':
            return input * 60
        elif unit == 'seconds':
            return input
        elif unit == 'hours':
            return input * 60 * 60
        else:
            raise Exception('For now days is not supported')

    def add_step(self, name, interval, connected=False, active=True):
        step = Step(name, interval, connected, active)
        self.steps.append(step)

    def construct(self, recipe_schedule):
        for rep in recipe_schedule:
            self.add_step(rep[0], rep[1], rep[2], rep[3])
        self.to_stages()

    def to_stages(self):
        stages = {}
        index = 0
        current_stage = []
        stage_index = 0
        print(len(self.steps))
        while index < len(self.steps):
            if self.steps[index].connected:
                current_stage.append(self.steps[index])
            else:
                stages[stage_index] = current_stage
                stage_index += 1
                current_stage = []
                current_stage.append(self.steps[index])
            index += 1
        print('Found {} stages: {}'.format(len(stages), stages))
        self.stages = stages


class Scheduler:
    def __init__(self):
        pass

    def to_seconds(self, input, unit='min'):
        """
        Convert to seconds
        :param input:
        :param unit:
        :return:
        """
        if unit == 'min':
            return input * 60
        elif unit == 'seconds':
            return input
        elif unit == 'hours':
            return input * 60 * 60
        else:
            raise Exception('For now days is not supported')

    def calculateOLD(self, end_date):
        """
        Calculate back the time
        :param end_date:
        :return:
        """
        stages = OrderedDict({'premix': 10, 'kneading': 10, 'autolyze': 30, 'stretch_and_fold': 150,
                  'bulk_ferment': 0, 'bench_rest': 30,
                  'preshape': 20, 'shape': 10, 'proof': 240, 'bake': 30,
                  'cool': 60})


        try:
            datetime_object = datetime.strptime(end_date, '%b %d %Y %I:%M%p')

        except ValueError as e:
            print('Wrong date time format input'.format(e))

        end_bake = datetime_object.timestamp()
        start_bake = end_bake - self.to_seconds(60)
        start_proof = start_bake - self.to_seconds(240)
        start_shape = start_proof - self.to_seconds(10)
        start_preshape = start_shape - self.to_seconds(20)
        start_bench_rest = start_preshape - self.to_seconds(30)
        start_bulk_ferment = start_bench_rest - self.to_seconds(30)
        stretch_and_fold = start_bulk_ferment - self.to_seconds(150)

        kneading = stretch_and_fold - self.to_seconds(10)
        autolyze = kneading - self.to_seconds(30)
        premix = autolyze - self.to_seconds(10)
        feed_starter = premix - self.to_seconds(8*60)

        start = feed_starter - self.to_seconds(0)

        print('Start proof: {}'.format(datetime_object.fromtimestamp(start_proof)))
        print('Start baking at {}'.format(datetime_object.fromtimestamp(start_bake)))
        print('End bake at {}'.format(datetime_object.fromtimestamp(end_bake)))

        print('Start feeding starter at {}'.
              format(datetime_object.fromtimestamp(start)))

    def timestamp_from_str(self, strdate):
        datetime_object = datetime.strptime(strdate, '%b %d %Y %I:%M%p')
        stamp = datetime_object #.timestamp()
        return stamp

    def convert_interval(self, s_interval):
        """Interval with timestamps instead of strings"""

        s1 = self.timestamp_from_str(s_interval[0])
        s2 = self.timestamp_from_str(s_interval[1])
        return(s1, s2)

    def delta_from_interval(self, s_interval):
        t_interval = self.convert_interval(s_interval)
        times = self.total_timedelta(t_interval)
        diffs = times[1] - times[0]
        timed = timedelta(seconds=diffs)
        return timed

    def schedule_preparation(self, recipe_schedule, my_schedule):
        """
        while (my_start + interval <= my_end)
        yes: step done, move to next step
        no: proceed to my next free time, no recipe step advanced
        both ended: good
        shedule ended: good
        my time ended: bad
        :return:
        """
        step_mgr = RecipeStepManager()
        step_mgr.construct(recipe_schedule)
        adjustment = {}
        start_time = my_schedule[0][0]
        print('\nStart at this time {}'.format(start_time))

        step_index = 0
        schedule_index = 0
        number_of_steps = len(step_mgr.steps)
        schedule_intervals = len(my_schedule)
        for si in my_schedule:

            st, end = self.convert_interval(si)
            print('\nNext free timeslot is from: {} to: {}\n'.format(st, end))
            current_time = st
            while step_index < number_of_steps:

                step = step_mgr.steps[step_index]
                delta = timedelta(seconds=step_mgr.steps[step_index].interval)
                print(st, delta)
                current_time = current_time + delta
                print('Step # {}:{} needs your active time: {}, needs {} minutes to complete, at: {}'.
                      format(step_index, step.step_name, step.active_step,
                             step.interval / 60, current_time))
                if current_time <= end:
                    adjustment[step.step_name] = current_time

                    print('Completed step # {}. {}'.
                          format(step_index, step_mgr.steps[step_index].step_name))
                    step_index += 1
                elif not step.active_step:
                    # TODO: take into account time step ends and time of next slot
                    print('Step {} is not active, but it will pass the current timeslot, '
                          'so proceed to the next free '
                          'timeslot'.format(step.step_name))
                    step_index += 1
                    break
                else:
                    print('Oh NO! Do not have time for step {}'.format(step.step_name))
                    break
        if step_index < number_of_steps:
            print('This recipe schedule cannot be completed within the times you gave, '
                  'please add more time')
            return None
        else:
            print('You can complete this recipe at following times {}'.format(adjustment))
            return adjustment


    def calc_schedule(self, recipe_schedule, my_schedule):
        """
        mystart + 30 < myend?
        yes: move recipe schedule
        no: move my schedule
        both ended: good
        shedule ended: good
        my time ended: bad
        :return:
        """
        step_mgr = RecipeStepManager()
        step_mgr.construct(recipe_schedule)
        adjustment = {}
        start_time = my_schedule[0][0]
        print('\nStarting at {}'.format(start_time))

        step_index = 0
        schedule_index = 0
        number_of_steps = len(step_mgr.steps)
        schedule_intervals = len(my_schedule)
        for si in my_schedule:

            st, end = self.convert_interval(si)
            print('\nNext free timeslot is from: {} to: {}\n'.format(st, end))
            current_time = st
            while step_index < number_of_steps:

                step = step_mgr.steps[step_index]
                delta = timedelta(seconds=step_mgr.steps[step_index].interval)
                print(st, delta)
                current_time = current_time + delta
                print('Step # {}:{} needs your active time: {}, needs {} minutes to complete, at: {}'.
                      format(step_index, step.step_name, step.active_step,
                             step.interval / 60, current_time))
                if current_time <= end:
                    adjustment[step.step_name] = current_time

                    print('Completed step # {}. {}'.
                          format(step_index, step_mgr.steps[step_index].step_name))
                    step_index += 1
                elif not step.active_step:
                    # TODO: take into account time step ends and time of next slot
                    print('Step {} is not active, but it will pass the current timeslot, '
                          'so proceed to the next free '
                          'timeslot'.format(step.step_name))
                    step_index += 1
                    break
                else:
                    print('Oh NO! Do not have time for step {}'.format(step.step_name))
                    break
        if step_index < number_of_steps:
            print('This recipe schedule cannot be completed within the times you gave, '
                  'please add more time')
            return None
        else:
            print('You can complete this recipe at following times {}'.format(adjustment))
            return adjustment


    def total_timedelta(self, start_date, end_date):

        #start_date = 'Nov 26 2018  2:30PM'
        #end_date = 'Nov 24 2018  2:30PM'

        try:
            datetime_object = datetime.strptime(start_date, '%b %d %Y %I:%M%p')

            datetime_object2 = datetime.strptime(end_date, '%b %d %Y %I:%M%p')
            print(dir(datetime_object))

            start_bake = datetime_object.timestamp()
            end_bake = datetime_object2.timestamp()
            print(dir(datetime_object))
            dd = end_bake - start_bake
            timed = timedelta(seconds=dd)
            print(timed)

        except ValueError as e:
            print('Wrong date time format input'.format(e))



def parse_options():
    parser = argparse.ArgumentParser(description='Schedule baking')
    parser.add_argument('-d', "--deadline",
                        metavar='end_time',
                        type=str,
                        required=False,
                        help='deadline time string, example: Nov 22 2018 2:30PM')
    parser.add_argument('--steps', required=False,
                        help='room temperature')
    parser.add_argument('--schedule', required=False,
                        help='schedule')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    return args



def main():
    args = parse_options()
    tt = Scheduler()
    start_date = 'Nov 22 2018  2:30PM'
    end_date = 'Nov 24 2018  2:30PM'
    tt.total_timedelta(start_date, end_date)

    datetime_object = datetime.strptime(end_date, '%b %d %Y %I:%M%p')

    regimen = [('Nov 22 2018  2:30PM','Nov 22 2018  3:30PM'), (), (), ()]
    #tt.calculate(args.deadline)

    tt.calc_schedule(recipe_schedule, my_schedule)

if __name__ == '__main__':
    main()
