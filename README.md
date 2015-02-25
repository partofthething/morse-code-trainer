# Morse Code Trainer

This program is one of many that trains you to hear Morse code. It uses the Koch method. 

The philosophy of the Koch method is that you need to learn Morse code as reflexes 
without doing any visual or other translations in your head as you go. You can do this
by learning Morse code at high speed (15 WPM or higher) from the very get-go. The trick is to start with 
just 2 letters: K and M. As soon as you can copy these two letters at high speed to 
90% accuracy for a few minutes, you can add another letter. And so it goes. 

There are lots of programs that train you with the Koch method. Usually these just play the sounds
and print out the letters as they're played. You write down the letters on a piece of paper as you go
and then check how you did after the session ends. 

I had two problems with this training mode:

1. My fingers got tired of writing all the letters on paper.
2. It was tedious and taxing to check my scribbled results with the correct answer. 

This program is designed for people who are good typers. Instead of scribbling on paper, 
you type your copy on the keyboard. Once a session is finished, the computer automatically
checks your results and prints out your accuracy. 

## Requirements
* wxPython for graphics
* pygame for sound
* morsecodelib (my little morse code library)

## Use
Just run clone the repo and run `python gui/gui.py` and the GUI should fire up. 
Press Start to get going. The answers will not show up until the end of your session 
(otherwise they distract you). The field that's highlighted in green is the current 
one to be typing in. 