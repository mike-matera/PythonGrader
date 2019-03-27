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

@generate_exercises(32, 33, 35)
class Project8(Project) :


    def test_0_check_docstring(self):
        filename = self.find_file('project8.py')
        self.assertIsNotNone(filename, "I can't find your project file (project8.py)")
        self.check_docstring(filename)


    def test_1_do_valid_sim(self) :
        '''Your program gave me unexpected resutlts when I tried to run a simulation.'''
        self.banner("Running a simulation with your program.")
        filename = self.find_file('project8.py')
        self.assertIsNotNone(filename, "I can't find your project file (project8.py)")

        with open('logs/test_1_valid_sim.out', 'a') as log :
            test = pexpect.spawnu('python "' + filename.as_posix() + '"', logfile=log, encoding='utf-8')
            turns = random.randrange(100, 100000)
            test.sendline(str(turns))
            try : 
                got = test.expect(['(\d+\.\d+)\s*%'], timeout=5)
                switch_percent = float(test.match.group(1))
                got = test.expect(['(\d+\.\d+)\s*%'], timeout=5)
                stay_percent = float(test.match.group(1))
            except :
                self.fail("The grader program failed to parse the output of your project.")

            if not (64 < switch_percent < 68) :
                self.fail('Your switch percentage ({}) is out of range.'.format(switch_percent))
            if not (31 < stay_percent < 35) :
                self.fail('Your stay percentage ({}) is out of range.'.format(stay_percent))
            test.close()

    def test_2_bogus_input(self) :
        '''Your program didn't handle bogus input properly.'''
        self.banner("Running your program with a little bogus input.") 
        filename = self.find_file('project8.py')
        self.assertIsNotNone(filename, "I can't find your project file (project8.py)")

        with open('logs/test_2_bogus_input.out', 'a') as log :
            test = pexpect.spawnu('python "' + filename.as_posix() + '"', logfile=log, encoding='utf-8')
            turns = random.randrange(200, 100000)
            test.sendline('this')
            test.sendline('is')
            test.sendline('bogus')
            test.sendline('-10')
            test.sendline('100001')
            test.sendline(str(turns))
            try : 
                got = test.expect([pexpect.EOF, '(\d+\.\d+)\s*%'], timeout=5)
                switch_percent = float(test.match.group(1))
                got = test.expect([pexpect.EOF, '(\d+\.\d+)\s*%'], timeout=5)
                stay_percent = float(test.match.group(1))
            except :
                self.fail("The grader program failed to parse the output of your project.")

            if not (64 < switch_percent < 68) :
                self.fail('Your switch percentage ({}) is out of range.'.format(switch_percent))
            if not (31 < stay_percent < 35) :
                self.fail('Your stay percentage ({}) is out of range.'.format(stay_percent))
            test.close()

class Project8_XC(Project) :

    def setUp(self) :
        filename = self.find_file('project8_xc.py')
        if filename is None :
            raise unittest.SkipTest('No project8_xc.py is present.')
        self.proj = self.import_project(filename)

    def test_0_check_xc_docstring(self):
        '''Your extra credit should have a docstring'''
        self.banner("Checking the docstring of your extra credit.") 
        filename = self.find_file('project8_xc.py')
        self.check_docstring(filename)

    def test_1_xc_run(self) :
        '''I saw somoething that I didn't expect when running your extra credit'''
        self.banner("Running your extra credit simulation") 
        filename = self.find_file('project8_xc.py')

        doors = random.randrange(10, 100)
        switch_target = 100 * ((doors - 1) / doors)
        stay_target = 100 * (1 / doors)
        target_range = 2
        
        with open('logs/test_extra_credit.out', 'a') as log :
            test = pexpect.spawnu('python ' + filename.as_posix() + ' {}'.format(doors), logfile=log, encoding='utf-8')
            turns = random.randrange(200, 500)
            test.sendline(str(turns))
            try : 
                got = test.expect([pexpect.EOF, '(\d+\.\d+)\s*%'], timeout=5)
                switch_percent = float(test.match.group(1))
                got = test.expect([pexpect.EOF, '(\d+\.\d+)\s*%'], timeout=5)
                stay_percent = float(test.match.group(1))
            except :
                self.fail("The grader program failed to parse the output of your project.")

            if not (switch_target-target_range < switch_percent < switch_target+target_range) :
                self.fail('Your switch percentage ({}) is out of range. It should be between {} and {}'.format(switch_percent, switch_target-target_range, switch_target+target_range))
            if not (stay_target-target_range < stay_percent < stay_target+target_range) :
                self.fail('Your stay percentage ({}) is out of range. It should be between {} and {}'.format(stay_percent, stay_target-target_range, stay_target+target_range))
            test.close()

    def test_2_xc_monty_docstring(self) :
        '''Your monty_door() function doesn't have a docstring'''
        self.banner("Looking for the docstring on extra credit monty_door()")
        self.assertIsNotNone(self.proj.monty_door.__doc__)

    def test_3_xc_monty(self) :
        '''Your monty_door() function returned something I didn't expect'''
        self.banner("Testing your extra credit monty_door() function")
        for run in range(100) :
            doors = random.randrange(5, 100)
            car = random.randrange(1, doors+1)
            pick = random.randrange(1, doors+1)

            got = self.proj.monty_door(car, pick, doors)
            self.assertEqual(type(got), list, "The monty_door() function didn't return a list!")
            if car in got :
                self.fail("Monty opened the door with the car behind it!")

            if pick in got :
                self.fail("Monty opened the door that the user picked.")

            self.assertEqual(len(got), doors-2, 'Monty should have opened {} doors but opened {} instead.'.format(doors-2, len(got)))
            
if __name__ == '__main__' : 
    unittest.main(verbosity=0, exit=False)
