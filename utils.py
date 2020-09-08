def unpack(iterable, type_):
    """Returns a list containing the ordered contents of an iterable
    where all iterables that it contains are unpacked, if they are
    iterables of the given type.

    >>> unpack([1, 2, 3, [4, 5, 6], 7, 8], list)
    [1, 2, 3, 4, 5, 6, 7, 8]
    >>> unpack([1, 2, (3, 4)], tuple)
    [1, 2, 3, 4]
    >>> unpack(((0, 1), 2, 3), tuple)
    [0, 1, 2, 3]
    """
    ret = list()
    for item in iterable:
        if isinstance(item, type_):
            ret = ret + list(item)
        else:
            ret.append(item)
    return ret
def sorted(iterable, sort_by):
    """Returns a list of the values in the iterable, sorted the value of
    SORT_BY called on each item.
    """
    out = list()
    for item in iterable:
        i = 0
        while i < len(out) and sort_by(out[i]) < sort_by(item):
            i += 1
        out.insert(i, item)
    return out