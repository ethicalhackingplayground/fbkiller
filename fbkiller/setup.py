#!/usr/bin/python

import os
import sys

try:
    if sys.version_info[0] < 3:
        raise Exception("REQUIRED PYTHON 3.x")
except Exception:
    print('REQUIRED PYTHON 3.x')
    print('Example: python3 setup.py')
    sys.exit(1)

os.system('chmod +x fbkiller.py')
os.system('pip3 install -r requirements.txt')
os.system('apt-get install tor')
os.system('sudo apt-get install privoxy')
if (os.path.isdir("passwords") == False):
    os.system("mkdir passwords")

if (os.path.isdir("sessions") == False):
    os.system("mkdir sessions")
print ("\n\n Done...")
