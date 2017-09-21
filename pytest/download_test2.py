import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

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


def download_many2(cc_list):
    cc_list = cc_list[:5]
    with ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))

        results = []
        for future in as_completed(to_do):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)

    return len(results)


if __name__ == '__main__':
    main(download_many2)
