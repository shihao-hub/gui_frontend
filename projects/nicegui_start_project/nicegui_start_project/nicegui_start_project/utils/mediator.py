__all__ = ["thread_pool", "SingletonMeta"]


def thread_pool():
    from .thread_utils import thread_pool as thread_pool_alias
    return thread_pool_alias


def SingletonMeta():  # NOQA
    from .singleton import SingletonMeta as SingletonMeta_alias
    return SingletonMeta_alias
