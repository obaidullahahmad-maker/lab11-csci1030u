import asyncio


def normal_double(n):
    return n * 2


async def async_double(n):
    return n * 2

print(normal_double(5))
print(async_double(5))
