#/usr/bin/env python3


# https://stackoverflow.com/a/36944992
from functools import wraps

def wrapper(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        method_output = method(self, *method_args, **method_kwargs)
        return method_output + "!"
    return _impl

class Foo:
    @wrapper
    def bar(self, word):
        return word

f = Foo()
result = f.bar("kitty")
print(result)