import dis
import functools
import inspect


def validate_param(param_name, validator):
    """
    Usage:
        @validate_param("x", lambda x: x > 1)
        def fn(x):
            pass
    """

    def decorator(func):
        sig = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            value = bound_args.arguments[param_name]
            if not validator(value):
                raise ValueError(f"Validation failed for `{param_name}`")
            return func(*args, **kwargs)

        return wrapper

    return decorator
