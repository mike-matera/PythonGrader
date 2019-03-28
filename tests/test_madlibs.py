import unittest
import logging 
import sys 
import pexpect
import random
import os
import time

from selenium import webdriver

from tests import Project, generate_exercises

class Project4(Project) :

    def setUp(self):
        self.proj_file = 'mad_lib.py'

    def test_04_correct_madlib(self):
        """Your program didn't produce the madlib that I expected"""
        self.banner("Checking the output of your madlib program.")
        filename = self.find_file(self.proj_file)
        self.assertIsNotNone(filename, f"I can't find your project file ({self.proj_file})")

        madlib = 'this is {noun} test fun {adjective} test blah {verb}'
        cmdline = 'python "' + filename.as_posix() + "\" '" + madlib + "'"
        noun = 'foobar'
        adjective = 'baz'
        verb = 'snaz'
        solution = madlib.format(noun=noun, verb=verb, adjective=adjective)
        
        with open('logs/test_correct_madlib.out', 'a') as log :
            test = pexpect.spawnu(cmdline, logfile=log, echo=False)

            for i in range(1,4) :
                got = test.expect([pexpect.EOF, '(?i)adjective', '(?i)verb', '(?i)noun'])
                if got == 0 :
                    self.fail('Your program never said "adjective" "adverb" or "noun"')
                elif got == 1 :
                    test.sendline(adjective)
                elif got == 2 : 
                    test.sendline(verb)
                elif got == 3 :
                    test.sendline(noun)

            got = test.expect([pexpect.EOF, solution])
            if got == 0 :
                self.fail("I never saw the complteted madlib: "+ solution)
            
        self.check_docstring(filename)


    def _xxx_test_05_bogus_madlib(self):
        """Your program didn't handle an error (extra credit not done)"""
        self.banner("Looking for the extra credit.")
        filename = self.find_file(self.proj_file)
        self.assertIsNotNone(filename, f"I can't find your project file ({self.proj_file})")

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


class Project4_Adv(Project):

    def setUp(self) :
        filename = self.find_file('project4_adv.py')
        if filename is None :
            raise unittest.SkipTest('No project4_adv.py is present.')
        self.driver = webdriver.Firefox()

    def tearDown(self) :
        self.driver.close()
        
    def test_web(self):
        os.putenv('MADLIB', 'this is {verb} test fun {adverb} test {noun}')
        os.putenv('FLASK_DEBUG', '1')
        filename = self.find_file('project4_adv.py')
        wd = os.path.dirname(filename)
        with open('logs/flask.out', 'a') as log :
            test = pexpect.spawnu('python  project4_adv.py', logfile=log, cwd=wd)
            result = test.expect([pexpect.EOF, '0.0.0.0'])
            self.driver.get('http://localhost:8080/')

            try:
                inputs = self.driver.find_elements_by_tag_name('input')
                inputs[0].send_keys('compile')
                inputs[1].send_keys('crumily')
                inputs[2].send_keys('keyboard')
            
                self.driver.get_screenshot_as_file('logs/web_form.png')
                self.driver.find_element_by_tag_name('form').submit()
            except:
                self.fail("I couldn't understand the form you sent me.")

            time.sleep(1)
            self.driver.get_screenshot_as_file('logs/completed_madlib.png')

if __name__ == '__main__' : 
    unittest.main(verbosity=0, exit=False)

