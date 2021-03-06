from collections import deque

class fzset(frozenset):
    def __repr__(self):
        return '{%s}' % ', '.join(map(repr, self))


def classify_bool(seq, pred):
    true_elems = []
    false_elems = []

    for elem in seq:
        if pred(elem):
            true_elems.append(elem)
        else:
            false_elems.append(elem)

    return true_elems, false_elems

def classify(seq, key=None):
    d = {}
    for item in seq:
        k = key(item) if (key is not None) else item
        if k in d:
            d[k].append(item)
        else:
            d[k] = [item]
    return d

def bfs(initial, expand):
    open_q = deque(list(initial))
    visited = set(open_q)
    while open_q:
        node = open_q.popleft()
        yield node
        for next_node in expand(node):
            if next_node not in visited:
                visited.add(next_node)
                open_q.append(next_node)




try:
    STRING_TYPE = basestring
except NameError:   # Python 3
    STRING_TYPE = str

###{standalone

import types
import functools
from contextlib import contextmanager

Str = type(u'')

def inline_args(f):
    # print '@@', f.__name__, type(f), isinstance(f, types.FunctionType), isinstance(f, types.TypeType), isinstance(f, types.BuiltinFunctionType)
    if isinstance(f, types.FunctionType):
        @functools.wraps(f)
        def _f_func(self, args):
            return f(self, *args)
        return _f_func
    elif isinstance(f, (type, types.BuiltinFunctionType)):
        @functools.wraps(f)
        def _f_builtin(_self, args):
            return f(*args)
        return _f_builtin
    elif isinstance(f, types.MethodType):
        @functools.wraps(f.__func__)
        def _f(self, args):
            return f.__func__(self, *args)
        return _f
    elif isinstance(f, functools.partial):
        # wraps does not work for partials in 2.7: https://bugs.python.org/issue3445
        # @functools.wraps(f)
        def _f(self, args):
            return f(*args)
        return _f
    else:
        @functools.wraps(f.__call__.__func__)
        def _f(self, args):
            return f.__call__.__func__(self, *args)
        return _f


try:
    from contextlib import suppress     # Python 3
except ImportError:
    @contextmanager
    def suppress(*excs):
        '''Catch and dismiss the provided exception

        >>> x = 'hello'
        >>> with suppress(IndexError):
        ...     x = x[10]
        >>> x
        'hello'
        '''
        try:
            yield
        except excs:
            pass

###}



try:
    compare = cmp
except NameError:
    def compare(a, b):
        if a == b:
            return 0
        elif a > b:
            return 1
        else:
            return -1


import sre_parse
import sre_constants
def get_regexp_width(regexp):
    try:
        return sre_parse.parse(regexp).getwidth()
    except sre_constants.error:
        raise ValueError(regexp)
