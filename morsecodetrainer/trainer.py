'''
Trains you
'''

import time
import random
import os
import re
from datetime import datetime

from morsecodelib import sound
from . import config

KOCH_LETTER_ORDER = ['K', 'M', 'R', 'S', 'U', 'A', 'P', 'T', 'L', 'O', 'W', 'I', '.', 'N', 'J', 'E', 'F', '0', 'Y',
                   'V', 'G', '5', '/', 'Q', '9', 'Z', 'H', '3', '8', 'B', '?', '4', '2', '7', 'C', '1', 'D', '6', 'X']

class Trainer(object):
    def __init__(self):
        self.stopped = True
        self.paused = False
        self.elapsed_seconds = 0.0
        self.num_characters = 2
        self.justlast = 0
        self.full_run_completed = False  # for determining whether or not to log score

    def run(self):
        start = time.time()
        paused_start_time = None
        elapsed_paused = 0.0
        self.stopped = False
        morse_sound = sound.MorseSoundPlayer()
        self.elapsed_seconds = 0.0
        self.full_run_completed = False
        valid_letters = KOCH_LETTER_ORDER[:self.num_characters]
        if self.justlast:
            valid_letters = valid_letters[-self.justlast:]
        while self.elapsed_seconds < config.MINUTES_OF_TRAINING * 60.0:
            if self.stopped:
                break
            if self.paused:
                if not paused_start_time:
                    paused_start_time = time.time()
                time.sleep(0.5)
                elapsed_paused += time.time() - paused_start_time
                continue
            else:
                paused_start_time = None
            word = self.make_word(valid_letters)
            morse_sound.text_to_sound(word)
            self.elapsed_seconds = time.time() - start - elapsed_paused
            self.render_correct_answer(word)

        else:
            if not self.justlast:
                # don't log situations when user is just focusing on most recent letters.
                self.full_run_completed = True

        morse_sound.stop()

    def make_word(self, valid_letters):
        return self.make_random(valid_letters)
        # return self.make_callsign(valid_letters)

    def make_random(self, valid_letters):
        length = self.get_length_of_phrase()
        letters = [random.choice(valid_letters) for _i in range(length)]
        word = ''.join(letters)
        return word

    def make_callsign(self, valid_letters):
        """
        make a callsign-like word out of the valids
        """
        length = random.choice([1, 2])
        alphas = [ai for ai in valid_letters if re.search('[A-Z]', ai)]
        numbers = [ai for ai in valid_letters if re.search('[0-9]', ai)]
        letters = [random.choice(alphas) for _i in range(2)]
        letters.append(random.choice(numbers))
        letters.extend([random.choice(alphas) for _i in range(length)])
        word = ''.join(letters)
        return word

    def get_length_of_phrase(self):
        """
        Randomly determine number of chars to use.

        Uniform distributions seem to put too many at 1 or 2 characters.
        """

        # random.choice(range(1,7))
        num = int(random.gauss(4, 1.5))
        if num > 7:
            num = 7
        elif num < 1:
            num = 1
        return num

    def render_correct_answer(self, word):
        """print out latest correct answer"""
        print(word)

    def set_num_characters(self, num_characters):
        self.num_characters = num_characters

    def set_justlast_characters(self, num_off_end):
        """
        Allows user to focus on only the most recently added few characters.
        """
        self.justlast = num_off_end

    def stop(self):
        self.stopped = True

    def log_results(self, accuracy_value):
        """
        Store results so you can see your history
        """
        with open(self.get_log_file_name(), 'a') as log_file:
            log_file.write('<{0}> {1} {2} {3}\n'.format(time.ctime(), self.num_characters,
                                                        config.MINUTES_OF_TRAINING, accuracy_value))

    def get_log_file_name(self):

        log_directory = os.path.join(os.path.expanduser('~'), '.morescodetrainer')
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        return os.path.join(log_directory, 'accuracy_history.txt')

    def plot_history(self):
        """
        Plot training progress as logged
        """
        from matplotlib import pyplot as plt


        times, chars, durations, accuracy = self.read_log()

        transitions = self.get_new_letter_dates(times, chars)

        fig, ax = plt.subplots()
        ax.plot_date(times, accuracy, '-o')
        fig.autofmt_xdate()
        plt.title('Morse Code learning progress')
        plt.ylabel('Accuracy (%)')

        for transition in transitions:
            plt.axvline(x=transition, c='BLACK')

        plt.axhline(y=90, c='RED')

        plt.show()

    def read_log(self):

        log_file_name = self.get_log_file_name()
        if not os.path.exists(log_file_name):
            print('No log file to plot')
            return

        data = []
        with open(log_file_name) as log_file:
            for line in log_file:
                match = re.search('<(.+?)> (\d+) (\d+) (\S+)', line)
                if not match:
                    print('Corrupted log entry: {0}'.format(line))
                timestamp = datetime.fromtimestamp(time.mktime(time.strptime(match.group(1))))
                num_chars = int(match.group(2))
                duration = float(match.group(3))
                accuracy = float(match.group(4))
                data.append((timestamp, num_chars, duration, accuracy))

        times, chars, durations, accuracy = zip(*data)
        return times, chars, durations, accuracy

    def get_historical_max_chars(self):
        """
        return the highgest number of characters the user has logged so far.
        """
        try:
            _times, chars, _durations, _accuracy = self.read_log()
        except:
            return 2
        return max(chars)

    def get_new_letter_dates(self, times, chars):
        """
        Find dates where we added a new letter
        """
        transitions = []
        max_num_chars = chars[0]
        last_tm = times[0]
        for tm, num_chars in zip(times, chars):
            if num_chars > max_num_chars:
                transitions.append(last_tm)
                max_num_chars = num_chars
            last_tm = tm
        return transitions


if __name__ == '__main__':
    trainer = Trainer()
    trainer.plot_history()
