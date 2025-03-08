def io_operation(func):
    from .utils import io_operation as io_operation_alias
    return io_operation_alias(func)


def thread_exception_handler(func):
    from .utils import thread_exception_handler as thread_exception_handler_alias
    return thread_exception_handler_alias(func)
