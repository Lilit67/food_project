import json
import os

class BreadStepTiming(object):
    premix = 0
    knead = 0
    autolyze = 0
    stretch_and_fold = 0
    bench_rest = 0
    preshape = 0
    shape = 0
    proof = 0
    bake_vapor = 0
    bake_final = 0

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


