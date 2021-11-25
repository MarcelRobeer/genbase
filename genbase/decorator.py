"""Base support for decorators."""

import inspect

from genbase.utils import recursive_to_dict


def add_callargs(function):
    """Decorator that passes `__callargs__`  to a function if available. Useful in conjunction with `MetaInfo`."""

    def inner(*args, **kwargs):
        ba = inspect.signature(function).bind(*args, **kwargs)
        ba.apply_defaults()

        kw = next((k for k, v in ba.signature.parameters.items()
                   if k == '__callargs__' or v.kind == inspect._ParameterKind.VAR_KEYWORD),
                  None)

        # Do not decorate the function if we are unable to pass __callargs__ as an argument
        if kw is None:
            return function(*ba.args, **ba.kwargs)

        # Construct __callargs__ (including introspection of the self argument)
        callargs = {'__name__': function.__name__, **dict(recursive_to_dict(ba.arguments))}
        if hasattr(function, '__self__') and 'self' not in callargs.keys():
            callargs['self'] = function.__self__
        if 'self' in callargs.keys():
            self = callargs.pop('self')
            callargs['self'] = self.to_config() if hasattr(self, 'to_config') and hasattr(self, '_dict') \
                else dict(recursive_to_dict(self))
            if '__name__' not in callargs['self'] and hasattr(self, '__class__') or hasattr(self, '__name__'):
                callargs['self']['__name__'] = self.__class__.__name__ if hasattr(self, '__class__') \
                    else self.__name__

        callargs.pop('__class__', None)
        return function(*ba.args, __callargs__=callargs, **ba.kwargs)
    return inner
