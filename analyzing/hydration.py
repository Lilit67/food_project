""" Helpers that concern hydration """

import constants.units as units
from smart.ingredients import Waters, Flours


class Hydration:
    low_hydration = 50
    low_medium_hydration = 60
    common_hydration = 70
    high_hydration = 85
    rather_high_hydration = 90
    very_high_hydration = 95
    hundred_percent_hydration = 100
    over_hundred_hydration = 110

    @staticmethod
    def weight(data, unit=gram):
        total = 0
        for w in data:
            total += data[w]
        return total

    @staticmethod
    def bread_hydration(ingredients):
        """
        With only ingredients in list, this method calculates hydration number and returns it.
        This method only counts liquids towards hydration, examples are water, milk, juice
        :param ingredients:
        :return: int
        """
        flours = Flours.get_flours(ingredients)
        waters = Waters.get_waters(ingredients)

        flour_weights = Hydration.weight(flours)
        water_weight = Hydration.weight(waters)

        flour_percent = 100
        hydration = flour_weights * flour_percent / water_weight
        return hydration


    @staticmethod
    def water_weight_in_honey(honey_weight):
        """
        Honey is 50 percent water

        """
        return honey_weight / 2

    @staticmethod
    def water_weight_in_starter(starter_weight):
        """

        :param starter_weight:
        :return:
        """
        return starter_weight / 2

    @staticmethod
    def water():
        return 100

    @staticmethod
    def honey(self):
        return 50

    @staticmethod
    def butter(self):
        return 30

    @staticmethod
    def flour(self):
        return 0

    @staticmethod
    def egg(self):
        return 60

    @staticmethod
    def milk(self):
        return 100



