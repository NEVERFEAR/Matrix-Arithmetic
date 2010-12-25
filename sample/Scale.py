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

print "=" * 20

MM = Matrix(M)

print "Scale(Matrix)"
print ToString(Scale(MM, 2))

print "Matrix.Scale()"
print MM.scale(2)

print "Matrix * Factor"
print MM * 2

MM *= 3
print "Assign Matrix * Factor"
print MM
