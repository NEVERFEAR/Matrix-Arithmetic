import math
import types

class MalformedMatrix(Exception):
    def __init__(self, msg, position):
        Exception.__init__(self, "Position %d: %s" % (position, msg))
        self.position = position


def BuildMatrixLists(s):
    """Builds a 2D array suitable for a matrix from a string."""
    result = []
    value = ""
    depth = 0
    invalue = False
    current = None
    width = 0 # Wont know this until after the first row
    
    for (pos, c) in enumerate(list(s)):
        if c == '[':
            depth += 1
            if depth > 2:
                raise MalformedMatrix("A Matrix cannot have any more than 2 dimensions.", pos)
            if current is None:
                current = result
            else:
                current = list()
                result.append(current)
                
            invalue = True
        elif c in list("0123456789.-"):
            if not invalue:
                raise MalformedMatrix("Numerical value unexpected at this time.", pos)
            elif c == '.' and value.find('.') != -1:
                raise MalformedMatrix("Malformed floating point literal.", pos)
            elif c == '-' and len(value) > 0:
                raise MalformedMatrix("Negative symbol must appear at the beginning of a numerical value.", pos)
            value += c
        elif c == ',' or c == ']':
            if depth > 1: # We've just came from a value
                if len(value) == 0:
                    raise MalformedMatrix("Empty value.", pos)
                if value.find('.') != -1:
                    current.append(float(value))
                else:
                    current.append(int(value))
            value = ""
            if c == ',':
                invalue = depth > 1 # A new value may be the next token but only if we're in the second dimension
            else: # ]
                if depth > 0:
                    if len(result) == 1: # If this is the first row
                        width = len(current)
                    elif len(current) != width:
                        raise MalformedMatrix("Row widths are inconsistent.", pos)
                invalue = False # Since the only time we have these we expect to start another
                depth -= 1
                if depth < 0:
                    raise MalformedMatrix("Invalid Syntax.", pos)
                
        elif c in [' ', '\t', '\n', '\r']:
            invalue = len(value) == 0 and depth > 1 # We no longer expect to start a new value as the
                                      # next token if we've already started one
        else:
            raise MalformedMatrix("Unexpected character '%s'." % (c), pos)
    if depth > 0:
        raise MalformedMatrix("Matrix improperly ended.", pos)
    return result
    
def Multiply(A, B):
    RowCntA = len(A)
    ColCntA = len(A[0])
    RowCntB = len(B)
    ColCntB = len(B[0])
    
    Result = []
    i = 0
    while i < RowCntA:
        ResultRow = []
        j = 0
        while j < ColCntB:
            total, r = 0, 0
            while r < ColCntA: # or RowCntB
                total = total + (A[i][r] * B[r][j])
                r = r + 1
            ResultRow.append(total)
            j = j + 1
        Result.append(ResultRow)
        i = i + 1
    return Result

def ApplyFunc(Matrix, F, Mutate = False):
    Result = [] if not Mutate else Matrix
    for RowIndex, Row in enumerate(Matrix):
        if not Mutate:
            ResultRow = []
        for ColIndex, Col in enumerate(Row):
            if Mutate:
                Row[ColIndex] = F(Col)
            else:
                ResultRow.append(F(Col))
        if not Mutate:
            Result.append(ResultRow)
    return Result

def Modulo(Matrix, Mod, Mutate = False):
    F = lambda v, x, y: v % Mod
    return ApplyFunc(Matrix, F, Mutate)

def Scale(Matrix, Factor, Mutate = False):
    F = lambda v, x, y: v * Factor
    return ApplyFunc(Matrix, F, Mutate)

def Add(Matrix, Factor, Mutate = False):
    F = lambda v, x, y: v + Factor
    return ApplyFunc(Matrix, F, Mutate)

def Negate(Matrix, Mutate = False):
    F = lambda v, x, y: -v
    return ApplyFunc(Matrix, F, Mutate)

def Identity(Matrix):
    F = lambda v, x, y: 1 if x == y else 0
    return ApplyFunc(Matrix, F, Mutate = False)

