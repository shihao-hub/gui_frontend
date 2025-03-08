import functools


def io_operation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def thread_exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # todo: recording information
            return func(*args, **kwargs)
        except Exception as e:
            print(f"函数 {func.__name__} 执行失败: {e}")
            raise

    return wrapper
