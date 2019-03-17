from datetime import timedelta
from time_unit import TimeUnit as timeunit


class Step:
    def __init__(self, recipe_id, step_name, interval, connected, active,
                 unit=timeunit.minutes, explanation=''):
        self.recipe_id = recipe_id
        self.step_name = step_name
        self.unit = unit
        self.duration = timedelta(minutes=interval)
        self.explanation = explanation
        self.internal_units = timeunit.seconds
        self.interval = self.to_seconds(interval, self.internal_units)
        self.next_step = None
        self.stretch = self.to_seconds(connected, self.internal_units)
        self.active_step = active
        self.completed = False
        self.timeback = 0
        self.step_start_time = 0
        self.step_end_time = None

    def set_timeback(self, current):
        self.timeback = current - self.duration
        self.step_end_time = self.timeback

    def set_start(self, start):
        self.step_start_time = start

    def __str__(self):
        return self.step_name

    def to_seconds(self, input, unit=timeunit.minutes):
        """
        Convert to seconds
        :param input:
        :param unit:
        :return:
        """
        if unit == timeunit.seconds:
            return input
        elif unit == timeunit.minutes:
            return input * 60
        elif unit == timeunit.hours:
            return input * 60 * 60
        elif unit == timeunit.days:
            return input * 60 * 60 * 24
        else:
            raise Exception('Larger than days input is not supported')

    def to_minutes(self, input, unit=timeunit.seconds):
        if unit == timeunit.minutes:
            return input
        elif unit == timeunit.seconds:
            return input / 60
        elif unit == timeunit.hours:
            return input * 60
        elif unit == timeunit.days:
            return input * 60 * 24
        else:
            raise Exception('Larger than days input is not supported')

    def duration(self):
        return self.interval.to_init


####### NOT USED YET

class Autolyze(Step):
    def __init__(self, active, duration, extension, min_time, max_time):
        Step.__init__(self, active, duration, extension)
        self.min_time = min_time
        self.max_time = max_time
        self._step_name = __class__.__name__

class StretchAndFold(Step):
    def __init__(self, active, duration, extension, min_time, max_time):
        Step.__init__(self, active, duration, extension)
        self.min_time = min_time
        self.max_time = max_time
        self._step_name = __class__.__name__

