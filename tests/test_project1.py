import unittest
import logging 
import sys 
import pexpect
import random

from tests import Project, generate_exercises

@generate_exercises(1, 2)
class Project1(Project) : 
    pass

if __name__ == '__main__' : 
    unittest.main(verbosity=2, exit=False)
