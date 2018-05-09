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
import inspect

from selenium import webdriver

from tests import Project, generate_exercises, io_control

from test_project5 import __Project5

class Project5Regrade(__Project5, Project) :
    def setUp(self) :
        self.projfile = 'project6.py'

@generate_exercises(18, 19, 20, 21)
class Project6(Project):

    def setUp(self) :
        filename = self.find_file('project6.py')
        spec = importlib.util.spec_from_file_location("project6", filename)
        self.proj = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.proj)
        self.madlib = ['test1 {} test2 {} test3 {} test4\n', 'foo\n', 'bar\n', 'bak\n']        
        self.words = ['abc\n', 'def\n', 'ghi\n']
        
    def test_2_docstrings(self):
        '''Your functions should each have docstrings.'''
        self.banner("Checking your functions for docstrings.")
        self.assertIsNotNone(self.proj.read_madlib_file.__doc__,
                           "Your read_madlib_file() function doesn't have a docstring.")
        
        self.assertIsNotNone(self.proj.do_madlib_input.__doc__,
                           "Your do_madlib_input() function doesn't have a docstring.")

        self.assertIsNotNone(self.proj.display_madlib.__doc__,
                            "Your display_madlib() function doesn't have a docstring.")

    def test_3_read_madlib_file(self):
        '''The read_madlib_file() function did not return what I expexed. See the log files.'''
        self.banner("Testing your read_madlib_file() function.")
        infile = os.path.join('logs', 'read_madlib_file_input.txt')
        outfile = os.path.join('logs', 'read_madlib_file_output.txt')
        with open(infile, 'w') as madfile :
            for l in self.madlib :
                madfile.write(l)

        got = self.proj.read_madlib_file(infile)
        for i, g in enumerate(got) :
            self.assertEqual(g.strip(), self.madlib[i].strip(), "")

    def test_4_do_madlib_input(self) :
        '''The do_madlib_input() function did not return the words I entered.''' 
        self.banner("Testing your do_madlib_input() function.")
        with io_control(''.join(self.words)) as stdout :
            words = self.proj.do_madlib_input(*self.madlib[1:])

        for i, word in enumerate(words) :
            self.assertEqual(word.strip(), self.words[i].strip())

    def test_5_display_madlib(self):
        '''The display_madlib() function didn't work as expected.''' 
        self.banner("Testing your display_madlib() function.")
        outfile = os.path.join('logs', 'display_madlib_output.txt')
        madlib = 'Foo Bar Bak Baz'
        with io_control('') as stdout :
            self.proj.display_madlib(madlib, outfile)
            got = stdout.getvalue()

        self.assertEqual(got.strip(), madlib.strip())
        self.assertTrue(os.path.exists(outfile), \
                        "I asked you to create {} and I don't see it.".format(outfile))

        with open(outfile) as m :
            got = m.read()

        self.assertEqual(got.strip(), madlib.strip())
                         
class Project6_Adv(Project):

    def setUp(self) :
        filename = self.find_file('project6_adv.py')
        if filename is None :
            raise unittest.SkipTest('No project6_adv.py is present.')
        self.driver = webdriver.Firefox()

    def tearDown(self) :
        self.driver.close()
        
    def test_web(self):
        os.putenv('FLASK_DEBUG', '1')
        filename = self.find_file('project6_adv.py')
        wd = os.path.dirname(filename)

        self.madlib = 'blah1 {} blah2 {} blah3 {} blah4'
        self.txtfile = 'test_madlib.txt'
        self.types = ['word_typ1', 'word_typ2', 'word_typ3']
        self.values = ['foo', 'bar', 'baz']

        with open('logs/flask.out', 'a') as log :
            test = pexpect.spawnu('bash -c ". ~/PythonGrader/env2.7/bin/activate && python  project6_adv.py"', logfile=log, cwd=wd)
            result = test.expect([pexpect.EOF, '0.0.0.0'])
            self.driver.get('http://localhost:8080/')

            try:
                inputs = self.driver.find_elements_by_tag_name('input')
                inputs[0].send_keys(self.madlib)
                inputs[1].send_keys(self.types[0])
                inputs[2].send_keys(self.types[1])
                inputs[3].send_keys(self.types[2])
            
                self.driver.get_screenshot_as_file('logs/madlib_form.png')
                self.driver.find_element_by_tag_name('form').submit()
            except:
                self.fail("I couldn't understand the first form you sent me.")

            time.sleep(1)
            try:
                inputs = self.driver.find_elements_by_tag_name('input')
                inputs[0].send_keys(self.values[0])
                inputs[1].send_keys(self.values[1])
                inputs[2].send_keys(self.values[2])
            
                self.driver.get_screenshot_as_file('logs/word_form.png')
                self.driver.find_element_by_tag_name('form').submit()
            except:
                self.fail("I couldn't understand the second form you sent me.")

            time.sleep(1)
            self.driver.get_screenshot_as_file('logs/final_form.png')

            test.close()
            test.wait()

        self.outfile = os.path.join(wd, 'madlib_log.txt')
        self.assertTrue(os.path.isfile(self.outfile), "I can't file the output file " + self.outfile)
        with open (self.outfile) as f :
            line = f.readline().strip()
        self.assertEqual(line, self.madlib.format(*self.values), "The madlib you saved doesn't match what I expected.")
        
            
if __name__ == '__main__' : 
    unittest.main(verbosity=0, exit=False)

