import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from pytest.download_test2 import download_one

CCS = ('CN ' * 1000)[:-1].split(' ')

def download_many(cc_list):
    max_workers = min(len(cc_list), 20)

    # 线程里面抛出异常呢???
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        to_do_map = {}
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do_map[future] = cc 

        done_iter = tqdm(as_completed(to_do_map), total=len(cc_list))

        for future in done_iter:
            res = future.result()


def main():
    download_many(CCS)


if __name__ == '__main__':
    main()
