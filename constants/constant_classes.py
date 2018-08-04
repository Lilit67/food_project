import math

class Units:
    gram = 'gr'
    lb = 'lb'
    oz = 'oz'


class Hydration:
    low_hydration = 50
    low_medium_hydration = 60
    common_hydration = 70
    high_hydration = 85
    rather_high_hydration = 90
    very_high_hydration = 95
    hundred_percent_hydration = 100
    over_hundred_hydration = 110

class RecipClassifier:
    sourdough = 'sourdough'


class HydrationCalculator:
    """ Return percent hydration"""
    @staticmethod
    def honey_hydration(honey_weight):
        """
        Honey is 50 percent water

        """
        return math.percent(honey_weight)

    @staticmethod
    def starter_hydration(starter_weight):
        """

        :param starter_weight:
        :return:
        """
        return 50

    @staticmethod
    def starter_dry_weight(weight, default_hydration=100):
        """
        starter_weight = 100%
        water_weight = 50%
        water_weight = starter_weight * 50 / 100
        :param weight:
        :param default_hydration:
        :return:
        """
        return weight
