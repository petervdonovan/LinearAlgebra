import maths
import utils

# def get_like_terms(terms):
#     """Returns a dictionary containing the like terms in the 
#     expression.
    
#     Categorization of terms has two levels. The first level is a
#     tuple in alphabetical order containing the hashable form of the
#     numerator of the expression without its constant coefficient; the
#     second level is a similar tuple containing the hashable form of the
#     denominator without its constant coefficient. The ratio of the
#     numerator and denominator coefficients is in the list accessed at
#     the appropriate index.
#     """
#     assert all(
#             isinstance(expr, RationalExpression) for expr in terms
#             ), ("The elements of {} are not all of type "
#                 + "RationalExpression.").format(terms)
#     ret = dict()
#     for term in terms:
#         term = MultiplicationExpression(term.simplified())
#         numerator_terms = []
#         denominator_terms = []
#         coefficient_terms = []
#         for factor in term:
#             # We check whether the factor can be evaluated as a constant:
#             if factor.eval() is not None:
#                 coefficient_terms.append(factor)
#             else:
#                 if isinstance(factor, ReciprocalExpression):
#                     denominator_terms.append(factor.denominator)
#                 else:
#                     numerator_terms.append(factor)
#         def list_to_product(list_):
#             if not numerator_terms:
#                 return SimpleExpression(1)
#             return MultiplicationExpression(*numerator_terms)
#         numerator = list_to_product(numerator_terms)
#         denominator = list_to_product(denominator_terms)
#         coefficient = list_to_product(coefficient_terms)
#         print("DEBUG: term is {}, coefficient factors are {}, numerator factors are {}, and denominator factors are {}".format(str(term), str(coefficient_terms), str(numerator_terms), str(denominator_terms)))
#         index1 = numerator.package()
#         index2 = denominator.package()
#         if index1 not in ret:
#             ret[index1] = dict()
#         if index2 not in ret[index1]:
#             ret[index1][index2] = list()
#         ret[index1][index2].append(coefficient)
#     print("DEBUG: like terms:", ret)
#     return ret


def str_to_expression(string):
    """Returns the expression described by the string.
    >>> str(str_to_expression("6xy"))
    '6xy'
    >>> str(str_to_expression("6xy+2"))
    '6xy + 2'
    >>> str(str_to_expression("2b- 2"))
    '2b - 2'
    """
    string = string.strip()
    operators = [
        ("+", AdditionExpression, lambda x: x),
        ("*", MultiplicationExpression, lambda x: x),
        ("/", MultiplicationExpression, ReciprocalExpression),
        (
            "-",
            AdditionExpression,
            lambda x: MultiplicationExpression(SimpleExpression(-1), x)
        )
    ]
    for op in operators:
        if op[0] in string:
            parts = string.split(op[0])
            return op[1](
                str_to_expression(parts[0]),
                *[
                    op[2](str_to_expression(part))
                    for part in parts[1:]
                ]
            )
    # Means that this string contains no explicit operators
    factors = []
    for token in maths.get_math_tokens_from_string(string):
        if type(token) == int: # This factor is an integer.
            for prime in maths.get_prime_factors(token):
                factors.append(prime)
        else: # This factor is an variable.
            factors.append(token)
    factors = [SimpleExpression(factor) for factor in factors]
    return MultiplicationExpression(*factors)
class RationalExpression:
    """Exactly represents an expression whose value is a rational
    number.
    """
    def __add__(self, other):
        """Returns a new expression representing the sum of two
        expressions.
        """
        return AdditionExpression(self, other)
    def __mul__(self, other):
        """Returns a new expression representing the product of two
        expressions.
        """
        return MultiplicationExpression(self, other)
    def __div__(self, other):
        """Returns a new expression representing the quotient of two
        expressions.
        """
        return MultiplicationExpression(self, ReciprocalExpression(other))
    def __sub__(self, other):
        """Returns a new expression representing the difference of two
        expressions.
        """
        return AdditionExpression(self, MultiplicationExpression(-1, other))
    def simplified(self):
        """Returns an equivalent expression."""
        return self
    def package(self):
        """Returns a hashable representation of SELF containing all
        information necessary to reconstruct an expression
        equivalent to SELF.
        """
        return str(self.simplified())
    @classmethod
    def unpackage(cls, package):
        """Returns an expression recovered from the hashable form of an
        expression."""
        return str_to_expression(package)
    def var_string(self):
        """Returns a string representation of the variables in the
        expression only (no operators, spaces, or coefficients)
        >>> str_to_expression("a + ab + 2c").var_string()
        'aabc'
        """
        return "".join(
            character for character in str(self)
            if character.isalpha()
        )


class CompoundExpression(RationalExpression):
    """Represents an expression that includes other expressions."""
    def __init__(self, *subexpressions):
        """Initializes an expression with the subexpressions that it
        comprises (all of which must be RationalExpressions)
        """
        assert len(subexpressions) > 0, "An expression must have contents."
        assert all(
            isinstance(expr, RationalExpression) for expr in subexpressions
            ), "The elements of {} are not all of type \
                RationalExpression.".format(subexpressions)
        self.subexpressions = list(subexpressions)
    def __getitem__(self, key):
        """Returns the term corresponding to a given index."""
        return self.subexpressions[key]
    def __len__(self):
        """Returns the number of subexpressions that this contains."""
        return len(self.subexpressions)
    def unlayered(self):
        """Returns an equivalent expression that contains the fewest
        distinct operations possible.
        """
        return type(self)(*[
            item.unlayered()
            for item in self
        ])


