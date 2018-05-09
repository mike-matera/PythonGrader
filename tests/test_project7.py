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
        self.assertIsNotNone(filename, "I can't find your project file (project7.py)")
        self.proj = self.import_project(filename)

    def test_2_check_docstring(self):
        '''Your program should have a valid docstring. 
Check the lecture notes for how to properly format a docstring.
'''
        self.banner("Looking for your program's docstring.")        
        filename = self.find_file('project7.py')
        self.assertIsNotNone(filename, "I can't find your project file (project7.py)")
        self.check_docstring(filename)

    def test_3_play_game(self) :
        '''I had a problem playing the Monty Hall game'''
        self.banner("Checking game play.")        
        filename = self.find_file('project7.py')
        self.assertIsNotNone(filename, "I can't find your project file (project7.py)")

        with open('logs/test_1_play_game.out', 'a') as log :
            test = pexpect.spawnu('python "' + filename.as_posix() + '"', logfile=log, encoding='utf-8')
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

    def test_4_pick_random_door_docstring(self) :
        '''You are missing a docstring in a function.'''
        self.banner('Looking for the docstring on pick_random_door()') 
        self.assertIsNotNone(self.proj.pick_random_door.__doc__,
                           "Your pick_random_door() function doesn't have a docstring.")

    def test_4_montys_choice_docstring(self) :
        '''You are missing a docstring in a function.''' 
        self.banner('Looking for the docstring on montys_choice()') 
        self.assertIsNotNone(self.proj.montys_choice.__doc__,
                           "Your montys_choice() function doesn't have a docstring.")

    def test_4_has_won_docstring(self) :
        '''You are missing a docstring in a function.''' 
        self.banner('Looking for the docstring on has_won()') 
        self.assertIsNotNone(self.proj.has_won.__doc__,
                           "Your has_won() function doesn't have a docstring.")

    def test_5_random_door(self) :
        '''Your random_door() function returned an incorrect result.'''
        self.banner('Checking the result of the pick_random_door() function.''') 
        for i in range(10) :
            doors = self.proj.pick_random_door()
            self.assertEqual(len(doors), 3, '''Your pick_random_door() function didn't return three values.''')
            trues = 0
            for door in doors :
                if type(door) != bool :
                    self.fail('''Your pick_random_door() returned a value that was not a bool.''')
                if door :
                    trues += 1
            self.assertEqual(1, trues, '''Your pick_random_door() function returned more than one True value.''') 
            
    
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

    def test_6_montys_choice(self) :
        '''Your montys_choice() function returned an incorrect result.'''
        self.banner('Checking the montys_choice() function.') 
        for guess in range(1, 4) :
            for car in range (1, 4) :
                doors = [False, False, False]
                doors[car-1] = True 
                monty = self.proj.montys_choice(*doors, guess)
                if not self.monty_is_valid(car, guess, monty) :
                    self.fail('Monty made the wrong choice:\n  I chose {} the car is behind {} and Monty opened the door {}'.format(guess, car, monty))

    def ref_won(self, car, guess, choice) :
        if choice == 'switch' and guess != car :
            return True
        elif choice == 'stay' and guess == car :
            return True
        else:
            return False

    def test_7_has_won(self) :
        '''Your has_won() function returned an incorrect result.'''
        self.banner('Checking the has_won() function.')
        stdout = sys.stdout
        sys.stdout = None
        try :
            for guess in range(1, 4) :
                for car in range(1, 4) :
                    doors = [False, False, False]
                    doors[car-1] = True 
                    for ss in ['stay', 'switch'] :
                        won = self.proj.has_won(*doors, guess, ss == 'switch')
                        if won != self.ref_won(car, guess, ss) :
                            self.fail("You told me I won when I should have lost. The car is behind door {}, the user initally cose door {} and then decided to {}".format(car, guess, ss))
        finally:
            sys.stdout = stdout
            
if __name__ == '__main__' : 
    unittest.main(verbosity=0, exit=False)
