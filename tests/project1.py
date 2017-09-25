import unittest
import logging 
import sys 

from tests import Project, generate_exercises

@generate_exercises(6, 7, 8, 9)
class Project3(Project) : 
    pass

if __name__ == '__main__' : 
    unittest.main(verbosity=2, exit=False)