def Copy(Matrix):
    F = lambda v, x, y: v
    return ApplyFunc(Matrix, F, Mutate = False)

def ToString(Matrix):
    t = ""
    Y = math.ceil(float(len(Matrix)) / 2)
    i = 1;
    RowLength = 0
    WholeLongest = 0
    FractionLongest = 0
    NegationSize = 0
    for Row in Matrix:
        ColCnt = 0
        for Col in Row:

            if type(Col) in [types.FloatType]:
                whole, fraction = str(Col).split(".", 2)
                n = len(whole)
                f = 0 if fraction == "0" else len(fraction)
            else:
                n = len(str(Col))
                f = 0
            if Col < 0.0:
                NegationSize = 1
            
            if n > WholeLongest:
                WholeLongest = n
            
            if f > FractionLongest:
                FractionLongest = f
            ColCnt = ColCnt + 1
    
    FloatPointSize = 1 if FractionLongest else 0
    
    RowLength = (ColCnt * (WholeLongest + 1 + FractionLongest + FloatPointSize))
   
    if FractionLongest:
        FormatPat = "%% %d.%df" % ( WholeLongest + 2 + NegationSize + FloatPointSize,
                                    FractionLongest)
    else:
        FormatPat = "%% %dd" % (WholeLongest + 1)
    
    for Row in Matrix:
        s = ""
        if i == Y:
            s = s + "M = "
        else:
            s = s + "    "
        
        s = s + "|"
        for Col in Row:
            s = s + (FormatPat % Col)
        s = s + " |"
        t = t + s + "\n"
        
        i = i + 1
    b = "    +-" + ((RowLength - 1) * " ") + "-+\n"
    return b + t + b

def AugmentIdentity(Matrix):
    RowCount = len(Matrix)
    AugmentedMatrix = []
    for Index, Row in enumerate(Matrix):
        if len(Row) != RowCount:
            raise MalformedMatrix("Matrix must be square")
        # Augment the matrix with the identity matrix row
        AugmentedRow = Row + map(lambda i : 1 if i == Index else 0, xrange(RowCount))
        AugmentedMatrix.append(AugmentedRow)
    return AugmentedMatrix

def ReduceToRowEchelonForm(Matrix, Mutate = False):
    Matrix = Matrix if Mutate else Copy(Matrix)
    
    Lead = 0
    RowCount = len(Matrix)
    for RowIndex in xrange(RowCount):
        print "Processing row", RowIndex
        ColumnCount = len(Matrix[RowIndex])
        if ColumnCount <= Lead:
            return # TODO: What does this mean?
        j = RowIndex
        
        # Find the first row who's lead is nonzero
        while Matrix[j][Lead] == 0:
            j += 1
            if RowCount == j:
                # If no row was found but there are zeros
                # In all the columns `Lead` then use our current row
                # and look towards the next lead column
                j = RowIndex
                Lead += 1
                if ColumnCount == Lead:
                    return # TODO: What does this mean?
        
        print "The lead is column", Lead, "and has value", Matrix[RowIndex][Lead]
        # This is the swap operation
        MatrixRowSwap(Matrix, RowIndex, j, True)
        # This is the row multiplication operation
        # Take the lead of the current row and use it as a divisor factor
        MatrixRowMultiplication(Matrix, RowIndex, 1.0 / Matrix[RowIndex][Lead], True)
        # Look at every row that isn't the current row and take the lead of the each row
        # as a factor and multiply subtract each row
        # This is the "row-addition" operation
        for j in xrange(RowCount):
            if j != RowIndex:
                # Multiply RowIndex Row by Factor then subtract from Row{j}
                MatrixRowAddition(Matrix, j, RowIndex, -Matrix[j][Lead], True)
        print "After handling row", RowIndex
        print ToString(Matrix)
        Lead += 1
    return Matrix

