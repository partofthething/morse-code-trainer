'''
Trains you
'''

import time
import random

from morsecodelib import sound


class Trainer(object):
    def __init__(self):
        self.stopped = False
    
    def run(self):
        start = time.clock()
        morse_sound = sound.MorseSoundPlayer()
        elapsed = 0.0
        while elapsed < 60:
            length = random.choice(range(1,7))
            letters = [random.choice(['M','K']) for _i in range(length)]
            word = ''.join(letters)
            morse_sound.text_to_sound(word)
            elapsed = time.clock() - start
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