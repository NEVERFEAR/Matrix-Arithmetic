from MatrixArithmetic import *

M = [
        [7,1],
        [2,3],
        [4,5]
]
MM = Matrix(M)

print ToString(M)
print ToString(Modulo(M, 2), "ModM")

print ToString(Modulo(MM, 2))
print MM.modulo(2)
print MM % 2

