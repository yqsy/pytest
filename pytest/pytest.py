import sys
import os
import logging
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

from pytest.common import hello

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
    format='%(asctime)s %(thread)d %(levelname)s %(filename)s:%(lineno)d %(message)s',
)

def f():
    logging.info('calling method g() in f()')
    return g()

def g():
    logging.info('calling method h() in g()')
    return h()

def h():
    logging.info('calling method i() in h()')
    return i()

def i():
    logging.info('append element i to gList in i()')

    raise Exception('exception has happen')



if __name__ == '__main__':
    hello()

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(thread)d %(levelname)s %(filename)s:%(lineno)d %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.debug('Information during calling f()')

    try:
        f()
    except Exception as ex:
        ty,tv,tb = sys.exc_info()
        logging.critical('{} {}'.format(ty,tv))
        logging.critical((traceback.format_tb(tb)))
        sys.exit(1)
