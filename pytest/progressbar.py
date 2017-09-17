from math import isclose

import sys

import time


def get_msg(complete_ratio):
    bar_max = 50
    completed = '=' * int(bar_max * complete_ratio)
    if not isclose(complete_ratio, 1.0):
        completed = completed[:-1] + '>'
    uncompleted = ' ' * (bar_max - len(completed))
    return '\r{:.1%}[{}{}]'.format(complete_ratio, completed, uncompleted)


def main():
    for i in range(0, 100):
        sys.stdout.write(get_msg(i / 100))
        sys.stdout.flush()
        time.sleep(0.1)


if __name__ == '__main__':
    main()
