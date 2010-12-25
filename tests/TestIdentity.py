'''
@author: doug@neverfear.org
'''
from MatrixArithmetic import *
import unittest

class TestIdentity(unittest.TestCase):
    
    def setUp(self):
        self.A = [
                    [1,2],
                    [3,4]
                ]
        self.mA = Matrix(self.A)
        
        self.B = [
                    [0,1],
                    [2,3],
                    [4,5]
                ]
        self.mB = Matrix(self.B)

    def tearDown(self):
        del self.A
        del self.B
        del self.mA
        del self.mB
    
    def testIdentityFunction(self):
        I = Identity(self.A)
        self.assertEquals(I, [[1,0],[0,1]])
        self.assertEquals(self.A, [[1,2],[3,4]])
        
        mI = Identity(self.mA)
        self.assertEquals(mI, [[1,0],[0,1]])
        self.assertEquals(self.mA, [[1,2],[3,4]])
    
    def testIdentityMethod(self):
        I = self.mA.identity()
        self.assertEquals(I, [[1,0],[0,1]])
        self.assertEquals(self.mA, [[1,2],[3,4]])
    
    def testNonSquare(self):
        self.assertRaises(NonSquareMatrixException, Identity, self.B)
        self.assertRaises(NonSquareMatrixException, Identity, self.mB)
      
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
