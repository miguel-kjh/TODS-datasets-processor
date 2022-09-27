def list2atomic_item(*kargs, sep="-") -> list:
    """
    Convert a list to an atom.
    """
    st = [
        sep.join(arg)
        for arg in kargs
    ]
    return [sep.join(st)]
