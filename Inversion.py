from MatrixArithmetic import *
"""
Invert a matrix.
"""

M = [
    [ 2.0,-1.0, 0.0],
    [-1.0, 2.0,-1.0],
    [ 0.0,-1.0, 2.0]
]

Expected = [
    [0.75, 0.50, 0.25],
    [0.50, 1.00, 0.50],
    [0.25, 0.50, 0.75]
]

print ToString(M)

I = Invert(M)
print ToString(I, "I")



