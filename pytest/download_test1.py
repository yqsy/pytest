import os

import requests
import sys

import time

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'http://flupy.org/data/flags'

DEST_DIR = 'downloads/'


def main():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    t0 = time.time()

    for cc in sorted(POP20_CC):
        url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
        resp = requests.get(url)
        image = resp.content
        print(cc, end=' ')
        sys.stdout.flush()
        path = os.path.join(DEST_DIR, cc.lower() + '.gif')
        with open(path, 'wb') as fp:
            fp.write(image)

    count = len(POP20_CC)
    elapsed = time.time() - t0

    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))
    

if __name__ == '__main__':
    main()
