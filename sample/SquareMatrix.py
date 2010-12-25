from MatrixArithmetic import *

# This is not a square and should throw an exception
try:
    MM = SquareMatrix([[1,2]])
    raise Exception("This should have thrown an exception")
except NonSquareMatrixException:
    print "Exception was correctly thrown"

MM = SquareMatrix([[1]])

MM = SquareMatrix([[1,2,3],[4,5,6],[7,8,9]])

try:
    MM = SquareMatrix([[1],[2]])
    raise Exception("This should have thrown an exception")
except NonSquareMatrixException:
    print "Exception was correctly thrown"
