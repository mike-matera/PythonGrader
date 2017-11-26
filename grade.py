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
    if len(sys.argv) < 3 : 
        print ("usage:", sys.argv[0], "<test> <zipfile> [username]")
        exit(-1)

    userfilter = None
    if len(sys.argv) == 4 :
        userfilter = sys.argv[3]

    test = sys.argv[1]
    workdir = canvas.extract(sys.argv[2])

    os.environ['PYTHONPATH'] = Path(__file__).resolve().parent.as_posix()
    debug = 'GRADER_DEBUG' in os.environ
    
    os.makedirs('results', exist_ok=True)
    for user in workdir.iterdir() :
        if userfilter is not None and user.name != userfilter :
            continue
        print('Grading user: ' + user.name)
        logdir = os.path.join(user.as_posix(), 'logs')
        testdir = os.path.join(user.as_posix(), 'tests')
        logfile = os.path.join(logdir, 'grader.log')
        os.makedirs(logdir)
        shutil.copytree('./tests', testdir)
        with open(logfile, 'a') as log :
            if debug :
                logfile = sys.stdout
            else:
                logfile = log
                
            subprocess.run('python ' + test, cwd=user.as_posix(), shell=True, check=True, stdout=logfile, stderr=logfile)
            shutil.rmtree(testdir)
            try:
                os.remove(os.path.join(user.as_posix(), 'geckodriver.log'))
            except:
                pass 
            subprocess.run('tree', cwd=user.as_posix(), shell=True, check=True, stdout=logfile, stderr=logfile)
        subprocess.run('zip -r ' + user.name + '.zip .', cwd=user.as_posix(), shell=True, check=True, stdout=subprocess.DEVNULL)
        shutil.copy2(os.path.join(user.as_posix(), user.name + '.zip'), 'results')


if __name__=="__main__":
    main()
