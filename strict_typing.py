#choose import inspect to merge args and kwargs
#choose modify __doc__ to show type signature

import inspect

def my_type_error(func, arg_key, val, exp_type, arg_type='Argument'):
    return TypeError(
        '{arg_type} {i} of {func} is type {type} ({val}), expected {exp_type}'.format(
            arg_type=arg_type,
            i=arg_key,
            func=func.__name__,
            type=type(val).__name__,
            val=repr(val),
            exp_type=exp_type.__name__,
    ))

def type_info(arg_names, arg_types, kwarg_types, ret_type):
    arg_types = (t.__name__ for t in arg_types)
    arg_pairs = zip(arg_names, arg_types)
    # add kwargs
    for name, the_type in kwarg_types.items():
        if the_type:
            arg_pairs.append((name,the_type.__name__))
    # turn it into a strn
    arg_pairs = (name + ': ' + the_type for (name,the_type) in arg_pairs)
    ret = ', '.join(arg_pairs)
    if ret_type:
        ret_type = ret_type.__name__
        ret += '\n' + 'returns: ' + ret_type
    return ret

def types(*arg_types, **kwarg_types):

    if arg_types is None: arg_types = []
    if kwarg_types is None: kwarg_types = {}

    # make sure it's mutable
    arg_types = list(arg_types)

    if '_ret_type' in kwarg_types:
        _ret_type = kwarg_types.pop('_ret_type')
    else:
        _ret_type = None
    funcdata, regular_arg_names = None, None # these will be populated inside
    def outer(func):
        funcdata = inspect.getargspec(func)
        regular_arg_names = funcdata.args
        def inner(*args, **kwargs):
            # look for holes in arg_types & kwarg_types, fill them in with each other
            for i,arg_name in enumerate(regular_arg_names):
                if len(arg_types) <= i: 
                    arg_types.append(None)
                this_arg_type = arg_types[i]
                # fill in arg_types with kwarg_types
                if this_arg_type is None \
                      and arg_name in kwarg_types \
                      and kwarg_types[arg_name] is not None:
                    arg_types[i] = kwarg_types[arg_name]
                # fill in kwarg_types with arg_types
                if arg_name not in kwarg_types \
                      or kwarg_types[arg_name] is None:
                    kwarg_types[arg_name] = arg_types[i]
            # check kwarg_types
            for kw,kw_val in kwargs.items():
                if kw in kwarg_types:
                    the_type = kwarg_types[kw]
                    if not isinstance(kw_val, the_type):
                        raise my_type_error(func, kw, kw_val, the_type, 'Keyword argument')
            # check regular arg_types
            for i,arg in enumerate(args):
                if len(arg_types) < i: break # didn't provide all arg_types
                the_type = arg_types[i]
                if not isinstance(arg, the_type):
                    raise my_type_error(func, i, arg, the_type)
            # ACTUAL FUNCTION CALL
            ret = func(*args, **kwargs)
            # check return type
            if _ret_type:
                if not isinstance(ret, _ret_type):
                    raise my_type_error(func, 'value', ret, _ret_type, 'Return')
            return ret
        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        if inner.__doc__ is None:
            inner.__doc__ = ''
        else:
            inner.__doc__ += '\n'
        inner.__doc__ += type_info(regular_arg_names, arg_types,kwarg_types,_ret_type)
        return inner
    return outer

@types(x=int, y=int, _ret_type=int)
def add2(x, y):
    '''this is add2'''
    return x+y

@types(str, _ret_type=str)
def end_char(strn):
    if len(strn) == 0: return
    else: return strn[-1]

