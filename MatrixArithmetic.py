'''Matrix Arithmetic utility module.

Author: doug@neverfear.org

This module provides matrix utility functions and objects to support matrix arithmetic.
This module has not been performance tuned for any specific use-case. In many ways
please think of this module as a simple set of utility routines not a serious attempt
at a matrix processing software development library.

'''

import math
import types

class MalformedMatrixException(Exception):
    '''A Matrix instance is not in a structurally sound form.'''
    pass

class MatrixParseException(Exception):
    '''A string representation of a matrix is malformed.'''
    def __init__(self, msg, position):
        Exception.__init__(self, "Position %d: %s" % (position, msg))
        self.position = position

class NonSquareMatrixException(MalformedMatrixException):
    '''A Matrix does not have an equal number of rows and columns.'''
    pass

class EmptyMatrixException(MalformedMatrixException):
    '''A Matrix has no rows or columns.'''
    pass

class IrregularRowException(MalformedMatrixException):
    '''There is a difference in the number of columns in each row.'''
    pass

class IncompatibleMatrixException(Exception):
    '''A Matrix is incompatible with an operation.'''
    pass

def is_numeric(x):
    from types import ComplexType, FloatType, IntType, LongType
    return type(x) in [ComplexType, FloatType, IntType, LongType]


class MatrixRow(object):
    '''Represents a row within a matrix.'''

    def __init__(*args, **kwds):
        self._columns = list(*args, **kwds)
    
    _delegate = [
        "__add__", "__contains__", "__delitem__", "__getslice__", "__eq__", "__ge__",
        "__getitem__", "__getslice__", "__gt__", "__iadd__", "__iter__", "__le__",
        "__len__", "__lt__", "__ne__", "__reversed__", "__setitem__", "__getslice__",
        "__str__", "__repr__", # TODO: Should we print out a row as a list? Let's do this for now..
        "append", "count", "extend", "index", "insert", "pop", "remove", "reverse",
        "sort", "__imul__", "__mul__", "__rmul__"
    ]
    
    for _f in _delegate:
        _py = ( "def %s(self, *args, **kwds):\n" +
                "    return self._columns.%s(*args, **kwds)\n") % (_f, _f)
        exec _py

class Matrix(object):
    '''Represents a matrix which is a collection of rows with a name.'''

    def __init__(self, matrix, name = "M"):
        self._rows = Copy(matrix)
        self.name = name
        self.Validate()
    
    def Validate(self):
        '''Validate that to matrix is well formed'''
        ColCount = None
        for Row in self._rows:
            if ColCount is None:
                ColCount = len(Row)
            elif ColCount != len(Row):
                raise MatrixParseException("Matrix has mixed column sizes")
        if ColCount is None or ColCount == 0:
            raise EmptyMatrixException("Matrix must have at least one row and one column")
    
    _delegate = [
        "__contains__", "__delitem__", "__getslice__", "__eq__", "__ge__",
        "__getitem__", "__getslice__", "__gt__", "__iter__", "__le__",
        "__len__", "__lt__", "__ne__", "__reversed__", "__setitem__", "__getslice__",
        "append", "count", "extend", "index", "insert", "pop", "remove", "reverse", "sort"
    ]
    
    for _f in _delegate:
        _py = ( "def %s(self, *args, **kwds):\n" +
                "    return self._rows.%s(*args, **kwds)\n") % (_f, _f)
        exec _py
    
    def scale(self, factor):
        '''Return a Matrix object that is a scaled copy of this matrix.'''
        return Matrix(Scale(self._rows, factor, Mutate = False))
    
    def multiply(self, matrix):
        '''Return a Matrix object that is the result of multiplying this matrix by another.'''
        kwds = {}
        if hasattr(matrix, "name"):
            kwds["name"] = self.name + matrix.name
        return Matrix(Multiply(self._rows, matrix), **kwds)
    
    def identity(self):
        '''Return a Matrix object that is the identity matrix for this matrix.'''
        return Matrix(Identity(self._rows))
    
    def modulo(self, factor):
        '''Return a Matrix object that is the result of this matrix modulo a factor.'''
        return Matrix(Modulo(self._rows, factor))
    
    def add(self, factor):
        '''Return a Matrix object that is the result of adding a factor to every term of this matrix.'''
        return Matrix(Add(self._rows, factor))
    
    def augment(self, matrix):
        '''Return a Matrix object that is the result of augmenting this matrix with another.'''
        return Matrix(Augment(self._rows, matrix))
    
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

    def __mod__(self, factor):
        '''Modulo this entire matrix by a factor.'''
        return self.modulo(factor)

    def __add__(self, matrix):
        '''Augment this matrix with another returning a new instance.'''
        return self.augment(matrix)
       
    def __iadd__(self, matrix):
        '''Augment this matrix with another.'''
        Augment(self._rows, matrix, Mutate = True)
        return self
    
    def __str__(self):
        return ToString(self._rows, self.name)
    
    def __repr__(self):
        return repr(self._rows)


