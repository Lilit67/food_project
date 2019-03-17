import sqlite3
import os
import argparse

import speaker


class BakerAssistant(object):
    def __init__(self, mastername):
        self.mastername = mastername
        self.speaker = speaker.Speaker()



    def activate_speaker(self):
        pass



