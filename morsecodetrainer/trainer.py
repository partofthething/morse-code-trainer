'''
Trains you
'''

import time
import random

from morsecodelib import sound
import config


class Trainer(object):
    def __init__(self):
        self.stopped = False
        self.elapsed_seconds = 0.0
    
    def run(self):
        start = time.clock()
        morse_sound = sound.MorseSoundPlayer()
        self.elapsed_seconds = 0.0
        while self.elapsed_seconds < config.MINUTES_OF_TRAINING*60.0:
            length = random.choice(range(1,7))
            letters = [random.choice(['M','K']) for _i in range(length)]
            word = ''.join(letters)
            morse_sound.text_to_sound(word)
            self.elapsed_seconds = time.clock() - start
            self.render_correct_answer(word)
            if self.stopped:
                break
    
    def render_correct_answer(self, word):
        """print out latest correct answer"""
        print word
        
    def stop(self):
        self.stopped = True
        
if __name__ == '__main__':
    trainer = Trainer()
    trainer.run()