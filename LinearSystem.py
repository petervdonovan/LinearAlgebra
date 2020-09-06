from Matrix import Matrix, get_pivot_position
from formatting import round2, roundall

class LinearSystem:
    """
    Describes a linear system of equations.
    """
    def __init__(self, aug_matrix=None, decimal_places=2):
        """
        Initializes this system based on its corresponding
        augmented matrix.
        """
        self.decimal_places = decimal_places
        if aug_matrix is None:
            while 1:
                print("Enter the augmented matrix for the system:\n")
                self.aug_matrix = Matrix()
                print(self)
                if "y" in input("Does this look correct? (y/n) ").lower():
                    break
        else:
            self.aug_matrix = aug_matrix
        self.ref = self.aug_matrix.ref()
    def __str__(self, decimal_places=2):
        """
        Represents this linear system as a string.
        """
        return "\n".join(
                " + ".join(
                        "{}*x{}".format(round2(entry, self.decimal_places), j+1) 
                        for j, entry in enumerate(row) 
                        if j < len(row) - 1
                    ) + " = " + str(round2(row[-1]))
                for row in self.aug_matrix
            )
    def num_solutions(self):
        """
        Returns the number of solutions that this system has.
        
        The only three values that can be returned by this function
        are 0, 1, and positive infinity.

        >>> LinearSystem(Matrix([[1, 1, 1], [2, 2, 2], [3, 3, 3]])).num_solutions()
        inf
        >>> LinearSystem(Matrix([[2, 1, 1], [4, 2, 1.25]])).num_solutions()
        0
        >>> LinearSystem(Matrix([[1, 1, 1], [2, 1, 2]])).num_solutions()
        1
        """
        if any(
                all(round2(entry, self.decimal_places) == 0 for entry in row[:-1]) \
                    and round2(row[-1], self.decimal_places) != 0
                for row in self.ref
            ):
            return 0
        num_tautologies = len([
            row for row in self.ref
            if all(round2(entry, self.decimal_places) == 0 for entry in row)
        ])
        num_constraints = len(self.ref) - num_tautologies
        num_vars = len(self.ref[0][:-1]) if len(self.ref) > 0 else 0
        if num_vars > num_constraints:
            return float("inf")
        else:
            return 1
    def solution(self):
        """
        Returns the unique solution to this equation, if a unique 
        solution exists.

        >>> roundall(LinearSystem(Matrix([[1, 1, 2], [1, 2, 3]])).solution())
        (1, 1)
        >>> roundall(LinearSystem(Matrix([[1, 1, 0, 3], [2, 1, 1, 7], [1, -1, 3, 8]])).solution())
        (1, 2, 3)
        """
        if self.num_solutions() != 1:
            return
        sols = dict()
        for row in self.ref[::-1]:
            pivot_pos = get_pivot_position(row, self.decimal_places)
            sols[pivot_pos] = (
                    row[-1] - sum(
                        sols[j+1]*coeff 
                        for j, coeff in list(enumerate(row))[pivot_pos:-1]
                    )
                ) / row[pivot_pos-1]
        return tuple([sols[j+1] for j in range(len(sols))])