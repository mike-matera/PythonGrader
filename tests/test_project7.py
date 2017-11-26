import unittest
import logging 
import sys 
import pexpect
import random
import os
import time
import importlib
import importlib.util
import tempfile

from selenium import webdriver

from tests import Project, generate_exercises, io_control

@generate_exercises(29, 30, 31)
class Project7(Project) :

    def setUp(self) :
        filename = self.find_file('project7.py')
        self.assertIsNotNone(filename, "I can't find your project file (project7.py)")       self.proj = self.import_project(filename)

    def test_0_check_docstring(self):
        filename = self.find_file('project7.py')
        self.assertIsNotNone(filename, "I can't find your project file (project7.py)")
        self.check_docstring(filename)


    def test_1_play_game(self) :
        filename = self.find_file('project7.py')
        self.assertIsNotNone(filename, "I can't find your project file (project7.py)")

        with open('logs/test_1_play_game.out', 'a') as log :
            test = pexpect.spawnu('python ' + filename.as_posix(), logfile=log, encoding='utf-8')
            door = random.randrange(1, 4)
            test.sendline(str(door))
            test.sendline('stay')            
            got = test.expect([pexpect.TIMEOUT, '(?i)goat', '(?i)car'], timeout=1)
            test.close()

            test = pexpect.spawnu('python ' + filename.as_posix(), logfile=log, encoding='utf-8')
            door = random.randrange(1, 4)
            test.sendline(str(door))
            test.sendline('switch')            
            got = test.expect([pexpect.TIMEOUT, '(?i)goat', '(?i)car'], timeout=1)
            test.close()

    def test_2_monty_door_docstring(self) :
        self.assertIsNotNone(self.proj.monty_door.__doc__,
                           "Your monty_door() function doesn't have a docstring.")

    def test_3_has_won_docstring(self) :
        self.assertIsNotNone(self.proj.has_won.__doc__,
                           "Your has_won() function doesn't have a docstring.")

    def monty_is_valid(self, car, guess, monty) :
        if   guess == 1 and car == 1 :
            return monty == 2 or monty == 3
        elif guess == 1 and car == 2 :
            return monty == 3
        elif guess == 1 and car == 3 :
            return monty == 2 
        elif guess == 2 and car == 1 :
            return monty == 3
        elif guess == 2 and car == 2 :
            return monty == 3 or monty == 1 
        elif guess == 2 and car == 3 :
            return monty == 1 
        elif guess == 3 and car == 1 :
            return monty == 2
        elif guess == 3 and car == 2 :
            return monty == 1
        elif guess == 3 and car == 3 :
            return monty == 1 or monty == 2
        
    def test_4_monty_door(self) :
        for guess in range(1, 4) :
            for car in range (1, 4) :
                monty = self.proj.monty_door(car, guess)
                if not self.monty_is_valid(car, guess, monty) :
                    self.fail('Monty made the wrong choice:\n  I chose {} the car is behind {} and Monty opened the door {}'.format(guess, car, monty))

    def ref_won(self, car, guess, choice) :
        if choice == 'switch' and guess != car :
            return True
        elif choice == 'stay' and guess == car :
            return True
        else:
            return False

    def test_5_has_won(self) :
        for guess in range(1, 4) :
            for car in range(1, 4) :
                for ss in ['stay', 'switch'] :
                    won = self.proj.has_won(car, guess, ss)
                    if won != self.ref_won(car, guess, ss) :
                        self.fail("You told me I won when I should have lost")
                        
if __name__ == '__main__' : 
    unittest.main(verbosity=2, exit=False)
