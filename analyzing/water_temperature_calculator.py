import logging
"""
OK, but what about this mixing friction? Unfortunately this is not a simple, 
single number. The type of mixer, the amount and consistency of the dough, 
and the length of mixing time all affect the mixing friction. 
So it’s a matter of experimentation for each recipe you make, 
but you can make an educated guess. If I’m using my KitchenAid 
mixer to mix about 3 pounds of dough of medium consistency 
(similar to a basic sourdough) for about 10 minutes,
 I’ll start with a guesstimate of 40 for the mixing friction, 
 if I haven’t made that particular recipe before. 
 If I’m going to mix it by hand, though, I’ll guess the number to be around 5, 
 because hand mixing generates much less heat. 
 So I plug my guesstimate into the formula along with the other 
 variables to determine my water temperature. 
 Then when I’m done mixing, I take the temperature of the dough; 
 if it’s what I hoped for, then I know my guess as to 
 mixing friction was correct, and I note this for the next time 
 I make this recipe. If not, I adjust the mixing friction number up or down next time.
"""
logger = logging.getLogger(__name__)

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

    @staticmethod
    def celcius_farenheight(temp):
        """
        Divide by 5, then multiply by 9, then add 32
        (0°C × 9/5) + 32
        :param temp:
        :return:
        """
        return (temp * 9 / 5) + 32

    @staticmethod
    def farenheight_celcius(temp):
        """
        Deduct 32, then multiply by 5, then divide by 9
        (0°F − 32) × 5/9 = -17.78°C
        :param temp:
        :return:
        """
        return (temp - 32) * 5 / 9

def main():
    mixing_friction_mixer = 40
    desired_dough_temp = 76
    room_temp = 64
    flour_temp = 54
    default_mixing_friction_by_hand = 5
    scale = 'F'
    temperature = WaterTemperatureCalculator.water_temp_no_preferment(desired_dough_temp=desired_dough_temp,
                                                                      room_temp=room_temp,
                                                                      flour_temp=flour_temp,
                                                                      mixing_friction=default_mixing_friction_by_hand,
                                                                      scale='F')
    print('Desired dough temperature {} {}'.format(desired_dough_temp, scale))
    print('Room temp {} {}'.format(room_temp, scale))
    print('Flour temp {} {}'.format(flour_temp, scale))
    print('Water temperature should be {} {}'.format(temperature, scale))

if __name__ == '__main__':
    main()