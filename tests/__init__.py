import io
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

@contextmanager
def io_control(input_text='') :
    stdin_buf = io.StringIO(input_text)
    stdout_buf = io.StringIO()

    stdin = sys.stdin
    stdout = sys.stdout
    
    sys.stdin = stdin_buf
    sys.stdout = stdout_buf
    
    yield stdout_buf

    sys.stdin = stdin
    sys.stdout = stdout

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

    def import_project(self, filename) :
        spec = importlib.util.spec_from_file_location('project', filename)
        proj = importlib.util.module_from_spec(spec)
        stdin = sys.stdin
        sys.stdin = None 
        spec.loader.exec_module(proj)
        sys.stdin = stdin
        return proj
    
    def do_exercise(self, name) :     
        py_file = self.find_file(name)        
        self.assertIsNotNone(py_file, 'You are missing exercise file "{}"'.format(name))
        self.check_docstring(py_file)
        
    def check_docstring(self, filename):
        with open(filename, 'r', encoding='utf-8') as ex :
            contents = ex.read()
        self.assertIsNotNone(re.search(r'cis(\s*|-)15', contents, re.I), "Your source file doesn't seem to have the right docstring")
