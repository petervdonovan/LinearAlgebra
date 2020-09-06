def round2(num, places=2):
    """
    Returns the number expressed as an int if the 
    result of the built-in round function would
    only have zeros after the decimal place.
    """
    nearest_one = round(num)
    return (
        nearest_one
        if abs(num - nearest_one) < 0.1**places
        else round(num, places)
    )
def roundall(iterable, places=2):
    """
    Returns a tuple of all of the numbers in the iterable,
    in order, rounded by round2.
    """
    return tuple([round2(num, places) for num in iterable])