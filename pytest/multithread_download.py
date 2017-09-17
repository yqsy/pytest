import operator
import threading
from cmath import isclose
from collections import namedtuple
from datetime import datetime
from queue import Queue

import requests
import sys

DOWNLOAD_URL = r'http://sw.bos.baidu.com/sw-search-sp/software/0f1809fc9bd9d/BaiduHi_setup.exe'
THREAD_NUMS = 5
DWONLOAD_TO_FILE = r'D:/reference/tmp/BaiduHi_setup.exe'

PRINT_INFO = namedtuple('PRINT_INFO', 'threadid begin end current')


class DownloadThread(threading.Thread):
    def __init__(self, download_task_queue):
        super(DownloadThread, self).__init__()

        # 多线程使用同一个queue,单生产者,多消费者
        self.download_task_queue = download_task_queue

    def run(self):
        while True:
            task = self.download_task_queue.get()
            task.run()
            self.download_task_queue.task_done()


class PrintThread(threading.Thread):
    def __init__(self, print_info_queue):
        super(PrintThread, self).__init__()
        self.print_info_queue = print_info_queue

    def run(self):
        self.begin_time = datetime.now()

        while True:
            print_info = self.print_info_queue.get()
            msg = self.generate_single_msg(print_info)
            print_msg = self.combine_print_msg(msg, print_info.begin)
            sys.stdout.write(print_msg)
            sys.stdout.flush()
            self.print_info_queue.task_done()

    # 通过文件下载起始点排序打印信息
    msg_dict = {}

    def combine_print_msg(self, msg, begin):
        """
        组合信息打印
        :param msg: 单条打印信息
        :param begin: 文件下载起始点,通过这个来排序打印位置
        :return:
        """
        self.msg_dict[begin] = msg

        sorted_msg_lst = sorted(self.msg_dict.values())

        print_msg = '\r'

        for value in sorted_msg_lst:
            print_msg = print_msg + value + '\n'

        return print_msg

    def generate_single_msg(self, print_info):
        """
        生成单条打印信息
        :param print_info: 通过print_info_queue传过来的下载信息
        :return:
        """
        file_bytes = print_info.end - print_info.begin
        size_str = sizeof_fmt(file_bytes)
        remain_bytes = file_bytes - print_info.current
        threadid = print_info.threadid
        download_time = datetime.now() - self.begin_time
        speed = int(print_info.current / download_time.seconds if download_time.seconds != 0 else 0.0)
        remain_time = remain_bytes / speed if speed != 0 else 0.0
        progress_bar = self.generate_progress_bar(print_info.current / file_bytes)

        print_msg = 'tid:{} {} [{}/{}] {}/s eta:{:.2f}s'.format(
            threadid,
            progress_bar,
            sizeof_fmt(print_info.current),
            sizeof_fmt(file_bytes),
            sizeof_fmt(speed),
            remain_time)

        return print_msg

    def generate_progress_bar(self, complete_ratio):
        bar_max = 50
        completed = '=' * int(bar_max * complete_ratio)
        if not isclose(complete_ratio, 1.0):
            completed = completed[:-1] + '>'
        uncompleted = ' ' * (bar_max - len(completed))
        return '{:.1%}[{}{}]'.format(complete_ratio, completed, uncompleted)


class DownloadTask():
    def __init__(self, *, begin, end, url, filename, print_info_queue):
        self.begin = begin
        self.end = end
        self.url = url
        self.filename = filename

        # 下载信息实时传递给打印信息队列
        self.print_info_queue = print_info_queue

    def run(self):
        print('id:{} begin: {} end: {}'.format(threading.get_ident(), self.begin, self.end))

        headers = {'Range': 'bytes={}-{}'.format(self.begin, self.end)}

        r = requests.get(self.url, headers=headers, stream=True)

        with open(self.filename, 'r+b') as fp:
            fp.seek(self.begin)

            current_bytes = 0
            for data in r.iter_content(chunk_size=4096):
                fp.write(data)
                current_bytes += len(data)

                prinf_info = PRINT_INFO(threadid=threading.get_ident(), begin=self.begin,
                                        end=self.end, current=current_bytes)
                self.print_info_queue.put(prinf_info)


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def main():
    r = requests.head(DOWNLOAD_URL)

    file_size = int(r.headers['content-length'])

    print('file size: {}'.format(sizeof_fmt(file_size)))

    # 根据线程数量划分成部分
    slice_rtn = slicing_file(file_size, THREAD_NUMS)
    print(slice_rtn)

    # 占据一个空文件
    print('begin to write an empty file')
    with open(DWONLOAD_TO_FILE, 'wb') as fp:
        fp.write(('\0' * file_size).encode())

    print('write empty file successfully')

    download_task_queue = Queue()

    for _ in range(THREAD_NUMS):
        t = DownloadThread(download_task_queue)
        t.setDaemon(True)
        t.start()

    print_info_queue = Queue()
    print_thread = PrintThread(print_info_queue)
    print_thread.setDaemon(True)
    print_thread.start()

    for one_part in slice_rtn:
        download_task = DownloadTask(begin=one_part[0], end=one_part[1], url=DOWNLOAD_URL,
                                     filename=DWONLOAD_TO_FILE, print_info_queue=print_info_queue)
        download_task_queue.put(download_task)

    download_task_queue.join()
    print_info_queue.join()


def slicing_file(sumbytes, part):
    """
    将文件分割成整数字节单块的若干块,不整除的字节数放到末尾
    :param sumbytes: 文件的总计字节数
    :param part: 分割成多少部分
    :return: [(begin,end), (begin,end)] , begin end 都是int型的
    """
    if part <= 0:
        return []

    each_part_bytes = sumbytes // part
    remain_bytes = sumbytes - each_part_bytes * part

    slice_rnt = []
    for i in range(part):
        begin = i * each_part_bytes
        end = begin + each_part_bytes

        # last ele
        if i == part - 1:
            end = end + remain_bytes

        # remove both 0
        if begin == 0 and end == 0:
            continue

        slice_rnt.append((begin, end))

    return slice_rnt


if __name__ == '__main__':
    main()
