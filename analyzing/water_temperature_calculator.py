class WaterTemperatureCalculator:
    def __init__(self):
        pass

    def reference(self):
        return "http://www.wildyeastblog.com/water/"

    @staticmethod
    def water_temp_preferment(desired_dough_temp, room_temp, flour_temp,
                   preferment_temp, mixing_friction, scale='F'):
        """
        TODO: what is the source of this info?
        Smart function to calculate optimal water temperature
        :param input1:
        :param input2:
        :return:
        """

        water_temp = (4 * desired_dough_temp) - room_temp - \
                flour_temp - preferment_temp - mixing_friction

        return water_temp

    @staticmethod
    def water_temp_no_preferment(desired_dough_temp, room_temp, flour_temp,
                   mixing_friction, scale='F'):
        """
        Same as above without preferment
        :return:
        """
        water_temp = (3 * desired_dough_temp) - room_temp - \
                     flour_temp - mixing_friction
        return water_temp