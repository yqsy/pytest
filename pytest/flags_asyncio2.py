import asyncio

import aiohttp
import tqdm
from pytest.download_test1 import BASE_URL, show, save_flag, main, POP20_CC


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


@asyncio.coroutine
def download_coro(cc_list):
    to_do = [download_one(cc) for cc in sorted(cc_list)]

    to_do_iter = asyncio.as_completed(to_do)

    to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
    for future in to_do_iter:
        res = yield from future


def download_many():
    loop = asyncio.get_event_loop()
    coro = download_coro(POP20_CC)
    loop.run_until_complete(coro)
    loop.close()


if __name__ == '__main__':
    download_many()
