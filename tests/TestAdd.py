'''
@author: doug@neverfear.org
'''
from MatrixArithmetic import *
import unittest

class TestAdd(unittest.TestCase):
    
    def setUp(self):
        self.A = [
                    [1,2],
                    [3,4]
                ]
        self.mA = Matrix(self.A)

    def tearDown(self):
        del self.A
        del self.mA
    
    def testAddFunctionNonMutate(self):
        B = Add(self.A, 2)
        self.assertEqual([[3,4],[5,6]], B)
        self.assertEqual([[1,2],[3,4]], self.A) # Check it's not mutated
        
        mB = Add(self.mA, 2)
        self.assertEqual([[3,4],[5,6]], mB)
        self.assertEqual([[1,2],[3,4]], self.mA) # Check it's not mutated
   
    def testAddFunctionMutate(self):
        B = Add(self.A, 2, Mutate = True)
        self.assertEqual([[3,4],[5,6]], B)
        self.assertEqual([[3,4],[5,6]], self.A) # Check it's mutated
        self.assertEqual(id(self.A), id(B)) # Check it's the same instance
        
        mB = Add(self.mA, 2, Mutate = True)
        self.assertEqual([[3,4],[5,6]], mB)
        self.assertEqual([[3,4],[5,6]], self.mA) # Check it's mutated
        self.assertEquals(id(self.mA), id(mB))
        
    def testAddMethod(self):
        mB = self.mA.add(2)
        self.assertEqual([[3,4],[5,6]], mB)
        self.assertEqual([[1,2],[3,4]], self.mA) # Check it's not mutated
      
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
