Strict Typing in Python
=======================

A simple decorator `@types` that gives you the ability to restrict the type
of a function's arguments and return values.

## Examples ##

    @types(x=int, y=int, _ret_type=int)
    def add2(x, y):
        '''this is add2'''
        return x+y

    @types(str, _ret_type=str)
    def end_char(strn):
        if len(strn) == 0: return
        else: return strn[-1]

If you call one of these functions correctly, it behaves normally:

    >>> add2(3,5)
    8

But call it with the wrong types and you get a TypeError:

    >>> add2('h',5)
    Traceback (most recent call last):
    ...
    TypeError: Argument 0 of add2 is type str ('h'), expected int

