
class EggConverter:

    @staticmethod
    def grams_to_eggs(grams):
        return int(grams/50)

    @staticmethod
    def egg_to_gram(eggs):
        return int(eggs) * 50

    @staticmethod
    def eggs_or_ea(eggs):
        if eggs > 10:
            return 'grams'
        else:
            return 'ea'

