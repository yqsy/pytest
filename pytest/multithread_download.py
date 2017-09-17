import threading
from collections import namedtuple
from queue import Queue

import requests

DOWNLOAD_URL = r'http://sw.bos.baidu.com/sw-search-sp/software/0f1809fc9bd9d/BaiduHi_setup.exe'
THREAD_NUMS = 5
DWONLOAD_TO_FILE = r'D:/reference/tmp/BaiduHi_setup.exe'


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


class DownloadTask():
    def __init__(self, *, begin, end, url, filename):
        self.begin = begin
        self.end = end
        self.url = url
        self.filename = filename

    def run(self):
        # print('id:{} begin: {} end: {}'.format(threading.get_ident(), self.begin, self.end))

        headers = {'Range': 'bytes={}-{}'.format(self.begin, self.end)}

        r = requests.get(self.url, headers=headers, stream=True)

        with open(self.filename, 'r+b') as fp:
            fp.seek(self.begin)
            for data in r.iter_content(chunk_size=4096):
                fp.write(data)


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

    for one_part in slice_rtn:
        download_task = DownloadTask(begin=one_part[0], end=one_part[1], url=DOWNLOAD_URL, filename=DWONLOAD_TO_FILE)
        download_task_queue.put(download_task)

    download_task_queue.join()


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
