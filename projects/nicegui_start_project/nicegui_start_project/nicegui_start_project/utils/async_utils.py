__all__ = ["sync_to_async"]

import asyncio

from .mediator import thread_pool


async def sync_to_async(func, *args, **kwargs):
    def sync_code():
        return func(*args, **kwargs)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(thread_pool().get_pool(), sync_code)
