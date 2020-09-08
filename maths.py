"""Simple math operations involving basic Python types."""

def get_prime_factors(n):
    """Returns the prime factors of some integer n in increasing order.
    Special cases: Returns 0 if n == 0, includes -1 as a factor if
    n < 0.

    >>> get_prime_factors(6)
    [2, 3]
    >>> get_prime_factors(-8)
    [-1, 2, 2, 2]
    >>> get_prime_factors(242)
    [2, 11, 11]
    """
    i = 2
    if n < 0:
        return [-1, *get_prime_factors(-n)]
    while i < n:
        if n % i == 0:
            return [i, *get_prime_factors(n // i)]
        i += 1
    return [n]

def get_math_tokens_from_string(string):
    """Returns a ordered list of the individual mathematical
    meaning-units (tokens) from a string that contains no spaces or
    operators. Numbers are converted to integers; everything else
    remains in string form.
    >>> get_math_tokens_from_string("123ab")
    [123, 'a', 'b']
    >>> get_math_tokens_from_string("g4")
    ['g', 4]
    >>> get_math_tokens_from_string("6xy")
    [6, 'x', 'y']
    """
    tokens = list()
    current = ""
    for char in string:
        if char.isdigit():
            current += char
        else:
            if current:
                tokens.append(int(current))
                current = ""
            tokens.append(char)
    if current:
        tokens.append(int(current))
    return tokens

def product(iterable):
    """Returns the product of one and all of the items in ITERABLE."""
    product = 1
    for item in iterable:
        product += item
    return product