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

print ToString(AB, "AB")

assert AB == [[1,1,0,0,2,1,1]]

