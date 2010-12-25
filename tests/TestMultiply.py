'''
@author: doug@neverfear.org
'''
from MatrixArithmetic import *
import unittest

class TestMultiply(unittest.TestCase):
    
    def setUp(self):
        self.A = [
                    [1,1,0,0]
                 ]
        self.mA = Matrix(self.A)
        self.B = [
                    [1,0,0,0,1,1,0],
                    [0,1,0,0,1,0,1],
                    [0,0,1,0,0,1,1],
                    [0,0,0,1,1,1,1]
                 ]
        self.mB = Matrix(self.B)
        
    def tearDown(self):
        del self.A
        del self.mA
        del self.B
        del self.mB
    
    def testMultiplyFunctionNonMutate(self):
        AB = Multiply(self.A, self.B)
        self.assertEqual([[1,0,0,0,1,1,0],[0,1,0,0,1,0,1],[0,0,1,0,0,1,1],[0,0,0,1,1,1,1]], self.B)
        self.assertEqual([[1,1,0,0]], self.A) # Check it's not mutated
        self.assertEqual([[1,1,0,0,2,1,1]], AB)
        
        mAB = Multiply(self.mA, self.B)
        self.assertEqual([[1,0,0,0,1,1,0],[0,1,0,0,1,0,1],[0,0,1,0,0,1,1],[0,0,0,1,1,1,1]], self.B)
        self.assertEqual([[1,1,0,0]], self.mA) # Check it's not mutated
        self.assertEqual([[1,1,0,0,2,1,1]], mAB)
        
        mAmB = Multiply(self.mA, self.mB)
        self.assertEqual([[1,0,0,0,1,1,0],[0,1,0,0,1,0,1],[0,0,1,0,0,1,1],[0,0,0,1,1,1,1]], self.mB)
        self.assertEqual([[1,1,0,0]], self.mA) # Check it's not mutated
        self.assertEqual([[1,1,0,0,2,1,1]], mAmB)
        
   
    def testMultiplyMethod(self):
        mAB = self.mA.multiply(self.B)
        self.assertEqual([[1,0,0,0,1,1,0],[0,1,0,0,1,0,1],[0,0,1,0,0,1,1],[0,0,0,1,1,1,1]], self.B)
        self.assertEqual([[1,1,0,0]], self.mA)
        self.assertEqual([[1,1,0,0,2,1,1]], mAB)
        
        mAmB = self.mA.multiply(self.mB)
        self.assertEqual([[1,0,0,0,1,1,0],[0,1,0,0,1,0,1],[0,0,1,0,0,1,1],[0,0,0,1,1,1,1]], self.mB)
        self.assertEqual([[1,1,0,0]], self.mA)
        self.assertEqual([[1,1,0,0,2,1,1]], mAmB)
      
    def testMultiplyOp(self):
        mAB = self.mA * self.B
        self.assertEqual([[1,0,0,0,1,1,0],[0,1,0,0,1,0,1],[0,0,1,0,0,1,1],[0,0,0,1,1,1,1]], self.B)
        self.assertEqual([[1,1,0,0]], self.mA)
        self.assertEqual([[1,1,0,0,2,1,1]], mAB)
        
        mAmB = self.mA * self.mB
        self.assertEqual([[1,0,0,0,1,1,0],[0,1,0,0,1,0,1],[0,0,1,0,0,1,1],[0,0,0,1,1,1,1]], self.mB)
        self.assertEqual([[1,1,0,0]], self.mA)
        self.assertEqual([[1,1,0,0,2,1,1]], mAmB)
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
