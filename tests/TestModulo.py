'''
@author: doug@neverfear.org
'''
from MatrixArithmetic import *
import unittest

class TestModulo(unittest.TestCase):
    
    def setUp(self):
        self.A = [
                    [1,2],
                    [3,4]
                ]
        self.mA = Matrix(self.A)

    def tearDown(self):
        del self.A
        del self.mA
    
    def testModuloFunctionNonMutate(self):
        B = Modulo(self.A, 2)
        self.assertEqual([[1,0],[1,0]], B)
        self.assertEqual([[1,2],[3,4]], self.A) # Check it's not mutated
        
        mB = Modulo(self.mA, 2)
        self.assertEqual([[1,0],[1,0]], B)
        self.assertEqual([[1,2],[3,4]], self.mA) # Check it's not mutated
   
    def testModuloFunctionMutate(self):
        B = Modulo(self.A, 2, Mutate = True)
        self.assertEqual([[1,0],[1,0]], B)
        self.assertEqual([[1,0],[1,0]], self.A)
        self.assertEqual(id(self.A), id(B)) # Check it's the same instance
        
        mB = Modulo(self.mA, 2, Mutate = True)
        self.assertEqual([[1,0],[1,0]], mB)
        self.assertEqual([[1,0],[1,0]], self.mA)
        self.assertEquals(id(self.mA), id(mB))
        
    def testModuloMethod(self):
        mB = self.mA.modulo(2)
        self.assertEqual([[1,0],[1,0]], mB)
        self.assertEqual([[1,2],[3,4]], self.mA) # Check it's not mutated
    
    def testModuloOp(self):
        mB = self.mA % 2
        self.assertEqual([[1,0],[1,0]], mB)
        self.assertEqual([[1,2],[3,4]], self.mA) # Check it's not mutated
        
      
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