def MatrixRowSwap(Matrix, RowIndex, WithIndex, Mutate = False):
    Matrix = Matrix if Mutate else Copy(Matrix)
    if RowIndex != WithIndex:
        print "Swaping", RowIndex, "with", WithIndex
        Row = Matrix[RowIndex]
        Matrix[RowIndex] = Matrix[WithIndex]
        Matrix[WithIndex] = Row
    return Matrix

def MatrixRowMultiplication(Matrix, RowIndex, Factor, Mutate = False):
    Matrix = Matrix if Mutate else Copy(Matrix)
    Row = Matrix[RowIndex]
    print "Multiply", Factor, "by", Row, "->",
    for ColIndex, Col in enumerate(Row):
        Row[ColIndex] = Col * Factor
    print Row
    return Matrix

def MatrixRowAddition(Matrix, ToIndex, RowIndex, Factor, Mutate = False):
    Matrix = Matrix if Mutate else Copy(Matrix)
    Row = Matrix[RowIndex]
    ToRow = Matrix[ToIndex]
    print "Adding", Row, "*", Factor, "to", ToRow, "->",
    for ColIndex, Col in enumerate(Row):
        ToRow[ColIndex] += Col * Factor
    print ToRow
    return Matrix

def GaussJordanElimination(Matrix):
    RowCount = len(Matrix)
    AugmentedMatrix = AugmentIdentity(Matrix)
    ReducedMatrix = ReduceToRowEchelonForm(AugmentedMatrix, Mutate = False)
    InvertedMatrix = []
    # Peal off the augmented matrix to leave the inverted matrix
    for Row in ReducedMatrix:
        InvertedMatrix.append(Row[RowCount:])
    return InvertedMatrix
Invert = GaussJordanElimination
    

if __name__ == "__main__":
    """
    print ToString(
        Multiply(
            [
                [1,1,0,0]
            ],
            # That multiplied by
            [
                [1,0,0,0,1,1,0],
                [0,1,0,0,1,0,1],
                [0,0,1,0,0,1,1],
                [0,0,0,1,1,1,1]
            ]
        )
    )
    
    print "=" * 20
    print "Multiply"
    print ToString(
        Multiply(
            [
                [1,2,3],
                [4,5,6]
            ],
            # That multiplied by
            [
                [7,1],
                [2,3],
                [4,5]
            ]
        )
    )
    
    print "=" * 20
    print "Modulo"
    print ToString(
        Modulo(
            [
                [7,1],
                [2,3],
                [4,5]
            ],
            
            2
        )
    )
    
    print "=" * 20
    # Let us check that the mutation works properly
    M = [
        [7,1],
        [2,3],
        [4,5]
    ]
    M_ID = id(M)
    ScaledM = Scale(M, 2, True)
    ScaledM_ID = id(ScaledM)
    assert M_ID == ScaledM_ID
    """
    print "=" * 20
    # We expect a result of
    # [
    #   [0.75, 0.50, 0.25],
    #   [0.50, 1.00, 0.50],
    #   [0.25, 0.50, 0.75]
    # ]
    M = [
        [ 2.0,-1.0, 0.0],
        [-1.0, 2.0,-1.0],
        [ 0.0,-1.0, 2.0]
    ]
    M = [
        [1, 2, 4],
        [1, 3, 9],
        [1, 7, 49]
    ]
    print "Before Inversion"
    print ToString(M)
    print "Inverted"
    print ToString(
        GaussJordanElimination(M)
    ) 

    print "=" * 20
    print "Shamirs Shared Secret"
    print "=" * 20
    Prime = 1234567890133
    MatrixA = [
        [  1,  2,  4],
        [  1,  3,  9],
        [  1,  7, 49]
    ]
    
    Inverted = GaussJordanElimination(MatrixA)
    
    print "Inverted Matrix:"
    print ToString(
        Inverted
    )
    MatrixS = [
        [1045116192326],
        [ 154400023692],
        [ 973441680328]
    ]
    #MatrixM = Multiply(MatrixS, Inverted)
    MatrixM = Multiply(Inverted, MatrixS)
    print ToString(MatrixM)
    print "Message Matrix:"
    print ToString(
        Modulo(MatrixM, Prime)
    )



