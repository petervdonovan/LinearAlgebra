import formatting

class Matrix:
    """
    Describes a 2D matrix, with implementation for extension of the matrix
    and elementary row operations.
    """
    def __init__(self, contents=None):
        """
        If contents is not None, then contents should be a list
        in the shape of a 2D array, where each list within the
        list represents one row. Otherwise, the matrix is created 
        using user input.
        """
        if contents is not None:
            self.contents = contents
        else:
            m = int(input("Number of rows? "))
            n = int(input("Number of cols? "))
            self.contents = [
                [
                    float(input("Number at row {}, column {}? ".format(i+1, j+1)))
                    for j in range(n)
                ]
                for i in range(m)
            ]
    def __str__(self, after_decimal=2):
        """
        Returns a string representation of the matrix.
        AFTER_DECIMAL: number of decimal places to show.
        """
        max_magnitude = max(abs(num) for row in self.contents for num in row)
        max_chars_before_decimal = int(sum(1 for i in range(max_magnitude) if i % 10 == 0) + 1) + 1 # for sign
        max_chars = max_chars_before_decimal + 1 + after_decimal #add 1 for decimal point
        out = ""
        for row in self.contents:
            for entry in row:
                out += ("{:<" + str(max_chars + 1) + "}").format(formatting.round2(entry, after_decimal))
            out += "\n"
        return out[:-1]
    def __getitem__(self, key):
        return self.contents[key]
    def __len__(self):
        return len(self.contents)
    def submatrix(self, start_row=1, start_col=1, end_row=None, end_col=None):
        """
        Returns a part of the matrix represented by this matrix.
        Boundaries are inclusive.

        >>> mat = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> print(mat.submatrix(2, 2))
        5     6     
        8     9     
        >>> print(mat.submatrix(1, 1, 2, 2))
        1     2     
        4     5     
        >>> print(mat.submatrix(1, 1, 2))
        1     2     3     
        4     5     6     
        """
        assert start_row > 0, "start_row cannot be less than the minimum row number"
        assert start_col > 0, "start_col cannot be less than the minimum column number"

        if end_row == None: end_row = len(self.contents)
        if end_col == None: end_col = len(self.contents[0] if len(self.contents) else 0)
        return Matrix(
            contents=[
                row[start_col - 1:end_col]
                for row in self.contents[start_row-1:end_row]
            ]
        )
    def insert(self, other, position):
        """
        Returns self with values from another matrix (OTHER).
        Position: Ordered pair with the row and column at which the other
        matrix should be inserted.
        
        >>> mat = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> other = Matrix([[11, 12], [13, 14]])
        >>> print(mat.insert(other, (1, 1)))
        11     12     3      
        13     14     6      
        7      8      9      
        >>> print(mat.insert(other, (2, 2)))
        1      2      3      
        4      11     12     
        7      13     14     
        >>> print(mat.insert(other, (1, 2)))
        1      11     12     
        4      13     14     
        7      8      9      
        >>> print(mat.insert(other, (3, 3)))
        1      2      3      
        4      5      6      
        7      8      11     
        """
        assert len(position) == 2
        assert min(*position) >= 1
        if len(self.contents) == 0:
            return Matrix([])
        if len(other.contents) == 0:
            return Matrix([[entry for entry in row] for row in self.contents])
        offset = (position[0] - 1, position[1] - 1)
        new_contents = [
            [
                (
                    other.contents[i - offset[0]][j - offset[1]]
                    if i - offset[0] in range(len(other.contents)) and j - offset[1] in range(len(other.contents[0]))
                    else self.contents[i][j]
                )
                for j in range(len(self.contents[0]))
            ]
            for i in range(len(self.contents))
        ]
        return Matrix(new_contents)
    def replace(self, row_to_mutate, mutator_row, scale):
        """
        Replaces the content of the ROW_TO_MUTATE with its current values plus 
        the values in the MUTATOR_ROW times SCALE.

        This is a side effect; return type is None.

        >>> mat = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> mat.replace(2, 1, -2)
        >>> print(mat)
        1     2     3     
        2     1     0     
        7     8     9     
        """
        assert min(row_to_mutate, mutator_row) > 0
        for j in range(len(self.contents[row_to_mutate - 1])):
            self[row_to_mutate - 1][j] += self[mutator_row - 1][j] * scale
    def interchange(self, row_a, row_b):
        """
        Swaps ROW_A with ROW_B.

        This is a side effect; return type is None.

        >>> mat = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> mat.interchange(2, 1)
        >>> print(mat)
        4     5     6     
        1     2     3     
        7     8     9     
        >>> mat.interchange(1, 2)
        >>> print(mat)
        1     2     3     
        4     5     6     
        7     8     9     
        """
        assert min(row_a, row_b) > 0
        if row_a == row_b: return
        temp = self.contents[row_a - 1]
        self.contents[row_a - 1] = self.contents[row_b - 1]
        self.contents[row_b - 1] = temp
    def scale(self, row_to_mutate, scale):
        """
        Replaces the content of the ROW_TO_MUTATE with its current values 
        times SCALE.

        This is a side effect; return type is None.

        >>> mat = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> mat.scale(1, 2)
        >>> print(mat)
        2     4     6     
        4     5     6     
        7     8     9     
        >>> mat.scale(3, 0.5)
        >>> print(mat)
        2     4     6     
        4     5     6     
        3.5   4     4.5   
        """
        self.contents[row_to_mutate - 1] = [
            entry * scale for entry in self.contents[row_to_mutate - 1]
        ]
    def copy(self):
        """
        Returns a copy of this matrix.
        """
        return Matrix([[entry for entry in row] for row in self.contents])
    def ref(self, accuracy=2):
        """
        Returns the row echelon form of this matrix.
        ACCURACY: Number of significant decimal places

        >>> print(Matrix([[1, 3, 4, 7], [3, 9, 7, 6]]).ref())
        3     9     7     6     
        0     0     1.67  5     
        >>> print(Matrix([[3, -4, 2, 0], [-9, 12, -6, 0], [-6, 8, -4, 0]]).ref())
        -9     12     -6     0      
        0      0      0      0      
        0      0      0      0      
        """
        mat = self.copy()
        if len(self) < 2:
            return mat
        first_entries = [row[0] for row in self]
        if not all(round(entry, accuracy) == 0 for entry in first_entries):
            # Step 1: Move row with pivot to top
            max_entry = max(first_entries)
            min_entry = min(first_entries)
            row_with_pivot = first_entries.index(
                max_entry if abs(max_entry) > abs(min_entry) else min_entry
            ) + 1
            mat.interchange(row_with_pivot, 1)
            # Step 2: Create zeros below the pivot
            for row in range(2, len(mat) + 1):
                mat.replace(row, 1, -mat[row - 1][0] / mat[0][0])
        # Step 3: Repeat
        return mat.insert(mat.submatrix(2, 2).ref(), (2, 2))
    def rref(self, accuracy=2):
        """
        Returns the reduced row echelon form of this matrix.
        ACCURACY: Number of significant decimal places

        >>> print(Matrix([[1, 3, 4, 7], [3, 9, 7, 6]]).rref())
        1     3     0     -5    
        0     0     1     3     
        >>> print(Matrix([[3, -4, 2, 0], [-9, 12, -6, 0], [-6, 8, -4, 0]]).rref())
        1     -1.33 0.67  0     
        0     0     0     0     
        0     0     0     0     
        """
        mat = self.ref()
        if len(self) < 2:
            return mat
        # Step 1: Scale all entries so that values in pivot positions are 1
        for i, row in enumerate(mat):
            pivot_pos = get_pivot_position(row)
            if pivot_pos is not None:
                mat.scale(i + 1, 1 / row[pivot_pos - 1])
        # Step 2: Create zeros above each pivot
        for i, row in enumerate(mat):
            pivot_pos = get_pivot_position(row)
            if pivot_pos is not None:
                for i2 in range(i):
                    mat.replace(i2 + 1, i + 1, -mat[i2][pivot_pos - 1] / row[pivot_pos - 1])
        return mat

def get_pivot_position(row, accuracy=2):
    for i in range(len(row)):
        if round(row[i], accuracy) != 0:
            return i + 1
