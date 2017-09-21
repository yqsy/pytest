import os

import requests
import sys

import time

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'http://flupy.org/data/flags'

DEST_DIR = 'downloads/'


def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def save_flag(image, cc):
    path = os.path.join(DEST_DIR, cc.lower() + '.gif')
    with open(path, 'wb') as fp:
        fp.write(image)


def download_many(cc_list):
    for cc in sorted(POP20_CC):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc)
    return len(cc_list)


def main(download_many):
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
