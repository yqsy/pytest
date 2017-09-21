import sys
from concurrent.futures import ThreadPoolExecutor

from pytest.download_test1 import get_flag, show, save_flag, main

MAX_WORKERS = 20


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc)
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with ThreadPoolExecutor(workers) as executor:
        # res是一个生成器
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))


if __name__ == '__main__':
    main(download_many)