class SquareMatrix(Matrix):
    '''Represents a square matrix where the number of columns and rows are equal.'''

    def Validate(self):
        '''Validate matrix is square.'''
        RowCount = len(self._rows)
        if RowCount == 0:
            raise EmptyMatrixException("Matrix must have at least one row and one column")
        for Row in self._rows:
            ColCount = len(Row)
            if ColCount == 0:
                raise EmptyMatrixException("Matrix must have at least one row and one column")
            if RowCount != ColCount:
                raise NonSquareMatrixException("Matrix has %d rows and at least one row does not have an equal number of columns" % RowCount)
    
    def invert(self):
        '''Apply Gauss-Jordon elimination to he matrix to create an instance of a matrix representing the inverse of this matrix.'''
        return Matrix(Invert(self._rows))
    

def is_matrix_type(x):
    from types import ListType
    return type(x) in [ListType, Matrix]

def ParseMatrix(s):
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
                raise MatrixParseException("A Matrix cannot have any more than 2 dimensions.", pos)
            if current is None:
                current = result
            else:
                current = list()
                result.append(current)
                
            invalue = True
        elif c in list("0123456789.-"):
            if not invalue:
                raise MatrixParseException("Numerical value unexpected at this time.", pos)
            elif c == '.' and value.find('.') != -1:
                raise MatrixParseException("Malformed floating point literal.", pos)
            elif c == '-' and len(value) > 0:
                raise MatrixParseException("Negative symbol must appear at the beginning of a numerical value.", pos)
            value += c
        elif c == ',' or c == ']':
            if depth > 1: # We've just came from a value
                if len(value) == 0:
                    raise MatrixParseException("Empty value.", pos)
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
                        raise MatrixParseException("Row widths are inconsistent.", pos)
                invalue = False # Since the only time we have these we expect to start another
                depth -= 1
                if depth < 0:
                    raise MatrixParseException("Invalid Syntax.", pos)
                
        elif c in [' ', '\t', '\n', '\r']:
            invalue = len(value) == 0 and depth > 1 # We no longer expect to start a new value as the
                                      # next token if we've already started one
        else:
            raise MatrixParseException("Unexpected character '%s'." % (c), pos)
    if depth > 0:
        raise MatrixParseException("Matrix improperly ended.", pos)
    return result

def Augment(A, B, Mutate = False):
    '''Augment matrix A with matrix B.
    
    Raises IncompatibleMatrixException if A and B have a differing number of rows.
    
    Returns a 2-dimensional list representing the resultant matrix.'''
    
    if not len(A):
        raise EmptyMatrixException("Operand A has no rows")
    if not len(B):
        raise EmptyMatrixException("Operand B has no rows")

    if len(A) != len(B):
        raise IncompatibleMatrixException("Operand matrix does not have an equal number of rows")
    if Mutate:
        NewRows = A
    else:
        NewRows = Copy(A)
    ColCount = len(B[0])
    for RowIndex, Row in enumerate(B):
        if RowIndex != 0:
            RowColCount = len(Row)
            if RowColCount != ColCount:
                raise IrregularRowException("Row %d has %d columns but row 0 has %d columns" % (RowIndex, RowColCount, ColCount))
        NewRows[RowIndex] += Row # TODO: Validate that every row in B is of

    return NewRows
    
def Multiply(A, B):
    '''Multiply matrix A by matrix B.
    
    Returns a 2-dimensional list representing the resultant matrix.'''
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
    '''Modulo a constant factor to all terms in a Matrix.

    Returns a 2-dimensional list representing the resultant matrix.'''
    F = lambda v, x, y: v % Mod
    return ApplyFunc(Matrix, F, Mutate)

def Scale(Matrix, Factor, Mutate = False):
    '''Multiply a constant factor to all terms in a Matrix.
    
    Returns a 2-dimensional list representing the resultant matrix.'''
    F = lambda v, x, y: v * Factor
    return ApplyFunc(Matrix, F, Mutate)

def Add(Matrix, Factor, Mutate = False):
    '''Add a constant factor to all terms in a Matrix.
    
    Returns a 2-dimensional list representing the resultant matrix.'''
    F = lambda v, x, y: v + Factor
    return ApplyFunc(Matrix, F, Mutate)

def Negate(Matrix, Mutate = False):
    '''Negate all terms in a Matrix.

    Returns a 2-dimensional list representing the resultant matrix.'''
    F = lambda v, x, y: -v
    return ApplyFunc(Matrix, F, Mutate)

def Identity(Matrix):
    '''Generates the identity matrix for the operand matrix.
    
    Raises NonSquareMatrixException if the operand matrix is invalid.

    Returns a 2-dimensional list representing the resultant matrix.'''
    ValidateSquare(Matrix)
    F = lambda v, x, y: 1 if x == y else 0
    return ApplyFunc(Matrix, F, Mutate = False)

def ValidateSquare(Matrix):
    '''Validates that the operand Matrix is square.

    Raises NonSquareMatrixException if the operand matrix is invalid.'''
    RowCount = len(Matrix)
    for Row in Matrix:
        if RowCount != len(Row):
            raise NonSquareMatrixException("Must be square")

def Copy(Matrix):
    '''Creates a shallow copy of the operand matrix.

    Returns a 2-dimensional list representing the resultant matrix.'''
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
            raise NonSquareMatrixException("Matrix must be square")
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



