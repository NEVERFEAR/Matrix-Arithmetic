from MatrixArithmetic import *
"""
An example of the Identity function
"""

M = [
        [ 1, 2,  4],
        [ 1, 3,  9],
        [ 1, 7, 49]
]

print ToString(M)
print ToString(Identity(M), Name = "I")

try:
     print ToString(Identity([[1,2]]), Name = "I")
     raise Exception("An error was expected")
except NonSquareMatrixException:
     print "Non-Square matrix has been properly rejected"

