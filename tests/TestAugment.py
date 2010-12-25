'''
@author: doug@neverfear.org
'''
from MatrixArithmetic import *
import unittest

class TestAugment(unittest.TestCase):
    
    def setUp(self):
        self.A = [
                    [1,2],
                    [3,4]
                ]
        self.B = [
                    [5,6],
                    [7,8]
                ]
        self.C = [
                    [9,0]
                ]
        self.mA = Matrix(self.A, "mA")
        self.mB = Matrix(self.B, "mB")
        self.mC = Matrix(self.C, "mC")

    def tearDown(self):
        del self.A
        del self.B
        del self.C
        del self.mA
        del self.mB
        del self.mC
    
    def testAugmentFunctionNonMutate(self):
        aAB = Augment(self.A, self.B)
        self.assertEqual([[1,2],[3,4]], self.A)
        self.assertEqual([[5,6],[7,8]], self.B)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], aAB)
        
        amAB = Augment(self.mA, self.B)
        self.assertEqual([[1,2],[3,4]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.B)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], amAB)
        
        aAmB = Augment(self.A, self.mB)
        self.assertEqual([[1,2],[3,4]], self.A)
        self.assertEqual([[5,6],[7,8]], self.mB)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], aAmB)
        
        amAmB = Augment(self.mA, self.mB)
        self.assertEqual([[1,2],[3,4]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.mB)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], amAmB)
        
        
   
    def testAugmentFunctionMutateList(self):
        aAB = Augment(self.A, self.B, Mutate = True)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], self.A)
        self.assertEqual([[5,6],[7,8]], self.B)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], aAB)
        
        amAB = Augment(self.mA, self.B, Mutate = True)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.B)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], amAB)
        
    def testAugmentFunctionMutateMatrix(self):
        aAmB = Augment(self.A, self.mB, Mutate = True)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], self.A)
        self.assertEqual([[5,6],[7,8]], self.mB)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], aAmB)
        
        amAmB = Augment(self.mA, self.mB, Mutate = True)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.mB)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], amAmB)
        
    def testAugmentMethod(self):
        amAB = self.mA.augment(self.B)
        self.assertEqual([[1,2],[3,4]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.B)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], amAB)
        
        amAmB = self.mA.augment(self.mB)
        self.assertEqual([[1,2],[3,4]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.mB)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], amAmB)
        
    def testAugmentByAddOp(self):
        amAB = self.mA + self.B
        self.assertEqual([[1,2],[3,4]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.B)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], amAB)
        
        amAmB = self.mA + self.mB
        self.assertEqual([[1,2],[3,4]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.mB)
        self.assertEqual([[1,2,5,6],[3,4,7,8]], amAmB)
    
    def testAugmentByIAddOpList(self):
        self.mA += self.B
        self.assertEqual([[1,2,5,6],[3,4,7,8]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.B)
        
    def testAugmentByIAddOpMatrix(self):
        self.mA += self.mB
        self.assertEqual([[1,2,5,6],[3,4,7,8]], self.mA)
        self.assertEqual([[5,6],[7,8]], self.mB)
    
        
        
        
      
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
