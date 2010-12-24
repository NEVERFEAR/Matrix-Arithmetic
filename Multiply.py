from MatrixArithmetic import *

A = [
        [1,1,0,0]
    ]

B = [
        [1,0,0,0,1,1,0],
        [0,1,0,0,1,0,1],
        [0,0,1,0,0,1,1],
        [0,0,0,1,1,1,1]
    ]

print ToString(A, "A")
print ToString(B, "B")

AB = Multiply(A, B)

print "list * list"
print ToString(AB, "AB")

assert AB == [[1,1,0,0,2,1,1]]

print "=" * 20

MA = Matrix(A, "MA")
MB = Matrix(B, "MB")

print "Matrix * Matrix"
MAMB = MA * MB
print MAMB
assert MAMB.name == "MAMB"

print "Matrix * list"
print MA * B

print "list * Matrix"
print  A * MB

