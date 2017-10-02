import unittest
import logging 
import sys 
import pexpect
import random
import os

from selenium import webdriver

from tests import Project, generate_exercises

@generate_exercises(11, 12, 13, 14)
class Project4(Project) : 

    def test_correct_madlib(self):
        filename = self.find_file('project4.py')
        self.assertIsNotNone(filename, "I can't find your project file (project4.py)")

        madlib = 'this is {verb} test fun {adjective} test blah {noun}'
        cmdline = 'python ' + filename.as_posix() + " '" + madlib + "'"
        verb = '123verb'
        noun = '53noun'
        adjective = '34adjective'
        
        with open('logs/test_correct_madlib.out', 'a') as log :
            test = pexpect.spawnu(cmdline, logfile=log)

            test.sendline(noun)
            test.sendline(verb)
            test.sendline(adjective)

            self.assertNotEqual(0, test.expect([pexpect.EOF, madlib.format(noun=noun, verb=verb, adjective=adjective)]))

        self.check_docstring(filename)


    def test_bogus_madlib(self):
        filename = self.find_file('project4.py')
        self.assertIsNotNone(filename, "I can't find your project file (project4.py)")

        madlib = 'this is {bad} test fun {bogus} test blah {nothing}'
        cmdline = 'python ' + filename.as_posix() + " '" + madlib + "'"
        verb = '123verb'
        noun = '53noun'
        adjective = '34adjective'
        
        with open('logs/test_bogus_madlib.out', 'a') as log :
            test = pexpect.spawnu(cmdline, logfile=log)

            test.sendline(noun)
            test.sendline(verb)
            test.sendline(adjective)

            self.assertNotEqual(0, test.expect([pexpect.EOF, '(?i)sorry']))

        self.check_docstring(filename)

class Project4_Adv(Project):

    def setUp(self) :
        filename = self.find_file('project4_adv.py')
        if filename is None :
            raise unittest.SkipTest('No project4_adv.py is present.')
        self.driver = webdriver.Firefox()

    def tearDown(self) :
        self.driver.close()
        
    def test_web(self):
        os.putenv('MADLIB', 'this is {verb} test fun {adjective} test blah {noun}')
        os.putenv('FLASK_DEBUG', '1')
        filename = self.find_file('project4_adv.py')
        wd = os.path.dirname(filename)
        with open('logs/flask.out', 'a') as log :
            test = pexpect.spawnu('python  project4_adv.py', logfile=log, cwd=wd)
            result = test.expect([pexpect.EOF, '0.0.0.0'])
            self.driver.get('http://localhost:8080/')
            inputs = self.driver.find_elements_by_tag_name('input')
            for field in inputs :
                field.send_keys("blah blah")

            self.driver.get_screenshot_as_file('logs/web_form.png')
            self.driver.find_element_by_tag_name('form').submit()
            self.driver.implicitly_wait(5) 
            self.driver.get_screenshot_as_file('logs/completed_madlib.png')

if __name__ == '__main__' : 
    unittest.main(verbosity=2, exit=False)

