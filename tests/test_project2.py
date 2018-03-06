import unittest
import logging 
import sys 
import pexpect
import random
import re
import os
import time

from selenium import webdriver

from tests import Project, generate_exercises

@generate_exercises(3, 4, 5)
class Project2(Project) : 

    def test_2_check_docstring(self) :
        filename = self.find_file('project2.py')
        self.assertIsNotNone(filename, "I can't find your project file")
        self.check_docstring(filename)

    def test_2_check_output(self) :
        filename = self.find_file('project2.py')
        self.assertIsNotNone(filename, "I can't find your project file")
        
        with open('logs/test_project_2.out', 'a') as log :
            test = pexpect.spawnu('python "' + filename.as_posix() + '"', logfile=log)
            self.assertNotEqual(0, test.expect([pexpect.EOF, "31556925"]))

    def test_3_check_hardcode(self) :
        filename = self.find_file('project2.py')
        self.assertIsNotNone(filename, "I can't find your project file")
        with open(filename) as py :
            for l in py.readlines() :
                if re.search(r'31556925', l) is not None :
                    if not re.search(r'#.*31556925', l) is not None:
                        print ('[warning]: Possbily hardcoded:\n[warning]: ', l) 
        
class Project2_Adv(Project):
    def setUp(self) :
        filename = self.find_file('project2_adv.py')
        if filename is None :
            raise unittest.SkipTest('No project2_adv.py is present.')
        self.driver = webdriver.Firefox()

    def tearDown(self) :
        self.driver.close()
        
    def test_web(self):
        os.putenv('FLASK_DEBUG', '1')
        filename = self.find_file('project2_adv.py')
        wd = os.path.dirname(filename)
        with open('logs/flask.out', 'a') as log :
            test = pexpect.spawnu('python  project2_adv.py', logfile=log, cwd=wd)
            result = test.expect([pexpect.EOF, '0.0.0.0'])
            self.driver.get('http://localhost:8080/')

            time.sleep(1)
            self.driver.get_screenshot_as_file('logs/screen.png')

if __name__ == '__main__' : 
    unittest.main(verbosity=0, exit=False)
