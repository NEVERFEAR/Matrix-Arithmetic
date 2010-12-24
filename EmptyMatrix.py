from MatrixArithmetic import *

try:
    SquareMatrix([])
    raise Exception("Exception should have been thrown.")
except EmptyMatrixException:
    print "Exception correctly thrown"
try:
    SquareMatrix([[]])
    raise Exception("Exception should have been thrown.")
except EmptyMatrixException:
    print "Exception correctly thrown"

try:
    Matrix([])
    raise Exception("Exception should have been thrown.")
except EmptyMatrixException:
    print "Exception correctly thrown"
try:
    Matrix([[]])
    raise Exception("Exception should have been thrown.")
except EmptyMatrixException:
    print "Exception correctly thrown"

