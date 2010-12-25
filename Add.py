from MatrixArithmetic import *
"""
A sample of adding a factor to all terms
"""

M = [
        [7,1],
        [2,3],
        [4,5]
    ]

MM = Matrix(M)

A = Add(M, 2)

print ToString(A, "A")

assert [[9,3],[4,5],[6,7]] == A

MA = Add(MM, 3)

assert [[10,4],[5,6],[7,8]] == MA

MA = MM.add(3)

assert [[10,4],[5,6],[7,8]] == MA
