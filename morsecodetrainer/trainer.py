'''
Trains you
'''

import time
import random

from morsecodelib import sound
import config

KOCH_LETTER_ORDER=['K', 'M', 'R', 'S','U','A','P','T','L','O','W','I','.','N','J','E','F','0','Y',
                   'V','G','5','/','Q','9','Z','H','3','8','B','?','4','2','7','C','1','D','6','X']

class Trainer(object):
    def __init__(self):
        self.stopped = False
        self.elapsed_seconds = 0.0
        self.num_characters = 2
        self.full_run_completed = False # for determining whether or not to log score
  
    def run(self):
        start = time.time()
        morse_sound = sound.MorseSoundPlayer()
        self.elapsed_seconds = 0.0
        self.full_run_completed = False
        while self.elapsed_seconds < config.MINUTES_OF_TRAINING*60.0:
            length = self.get_length_of_phrase()
            letters = [random.choice(KOCH_LETTER_ORDER[:self.num_characters]) for _i in range(length)]
            word = ''.join(letters)
            morse_sound.text_to_sound(word)
            self.elapsed_seconds = time.time() - start
            self.render_correct_answer(word)
            if self.stopped:
                break
        else:
            self.full_run_completed = True
            
    def get_length_of_phrase(self):
        """
        Randomly determine number of chars to use. 
        
        Uniform distributions seem to put too many at 1 or 2 characters. 
        """
        
        #random.choice(range(1,7))
        num = int(random.gauss(4,1.5))
        if num>7:
            num = 7
        elif num<1:
            num = 1
        return num
    
    def render_correct_answer(self, word):
        """print out latest correct answer"""
        print word
    
    def set_num_characters(self, num_characters):
        self.num_characters = num_characters
        
    def stop(self):
        self.stopped = True
        
if __name__ == '__main__':
    trainer = Trainer()
    trainer.run()