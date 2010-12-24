import math
import types

class MalformedMatrix(Exception):
    def __init__(self, msg, position):
        Exception.__init__(self, "Position %d: %s" % (position, msg))
        self.position = position

class NonSquareMatrixException(Exception):
    pass

def is_numeric(x):
    from types import ComplexType, FloatType, IntType, LongType
    return type(x) in [ComplexType, FloatType, IntType, LongType]


class MatrixRow(object):
    
    def __init__(*args, **kwds):
        self._columns = list(*args, **kwds)
    
    _delegate = [
        "__add__", "__contains__", "__delitem__", "__getslice__", "__eq__", "__ge__",
        "__getitem__", "__getslice__", "__gt__", "__iadd__", "__iter__", "__le__",
        "__len__", "__lt__", "__ne__", "__reversed__", "__setitem__", "__getslice__",
        "__str__", "__repr__", # TODO: Should we print out a row as a list? Let's do this for now..
        "append", "count", "extend", "index", "insert", "pop", "remove", "reverse", "sort"
    ]
    
    for _f in _delegate:
        _py = ( "def %s(self, *args, **kwds):\n" +
                "    return self._columns.%s(*args, **kwds)\n") % (_f, _f)
        exec _py
    
    # ============================
    # Custom methods
    # ============================
    def __imul__(self, y):
        pass # TODO: Multiply this row. With a column? Scale it? Dunno yet
    
    def __mul__(self, y):
        pass # TODO: Multiply this row with a column? scale it? decide
    
    def __rmul__(self, y):
        pass # TODO: Multiply with reversed operands

class Matrix(object):
    def __init__(self, matrix, name = "M"):
        self._rows = Copy(matrix)
        self.name = name
    
    def Validate(self):
        """Validate that to matrix is well formed"""
        ColCount = None
        for Row in self._rows:
            if ColCount is None:
                ColCount = len(Row)
            elif ColCount != len(Row):
                raise MalformedMatrix("Matrix has mixed column sizes")
        if ColCount is None:
            raise MalformedMatrix("Matrix must have at least one row and column")
    
    _delegate = [
        "__add__", "__contains__", "__delitem__", "__getslice__", "__eq__", "__ge__",
        "__getitem__", "__getslice__", "__gt__", "__iadd__", "__iter__", "__le__",
        "__len__", "__lt__", "__ne__", "__reversed__", "__setitem__", "__getslice__",
        "append", "count", "extend", "index", "insert", "pop", "remove", "reverse", "sort"
    ]
    
    for _f in _delegate:
        _py = ( "def %s(self, *args, **kwds):\n" +
                "    return self._rows.%s(*args, **kwds)\n") % (_f, _f)
        exec _py
    
    def scale(self, factor):
        return Matrix(Scale(self._rows, factor, Mutate = False))
    
    def multiply(self, matrix):
        kwds = {}
        if hasattr(matrix, "name"):
            kwds["name"] = self.name + matrix.name
        return Matrix(Multiply(self._rows, matrix), **kwds)
    
    # ============================
    # Custom methods
    # ============================
    
    # NOTE: The multiplication function should work as follows
    """
    - If factor is a numeric type then scale
    - If factor is a list or matrix type then perform a matrix multiplication
    """
    
    def __imul__(self, y):
        if is_numeric(y):
            self._rows = Scale(self._rows, y, Mutate = True)
        elif is_matrix_type(y):
            self._rows = Multiply(self._rows, y)
        return self
    
    def __mul__(self, y):
        if is_numeric(y):
            return self.scale(y)
        elif is_matrix_type(y):
            kwds = {}
            if hasattr(y, "name"):
                kwds["name"] = self.name + y.name
            return Matrix(Multiply(self._rows, y), **kwds)
    
    def __rmul__(self, y):
        if is_numeric(y):
            return self.scale(y)
        elif is_matrix_type(y):
            kwds = {}
            if hasattr(y, "name"):
                kwds["name"] = y.name + self.name
            return Matrix(Multiply(y, self._rows), **kwds)

    def __str__(self):
        return ToString(self._rows, self.name)
    
    __repr__ = __str__



def is_matrix_type(x):
    from types import ListType
    return type(x) in [ListType, Matrix]

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
                Row[ColIndex] = F(Col, ColIndex, RowIndex)
            else:
                ResultRow.append(F(Col, ColIndex, RowIndex))
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
    ValidateSquare(Matrix)
    F = lambda v, x, y: 1 if x == y else 0
    return ApplyFunc(Matrix, F, Mutate = False)

def ValidateSquare(Matrix):
    RowCount = len(Matrix)
    for Row in Matrix:
        if RowCount != len(Row):
            raise NonSquareMatrixException("Must be square")

def Copy(Matrix):
    F = lambda v, x, y: v
    return ApplyFunc(Matrix, F, Mutate = False)

def ToString(Matrix, Name = "M"):
    t = ""
    Y = math.ceil(float(len(Matrix)) / 2)
    i = 1;
    RowLength = 0
    WholeLongest = 0
    FractionLongest = 0
    NegationSize = 0
    NameLength = len(Name)
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
            s = s + "%s = " % Name
        else:
            s = s + "%s   " % (" " * NameLength)
        
        s = s + "|"
        for Col in Row:
            s = s + (FormatPat % Col)
        s = s + " |"
        t = t + s + "\n"
        
        i = i + 1
    b = (" " * NameLength) + "   +-" + ((RowLength - 1) * " ") + "-+\n"
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
        Lead += 1
    return Matrix

def MatrixRowSwap(Matrix, RowIndex, WithIndex, Mutate = False):
    Matrix = Matrix if Mutate else Copy(Matrix)
    if RowIndex != WithIndex:
        Row = Matrix[RowIndex]
        Matrix[RowIndex] = Matrix[WithIndex]
        Matrix[WithIndex] = Row
    return Matrix

def MatrixRowMultiplication(Matrix, RowIndex, Factor, Mutate = False):
    Matrix = Matrix if Mutate else Copy(Matrix)
    Row = Matrix[RowIndex]
    for ColIndex, Col in enumerate(Row):
        Row[ColIndex] = Col * Factor
    return Matrix

def MatrixRowAddition(Matrix, ToIndex, RowIndex, Factor, Mutate = False):
    Matrix = Matrix if Mutate else Copy(Matrix)
    Row = Matrix[RowIndex]
    ToRow = Matrix[ToIndex]
    for ColIndex, Col in enumerate(Row):
        ToRow[ColIndex] += Col * Factor
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



