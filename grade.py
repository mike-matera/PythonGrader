import os
import sys
import canvas
import tempfile
import importlib 
import logging 
import shutil 
import subprocess 

from pathlib import Path

def main() :
    if len(sys.argv) < 2 : 
        print ("usage:", sys.argv[0], "<zipfile> [username]")
        exit(-1)

    userfilter = None
    if len(sys.argv) == 3 :
        userfilter = sys.argv[2]

    test = 'tests/test_project3.py'
    workdir = canvas.extract(sys.argv[1])

    os.environ['PYTHONPATH'] = Path(__file__).resolve().parent.as_posix()

    os.makedirs('results', exist_ok=True)
    for user in workdir.iterdir() :
        if userfilter is not None and user.name != userfilter :
            continue
        print('Grading user: ' + user.name)
        shutil.copy2(test, user.as_posix())
        logdir = os.path.join(user.as_posix(), 'logs')
        logfile = os.path.join(logdir, 'grader.log')
        os.makedirs(logdir)
        with open(logfile, 'a') as log :
            subprocess.run('python test_project3.py', cwd=user.as_posix(), shell=True, check=True, stdout=log, stderr=log)
            subprocess.run('tree', cwd=user.as_posix(), shell=True, check=True, stdout=log, stderr=log)
        

        subprocess.run('zip -r ' + user.name + '.zip .', cwd=user.as_posix(), shell=True, check=True, stdout=subprocess.DEVNULL)
        shutil.copy2(os.path.join(user.as_posix(), user.name + '.zip'), 'results')

    
if __name__=="__main__":
    main()
