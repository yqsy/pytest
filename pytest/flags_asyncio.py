import asyncio

import aiohttp

from pytest.download_test1 import BASE_URL, show, save_flag, main


@asyncio.coroutine
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc)
    resp = yield from aiohttp.request('GET', url)
    image = yield from resp.read()
    return image


@asyncio.coroutine
def download_one(cc):
    image = yield from get_flag(cc)
    show(cc)
    save_flag(image, cc)
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)]

    # wait不是阻塞型函数,是一个协程,等传给它的所有协程运行完毕后结束
    # 把各个协程包装进一个Task对象,最终的结果是,wait处理的所有对象都通过某种方式编程Future类的实例
    wait_coro = asyncio.wait(to_do)

    # res是结束的期物 _未结束的期物
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()

    return len(res)


if __name__ == '__main__':
    main(download_many)
