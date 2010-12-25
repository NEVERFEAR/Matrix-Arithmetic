'''
@author: doug@neverfear.org
'''
from MatrixArithmetic import *
import unittest

class TestScale(unittest.TestCase):
    
    def setUp(self):
        self.A = [
                    [1,2],
                    [3,4]
                ]
        self.mA = Matrix(self.A)

    def tearDown(self):
        del self.A
        del self.mA
    
    def testScaleFunctionNonMutate(self):
        B = Scale(self.A, 2)
        self.assertEqual([[2,4],[6,8]], B)
        self.assertEqual([[1,2],[3,4]], self.A) # Check it's not mutated
        
        mB = Scale(self.mA, 2)
        self.assertEqual([[2,4],[6,8]], mB)
        self.assertEqual([[1,2],[3,4]], self.mA) # Check it's not mutated
   
    def testScaleFunctionMutate(self):
        B = Scale(self.A, 2, Mutate = True)
        self.assertEqual([[2,4],[6,8]], B)
        self.assertEqual([[2,4],[6,8]], self.A) # Check it's mutated
        self.assertEqual(id(self.A), id(B)) # Check it's the same instance
        
        mB = Scale(self.mA, 2, Mutate = True)
        self.assertEqual([[2,4],[6,8]], mB)
        self.assertEqual([[2,4],[6,8]], self.mA) # Check it's mutated
        self.assertEquals(id(self.mA), id(mB))
        
    def testScaleMethod(self):
        mB = self.mA.scale(2)
        self.assertEqual([[2,4],[6,8]], mB)
        self.assertEqual([[1,2],[3,4]], self.mA) # Check it's not mutated
    
    def testScaleOpFloat(self):
        mB = self.mA * 2.0
        self.assertEqual([[2,4],[6,8]], mB)
        self.assertEqual([[1,2],[3,4]], self.mA) # Check it's not mutated
    
    def testScaleOpInt(self):
        mB = self.mA * 2
        self.assertEqual([[2,4],[6,8]], mB)
        self.assertEqual([[1,2],[3,4]], self.mA) # Check it's not mutated
      
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
