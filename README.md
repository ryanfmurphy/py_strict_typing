Strict Typing in Python
=======================

Provides a simple decorator that gives you the ability to restrict the type
of a function's arguments and return values.

Examples:

    @strict_typing(x=int, y=int, _ret_type=int)
    def add2(x, y):
        '''this is add2'''
        return x+y

    @strict_typing(str, _ret_type=str)
    def end_char(strn):
        if len(strn) == 0: return
        else: return strn[-1]

