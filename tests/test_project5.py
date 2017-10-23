import unittest
import logging 
import sys 
import pexpect
import random
import os
import time

from selenium import webdriver

from tests import Project, generate_exercises

@generate_exercises(15, 16, 17)
class Project5(Project) : 

    def test_2_check_docstring(self):
        filename = self.find_file('project5.py')
        self.assertIsNotNone(filename, "I can't find your project file (project5.py)")
        self.check_docstring(filename)

    def test_3_check_prompts(self) :
        filename = self.find_file('project5.py')
        self.assertIsNotNone(filename, "I can't find your project file (project5.py)")

        self.madlib = 'blah1 {} blah2 {} blah3 {} blah4'
        self.txtfile = 'test_madlib.txt'
        self.types = ['word_typ1', 'word_typ2', 'word_typ3']
        self.values = ['foo', 'bar', 'baz']
        
        with open(self.txtfile, 'w') as f :
            f.write(self.madlib + '\n')
            for w in self.types :
                f.write(w + '\n')

        with open('logs/test_3_check_prompts.out', 'a') as log :
            test = pexpect.spawnu('python ' + filename.as_posix() + ' ' + self.txtfile, logfile=log)
            for i in range(3) :
                got = test.expect([pexpect.TIMEOUT, self.types[i]], timeout=1)
                if got == 0 :
                    self.fail('You never prompted me for a ' + self.types[i])
                test.sendline(self.values[i])
            test.close()
        

    def test_4_check_output(self) :
        filename = self.find_file('project5.py')
        self.assertIsNotNone(filename, "I can't find your project file (project5.py)")
        
        self.madlib = 'blah1 {} blah2 {} blah3 {} blah4'
        self.txtfile = 'test_madlib.txt'
        self.types = ['word_typ1', 'word_typ2', 'word_typ3']
        self.values = ['foo', 'bar', 'baz']

        with open('logs/test_4_check_outupt.out', 'a') as log :
            test = pexpect.spawnu('python ' + filename.as_posix() + ' ' + self.txtfile, logfile=log)

            for i in range(3) :
                test.sendline(self.values[i])

            got = test.expect([pexpect.TIMEOUT, pexpect.EOF, self.madlib.format(*self.values)], timeout=1)
            if got < 2 :
                self.fail("I didn't see the completed madlib printed.")
            test.close()

    def test_5_check_file(self) :
        
        self.madlib = 'blah1 {} blah2 {} blah3 {} blah4'
        self.txtfile = 'test_madlib.txt'
        self.types = ['word_typ1', 'word_typ2', 'word_typ3']
        self.values = ['foo', 'bar', 'baz']

        self.outfile = self.txtfile + '.complete'
        
        self.assertTrue(os.path.isfile(self.outfile), "I can't file the output file " + self.outfile)
        with open (self.outfile) as f :
            line = f.readline().strip()

        self.assertEqual(line, self.madlib.format(*self.values), "The madlib you saved doesn't match what I expected.")
        
class Project5_Adv(Project):

    def setUp(self) :
        filename = self.find_file('project5_adv.py')
        if filename is None :
            raise unittest.SkipTest('No project5_adv.py is present.')
        self.driver = webdriver.Firefox()

    def tearDown(self) :
        self.driver.close()
        
    def test_web(self):
        os.putenv('FLASK_DEBUG', '1')
        filename = self.find_file('project5_adv.py')
        wd = os.path.dirname(filename)

        self.madlib = 'blah1 {} blah2 {} blah3 {} blah4'
        self.txtfile = 'test_madlib.txt'
        self.types = ['word_typ1', 'word_typ2', 'word_typ3']
        self.values = ['foo', 'bar', 'baz']

        with open('logs/flask.out', 'a') as log :
            test = pexpect.spawnu('python  project5_adv.py', logfile=log, cwd=wd)
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
    unittest.main(verbosity=2, exit=False)

