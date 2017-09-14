import sys
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

from pytest.common import hello

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
    format='%(asctime)s %(thread)d %(levelname)s %(filename)s:%(lineno)d %(message)s',
)

if __name__ == '__main__':
    hello()

    logging.debug('Information during calling f()')