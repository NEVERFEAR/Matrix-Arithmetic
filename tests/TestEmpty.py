'''
@author: doug@neverfear.org
'''
from MatrixArithmetic import *
import unittest

class TestEmpty(unittest.TestCase):
    
    def testNoRows(self):
       self.assertRaises(EmptyMatrixException, Matrix, [])
       self.assertRaises(EmptyMatrixException, SquareMatrix, [])
    
    def testNoColumns(self):
       self.assertRaises(EmptyMatrixException, Matrix, [[]])
       self.assertRaises(EmptyMatrixException, SquareMatrix, [[]])
        
      
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
