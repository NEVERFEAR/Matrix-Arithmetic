from MatrixArithmetic import *
"""
Scale a matrix by a factor.
"""

M = [
        [7,1],
        [2,3],
        [4,5]
    ]

print ToString(M)
ScaledM = Scale(M, 2)
print ToString(ScaledM)
assert ScaledM == [[14,2],[4,6],[8,10]]

