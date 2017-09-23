import asyncio


async def compute(x, y):
    print('Compute {} + {} ...'.format(x, y))
    await asyncio.sleep(1.0)
    return x + y


async def print_sum(x, y):
    result = await compute(x, y)
    print('{} + {} = {}'.format(x, y, result))


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_sum(1, 2))
    loop.close()


if __name__ == '__main__':
    main()
