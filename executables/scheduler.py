import logging
from datetime import datetime, timedelta
from collections import OrderedDict
import logging
import argparse
import json

recipe_schedule = [('premix', 30, False, True),
                   ('StretchFold', 150, True, True),
                   ('bulk fermentation', 14*60, True, False),
                   ('rest', 30, False, True),
                   ('shape', 30, True, True),
                   ('proof', 4*60, False, False),
                   ('bake', 40, False, True)]

my_shedule = [('Nov 22 2018  5:30PM', 'Nov 22 2018  10:30PM'),
('Nov 23 2018  5:30PM', 'Nov 23 2018  10:30PM')
              ]

class Step:
    def __init__(self, step_name, interval, connected, active):
        self.step_name = step_name
        self.interval = interval*60
        self.next_step = None
        self.connected = False
        self.active_step = True


class RecipeStepManager:
    def __init__(self):
        self.time_unit = 'minutes'
        self.steps = []


    def to_seconds(self, interval, from_u='minutes', to_u='seconds'):
        """
        Interval is an int
        :param interval:
        :param from_u:
        :param to_u:
        :return: int
        """
        return interval * 60

    def add_step(self, name, interval, connected=False, active=True):
        step = Step(name, interval, connected, active)
        self.steps.append(step)

    def construct(self, recipe_schedule):
        for rep in recipe_schedule:
            self.add_step(rep[0], rep[1], rep[2], rep[3])


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
        return input * 60

    def premix(self):
        return 20

    def kneading(self):
        return 10


    def calculate(self, end_date):
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
            print(dir(datetime_object))
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
        #print('Interval to convert {}'.format(s_interval))
        s1 = self.timestamp_from_str(s_interval[0])
        s2 = self.timestamp_from_str(s_interval[1])
        return(s1, s2)

    def delta_from_interval(self, s_interval):
        t_interval = self.convert_interval(s_interval)
        times = self.total_timedelta(t_interval)
        diffs = times[1] - times[0]
        timed = timedelta(seconds=diffs)
        return timed

    def calc_schedule(self):
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
        start_time = my_shedule[0][0]
        print('\n\nI can start at {}'.format(start_time))

        step_index = 0
        schedule_index = 0
        number_of_steps = len(step_mgr.steps)
        schedule_intervals = len(my_shedule)
        for si in my_shedule:

            st, end = self.convert_interval(si)
            print('I have timeslot from: {} to: {}'.format(st, end))

            print('Completed step number {}.{}'.format(step_index, step_mgr.steps[step_index].step_name))

            current_time = st
            while step_index <= number_of_steps:
                step = step_mgr.steps[step_index]
                print('Step: {}, time needed: {} minutes'.
                      format(step.step_name, step.interval / 60))

                delta = timedelta(seconds=step_mgr.steps[step_index].interval)
                current_time = st + delta
                print('This step will be completed at this time {}'.format(current_time))
                if current_time <= end:
                    adjustment[step.step_name] = current_time
                    step_index += 1
                elif not step.active_step:
                    print('Step {} is not active, proceed to next '
                          'schedule interval'.format(step.step_name))
                    step_index += 1
                    continue
                else:
                    print('Oh NO! Do not have time for step {}'.format(step.step_name))
                    break
        if step_index < number_of_steps:
            print('This recipe schedule cannot be completed within the times you gave, '
                  'please add more time')
        else:
            print('You can complete this recipe at following times {}'.format(adjustment))

    def calc_schedulenon(self):
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
        start_time = my_shedule[0][0]
        print('\n\nI can start at {}'.format(start_time))

        step_index = 0
        schedule_index = 0
        number_of_steps = len(step_mgr.steps)
        schedule_intervals = len(my_shedule)

        while step_index <= number_of_steps:
            step = step_mgr.steps[step_index]
            print('Step: {}, time needed: {} minutes'.
                  format(step.step_name, step.interval / 60))

            while schedule_index < schedule_intervals:
                st, end = self.convert_interval(my_shedule[schedule_index])
                print('I have time from: {} to: {}'.format(st, end))

                delta = timedelta(seconds=step_mgr.steps[step_index].interval)
                proceed = st + delta
                print('This step will be completed at this time {}'.format(proceed))
                if proceed <= end:
                    adjustment[step.step_name] = proceed
                    step_index += 1
                else:
                    schedule_index += 1
                    print('Oh NO! Do not have time for step {}'.format(step.step_name))
        if step_index < number_of_steps:
            print('This recipe schedule cannot be completed within the times you gave, '
                  'please add more time')
        else:
            print('You can complete this recipe at following times {}'.format(adjustment))

    # ORIG

    def total_timedelta(self, start_date, end_date):

        start_date = 'Nov 26 2018  2:30PM'
        end_date = 'Nov 24 2018  2:30PM'

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
                        required=True,
                        help='deadline time string, example: Nov 22 2018 2:30PM')
    parser.add_argument('--room_temp', required=False,
                        help='room temperature')
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
    tt.calculate(args.deadline)

    tt.calc_schedule()

if __name__ == '__main__':
    main()
