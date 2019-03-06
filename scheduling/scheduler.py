import logging
from datetime import datetime, timedelta
from collections import OrderedDict
import logging
import argparse
import json

# name, interval, stretch, active
recipe_schedule = [('premix', 30, 8*60, False),
                   ('StretchFold', 150, 60, True),
                   ('bulk fermentation', 14*60, 60, False),
                   ('bench rest', 30, 20, True),
                   ('shape', 30, 40, True),
                   ('proof', 4*60, 4*60, False),
                   ('bake', 40, 0, True)]

# interval, connected, active
# if connected to previous and active, cannot take the next user timeslot
recipe_schedule2 = [('premix', 10, 50, True),
                    ('autolyze', 8 * 60, 90, True),
                   ('StretchFold', 150, 200, True),
                   ('bulk fermentation', 14*60, 90, False),
                   ('bench rest', 30, 60, True),
                   ('shape', 30, 0, True),
                   ('proof', 4*60, 8*60, False),
                   ('bake', 40, 0, True)]

# interval, connected, active
recipe_schedule_impossible = [('premix', 100, True, True),
                    ('autolyze', 8 * 60, True, True),
                   ('StretchFold', 150, True, True)]


my_schedule = [('Nov 22 2018  5:30PM', 'Nov 22 2018  10:30PM'),
('Nov 23 2018  5:30PM', 'Nov 24 2018  1:30AM'),
               ('Nov 24 2018  1:30PM', 'Nov 24 2018  1:30AM')]

my_schedule2 = [('Nov 22 2018  5:30PM', 'Nov 22 2018  10:30PM'),
('Nov 23 2018  5:30PM', 'Nov 23 2018  11:30PM'),
               ('Nov 26 2018  5:30PM', 'Nov 23 2018  11:30PM')]

class BakerTimeManager:
    """
    String interval
    """
    def __init__(self, schedule):

        self.schedule = schedule
        self.start_time, self.end_time = self.all_timeline()
        self.length = len(self.schedule)
        self.current = 0

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
        """ Timedelta from string interval"""
        t_interval = self.convert_interval(s_interval)
        times = self.total_timedelta(t_interval)
        diffs = times[1] - times[0]
        timed = timedelta(seconds=diffs)
        return timed

    def all_timeline(self):
        start = self.schedule[0][0]
        end = self.schedule[-1][1]
        interval = (start, end)
        self.all_time = self.convert_interval(interval)
        print(self.all_time)
        return self.all_time

    def next_window(self):

        while self.current < self.length:
            self.current += 1
            yield self.current
        raise Exception('No more windows left!')

    def apply_stretch(self, current):
        print('{}: using extended time {}'.format(step.step_name, step.stretch))
        
        step_end = step_end + stretch
        if step_end >= start and step_end <= end:
            print ('Step can complete at this time, '
                   'with extended step time {} {}'.format(start, end))

    def inside(self, step, step_end, stretch=0):

        start, end = self.convert_interval(self.schedule[self.current])
        if step_end >= start and step_end <= end:
            return True
        else:
            print('Oops!!! Step #{} is outside window. Lets move to check next interval '
                  'window in your schedule'.format(step.step_name))
            #self.current += 1
            self.next_window()
            # proceed to check next time intervals
            while self.current < len(self.schedule):
                start, end = self.convert_interval(self.schedule[self.current])
                print('Next window starts {} and ends {}'.format(start, end))
                # free time interval ends earlier than recipe step time
                if end < step_end:
                    print('Skip over this interval {} {}'.format(start, end))
                    self.current += 1
                    #self.next_window()
                    continue
                else:
                    if step_end >= start and step_end <= end:
                        return True
                    else:
                        print('Step {} can be extended up to: {}'.format(step.step_name, step.stretch))
                        extention = step_end + stretch
                        if extention >= start:  # and extention <= end:
                            print('Step {} can be extended to time: {}'.format(start))

                            print ('Correcting step end time to {}'
                                   .format(start))
                            #self.current_time =
                            return True
                        else:
                            return False

        return False


class Step:
    def __init__(self, step_name, interval, connected, active):
        self.step_name = step_name
        self.interval = self.to_seconds(interval)
        self.next_step = None
        self.stretch = self.to_seconds(connected)
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
            raise Exception('For now days conversion is not supported')

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
        if unit == 'min':
            return input * 60
        elif unit == 'seconds':
            return input
        elif unit == 'hours':
            return input * 60 * 60
        else:
            raise Exception('Days is not supported')


    def schedule_preparation(self, recipe_schedule, my_schedule):
        """
        both ended: good
        shedule ended: good
        my time ended: bad
        :return:
        """
        # init
        step_mgr = RecipeStepManager()
        time_mgr = BakerTimeManager(my_schedule)

        step_mgr.construct(recipe_schedule)
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
            print('This recipe schedule CANNOT be completed within the times you gave, '
                  'please add more time')
            return None
        else:
            print('You CAN complete this recipe at following times {}'.format(adjustment))
            return adjustment


    def total_timedelta(self, start_date, end_date):

        try:
            datetime_object = datetime.strptime(start_date, '%b %d %Y %I:%M%p')

            datetime_object2 = datetime.strptime(end_date, '%b %d %Y %I:%M%p')

            start_bake = datetime_object.timestamp()
            end_bake = datetime_object2.timestamp()

            dd = end_bake - start_bake
            timed = timedelta(seconds=dd)
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
    sch = Scheduler()
    start_date = 'Nov 22 2018  2:30PM'
    end_date = 'Nov 24 2018  2:30PM'
    sch.total_timedelta(start_date, end_date)

    datetime_object = datetime.strptime(end_date, '%b %d %Y %I:%M%p')

    regimen = [('Nov 22 2018  2:30PM','Nov 22 2018  3:30PM'), (), (), ()]
    #tt.calculate(args.deadline)

    #tt.calc_schedule(recipe_schedule, my_schedule)
    sch.schedule_preparation(recipe_schedule, my_schedule)


if __name__ == '__main__':
    main()
