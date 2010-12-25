#!/usr/bin/python
import unittest
import os
from os import path
import sys

directory = path.dirname(sys.argv[0])
base = path.basename(sys.argv[0])

if directory == "":
    directory = "."
files = os.listdir(directory)

working = os.getcwdu()
os.chdir(directory)

TestCases = []
for f in files:
    if path.isfile(f) and f.startswith("Test") and f.endswith(".py") and f != base:
        TestCases.append(f[:-3])
        __import__(f[:-3])

os.chdir(working)

print "TestCases =", ", ".join(TestCases)

unittest.main()
