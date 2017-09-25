import os 
import re
import unittest 
import importlib.util
import subprocess 

from pathlib import Path 

subprocess.run('tree', shell=True)

def make_method(testbase) :
    test_name = 'test_exercise_{}'.format(testbase)
    def test_exercise(self) :
        self.do_exercise(testbase + '.py')
    return test_name, test_exercise 

def generate_exercises(cl, *exes) :
    def decorator(cl):
        for ex in exes : 
            testbase = 'ex{}'.format(ex)
            test_name, test_method = make_method(testbase)
            setattr(cl, test_name, test_method) 
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
        self.assertIsNotNone(py_file)

        spec = importlib.util.spec_from_file_location('', py_file)
        module = importlib.util.module_from_spec(spec)
        try : 
            spec.loader.exec_module(module)
        except SyntaxError as e : 
            self.fail('There was a syntax error: ' + str(e))

        print ("DEBUG:", module.__doc__)
        self.assertIsNotNone(module.__doc__, "Your exercise doesn't have a docstring")
        self.assertIsNotNone(re.search('cis-15', str(module.__doc__), re.I), 
                   "I don't see cis-15 in your docstring")

