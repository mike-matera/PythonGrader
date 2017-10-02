import sys 
import os
import re 
import zipfile
import os
import io
import tempfile 
import atexit
import subprocess
import shutil
import logging
import unittest 

from pathlib import Path

def cleanup() :
    global __canvas_tempdir
    if __canvas_tempdir is not None :
        __canvas_tempdir.cleanup()
        
def extract(zipname) :
    global __canvas_tempdir
    __canvas_tempdir = tempfile.TemporaryDirectory(prefix='pygr-')
    atexit.register(cleanup)

    canvas_temp_dir = os.path.join(__canvas_tempdir.name, 'canvas_tmp')
    user_temp_dir = os.path.join(__canvas_tempdir.name, 'users')
    zip_abspath = os.path.abspath(zipname)
    
    os.makedirs(canvas_temp_dir)

    subprocess.run("unzip " + str(zip_abspath), cwd=canvas_temp_dir, shell=True, check=True, stdout=subprocess.DEVNULL)

    unzip_path = Path(canvas_temp_dir)
    for f in unzip_path.iterdir() :
        parts = f.name.split('_')
        user = parts.pop(0)

        late = False
        if parts[0] == 'late' :
            late = True
            parts.pop(0)

        while re.match('\d+', parts[0]) is not None :
            parts.pop(0)

        filename = '_'.join(parts)        
        filename = os.path.basename(filename)

        # Fix numering hassle.         
        while re.search('-(\d+)\.\w+$', filename) is not None : 
            filename = re.sub('-\d+\.', '.', filename)

        userdir = os.path.join(user_temp_dir, user)
        os.makedirs(userdir, exist_ok=True)

        shutil.copy2(f.as_posix(), os.path.join(userdir, filename))
        if Path(filename).suffix == '.zip' : 
            subprocess.run('unzip "' + filename + '"', cwd=userdir, shell=True, check=True, stdout=subprocess.DEVNULL)
            os.unlink(os.path.join(userdir, filename))

        elif Path(filename).suffix == '.gz' :
            subprocess.run('tar -xvf "' + filename + '"', cwd=userdir, shell=True, check=True, stdout=subprocess.DEVNULL)
            os.unlink(os.path.join(userdir, filename))

        elif Path(filename).suffix == '.7z' :
            subprocess.run('7zr x "' + filename + '"', cwd=userdir, shell=True, check=True, stdout=subprocess.DEVNULL)
            os.unlink(os.path.join(userdir, filename))

        if late : 
            subprocess.run('touch ' + os.path.join(userdir, '__late__'), shell=True)

    return Path(user_temp_dir)
