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

    test = 'tests/project1.py'
    workdir = canvas.extract(sys.argv[1])

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    os.environ['PYTHONPATH'] = Path(__file__).resolve().parent.as_posix() 
    for user in workdir.iterdir() :
        logger.info('Grading user: ' + user.name)
        shutil.copy2(test, user.as_posix())
        subprocess.run('python project1.py', cwd=user.as_posix(), shell=True, check=True)

    
if __name__=="__main__":
    main()
