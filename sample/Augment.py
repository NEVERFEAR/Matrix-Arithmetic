from MatrixArithmetic import *
"""
A sample of adding a factor to all terms
"""

A = [
        [7,1],
        [2,3],
        [4,5]
    ]

B = [
        [0,1],
        [2,3],
        [4,5]
    ]

MA = Matrix(A, "MA")
MB = Matrix(B, "MB")

AB = Augment(A, B)

print ToString(AB, "AB")

assert [[7,1,0,1],[2,3,2,3],[4,5,4,5]] == AB

MAB = MA.augment(B)
MAB.name = "MAB"
print MAB
assert id(MAB) != id(MA)
assert [[7,1,0,1],[2,3,2,3],[4,5,4,5]] == MAB

MAB = MA + B
MAB.name = "MAB"
print MAB
assert id(MAB) != id(MA)
assert [[7,1,0,1],[2,3,2,3],[4,5,4,5]] == MAB

MAMB = MA + MB
MAMB.name = "MAMB"
print MAMB

assert [[7,1,0,1],[2,3,2,3],[4,5,4,5]] == MAMB

MA += MB
assert [[7,1,0,1],[2,3,2,3],[4,5,4,5]] == MAMB

C = [
    [1],
    [2]
]
try:
    MA + C
    raise Exception("Expect exception not thrown")
except IncompatibleMatrixException:
    print "Got expected exception"
