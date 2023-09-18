"""
Truth table script:
    Process truth table of a function with the form:
        f(n...) -> m
    where type of n, m equals bool.
"""

def to_bin(i : int, length : int):
    text = "{0:b}".format(i) # Convert i into a string binary-sequence
    text = ("0" * (length - len(text))) + text # Concat remainder zeros to match required length
    return [bool(int(x)) for x in text] # Convert string into truth table's values

def table_of(func):
    length = func.__code__.co_argcount
    all_comb = []
    # Process all parameter's combinations for func:
    #   = 2 ** n
    # where n = count of func's arguments
    for i in range(2 ** length):
        all_comb.append(to_bin(i, length))

    print(f" - Table of {func.__name__} -")
    for comb in all_comb:
        print(f"{func.__name__}{comb} = {func(*comb)}")
    print("")
