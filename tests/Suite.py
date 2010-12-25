#!/usr/bin/python2.7
import unittest
import os
from os import path
import sys

directory = path.dirname(path.realpath(__file__))
base = path.basename(__file__)

if directory == "":
    directory = "."
files = os.listdir(directory)

working = os.getcwdu()
os.chdir(directory)

Suite = unittest.TestSuite()

TestLoader = unittest.TestLoader()
TestCases = []
for f in files:
    if path.isfile(f) and f.startswith("Test") and f.endswith(".py") and f != base:
        name = f[:-3]
        TestCases.append(name)
        Suite.addTests(TestLoader.discover(start_dir=directory, pattern = "Test*.py"))

os.chdir(working)

print "TestCases =", ", ".join(TestCases)

Result = unittest.TestResult()

Suite.run(Result)

print Result
