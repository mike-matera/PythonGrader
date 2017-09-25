import unittest
import logging 
import sys 
import pexpect
import random

from tests import Project, generate_exercises

@generate_exercises(6, 7, 8, 9)
class Project3(Project) : 

    def test_project_3(self) :

        filename = self.find_file('project3.py')
        self.assertIsNotNone(filename, "I can't find your project file (project3.py)")

        a = random.uniform(-10000, 10000)
        b = random.uniform(-10000, 10000)

        with open('logs/test_project_3.out', 'a') as log :
            test = pexpect.spawnu('python ' + filename.as_posix(), logfile=log)

            test.sendline(f"{a}")
            test.sendline(f"{b}")

            self.assertNotEqual(0, test.expect([pexpect.EOF, "a is {}".format(a)]))
            self.assertNotEqual(0, test.expect([pexpect.EOF, "b is {}".format(b)]))
            self.assertNotEqual(0, test.expect([pexpect.EOF, "{}+{}\s*=\s*{}".format(a,b,a+b)]))
            self.assertNotEqual(0, test.expect([pexpect.EOF, "{}-{}\s*=\s*{}".format(a,b,a-b)]))
            self.assertNotEqual(0, test.expect([pexpect.EOF, "{}*{}\s*=\s*{}".format(a,b,a*b)]))
            self.assertNotEqual(0, test.expect([pexpect.EOF, "{}/{}\s*=\s*{}".format(a,b,a/b)]))
            self.assertNotEqual(0, test.expect([pexpect.EOF, "{}%{}\s*=\s*{}".format(a,b,a%b)]))
            self.assertNotEqual(0, test.expect([pexpect.EOF, "{}<{}\s*=\s*{}".format(a,b,a<b)]))
            self.assertNotEqual(0, test.expect([pexpect.EOF, "{}>{}\s*=\s*{}".format(a,b,a>b)]))
            self.assertNotEqual(0, test.expect([pexpect.EOF, "{}=={}\s*=\s*{}".format(a,b,a==b)]))


if __name__ == '__main__' : 
    unittest.main(verbosity=2, exit=False)