class AdditionExpression(CompoundExpression):
    """Represents the sum of an arbitrary number of terms.
    """
    def __str__(self):
        """Returns the string representation of this expression."""
        return "(" + " + ".join(str(term) for term in self.subexpressions) + ")"
    
    def simplified(self):
        """Returns a simpler equivalent expression, where expressions
        involving variables are in alphabetical order and constant
        terms are at the end.

        >>> print(str_to_expression("1 + 2").simplified())
        3
        >>> print(str_to_expression("1 + 2 + z").simplified())
        z + 3
        >>> print(str_to_expression("1 + 2 + z + 3 + 2z + a").simplified())
        a + 3z + 6
        >>> print(str_to_expression("ab + bc + 2ab").simplified())
        3ab + bc
        >>> print(str_to_expression("aa + a + ab").simplified())
        a + aa + ab
        """
        unlayered = AdditionExpression.unlayered(self)
        constants = []
        like_terms = dict()
        for term in unlayered:
            coefficient_factors = [
                factor for factor in term
                if factor.eval() is not None
            ]
            if not coefficient_factors:
                coefficient_factors = [SimpleExpression(1)]
            non_coefficient_factors = [
                factor for factor in term
                if factor.eval() is None
            ]
            if len(non_coefficient_factors) == 0:
                constants.append(
                    MultiplicationExpression(*coefficient_factors)
                )
            else:
                id = MultiplicationExpression(
                    *non_coefficient_factors
                ).package()
                if id not in like_terms:
                    like_terms[id] = list()
                like_terms[id].append(MultiplicationExpression(
                    *coefficient_factors
                ))
        print("DEBUG: like_terms:", like_terms)
        terms = utils.sorted([
            MultiplicationExpression(
                AdditionExpression(*like_terms[id]),
                MultiplicationExpression(RationalExpression.unpackage(
                    id
                ))
            )
            for id in like_terms
        ], lambda expr: str(expr))
        if constants:
            terms.append(AdditionExpression(*constants))
        return AdditionExpression(*terms).unlayered()
        # # Expand into a series of terms
        # terms = [term.simplified() for term in self.subexpressions]
        # terms = unpack(terms, AdditionExpression)
        # # Combine like terms
        # indexed_terms = get_like_terms(terms)
        # resulting_terms = list()
        # for numerator in indexed_terms:
        #     for denominator in indexed_terms[numerator]:
        #         coeff = AdditionExpression(
        #             *[
        #                 term.simplified() for term in
        #                 indexed_terms[numerator][denominator]
        #             ]
        #         )
        #         numerator = RationalExpression.unpackage(numerator)
        #         denominator = RationalExpression.unpackage(denominator)
        #         parts = []
        #         if not coeff.is_empty():
        #             parts.append(coeff)
        #         if not numerator.is_empty():
        #             parts.append(numerator)
        #         if not denominator.is_empty():
        #             print("DEBUG: denominator.subexpressions =", denominator.subexpressions)
        #             parts.append(
        #                 ReciprocalExpression(denominator)
        #             )
        #         resulting_terms.append(MultiplicationExpression(*parts))
        # resulting_terms = sorted(
        #     resulting_terms,
        #     key=lambda expr: expr.var_string()
        # )
        # if len(resulting_terms) > 0:
        #     return AdditionExpression(*resulting_terms)
        # else:
        #     return resulting_terms[0]
    def eval(self):
        """Returns the inexact float representation of the expression."""
        term_values = [term.eval() for term in self.subexpressions]
        return None if None in term_values else sum(term_values)
    def unlayered(self):
        """Returns an equivalent expression that contains the fewest
        distinct operations possible.
        """
        if len(self) == 1:
            return self[0]
        return super().unlayered()
class MultiplicationExpression(CompoundExpression):
    """Represents a product of 1 and one or more rational
    expressions.
    """
    def __str__(self):
        """Returns the string representation of this expression."""
        return "*".join(str(factor) for factor in self.subexpressions)
    def simplified(self):
        """Returns a simpler equivalent expression in the form
        of a sum of non-combinable terms.
        """
        unlayered = self.unlayered()
        # TODO: Apply distributive property
        return unlayered
    def eval(self):
        """Returns the inexact float representation of the expression."""
        factor_values = [factor.eval() for factor in self.subexpressions]
        return None if None in factor_values else maths.product(factor_values)
class ReciprocalExpression(RationalExpression):
    """Represents the reciprocal of another expression."""
    def __init__(self, denominator):
        """Creates an expression representing the reciprocal of
        DENOMINATOR."""
        self.denominator = denominator
    def __str__(self):
        """Returns the string representation of this expression."""
        return "1 / " + str(self.denominator)
    def eval(self):
        """Returns the inexact float representation of the
        expression.
        """
        return None if self.denominator is None else 1 / self.denominator
class SimpleExpression(RationalExpression):
    """Represents an atomic expression -- either a prime number or a
    variable.
    """
    def __init__(self, value):
        """Initializes this SimpleExpression with the single value that
        it contains.
        """
        self.value = value
    def __str__(self):
        """Returns the string representation of this expression."""
        return str(self.value)
    def eval(self):
        """Returns the float approximation of the numerical value of
        this expression, if that numerical value is known.
        """
        return self.value if isinstance(self.value, int) else None
    def unlayered(self):
        """Returns an equivalent expression that contains the fewest
        distinct operations possible. In a SimpleExpression, there are
        already 0 operations, which is the minimum theoretically
        possible.
        """
        return self