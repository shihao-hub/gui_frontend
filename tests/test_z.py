import asyncio


async def test():
    print(123123123)


test2 = lambda: test()


def test3():
    res = test2()
    print(type(res))
    return res


print(type(test2))
print(test3())
# asyncio.run(test3())
