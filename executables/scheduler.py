import logging
from datetime import datetime
from collections import OrderedDict
import logging
import argparse
import json

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
    end_date = 'Nov 22 2018  2:30PM'
    regimen = [('Nov 22 2018  2:30PM','Nov 22 2018  3:30PM'), (), (), ()]
    tt.calculate(args.deadline)

if __name__ == '__main__':
    main()
