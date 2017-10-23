import os 
import re
import sys
import unittest 
import importlib.util
import subprocess 
import logging
import pexpect
from contextlib import contextmanager

from pathlib import Path 

def make_method(testbase) :
    test_name = 'test_1_exercise_{}'.format(testbase)
    def test_exercise(self) :
        self.do_exercise(testbase + '.py')
    return test_name, test_exercise 

def generate_exercises(cl, *exes) :
    '''Decorator that adds test functions to classes that are derived from unittest.TestCase''' 
    def decorator(cl):
        for ex in exes : 
            testbase = 'ex{}'.format(ex)
            test_name, test_method = make_method(testbase)
            setattr(cl, test_name, test_method)
        # Add the late test.
        def test_is_not_late(self) :
            self.assertIsNone(self.find_file('__late__'))
        setattr(cl, 'test_0_is_not_late', test_is_not_late)
        return cl
    return decorator

class Project(unittest.TestCase) : 
                             
    def find_file(self, name) : 
        p = Path(os.getcwd())
        for cand in p.glob('**/' + name) :
            return cand
        return None
        
    def do_exercise(self, name) :     
        py_file = self.find_file(name)        
        self.assertIsNotNone(py_file, 'You are missing exercise file "{}"'.format(name))
        self.check_docstring(py_file)
        
    def check_docstring(self, filename):
        with open(filename, 'r') as ex :
            contents = ex.read()
        self.assertIsNotNone(re.search(r'cis(\s*|-)15', contents, re.I), "Your source file doesn't seem to have the right docstring")
