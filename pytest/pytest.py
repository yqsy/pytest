"""
日志记录到console,前台的展示
发生异常时呼出qt窗口提示,并记录日志
"""

import sys
import os
import logging
import traceback

import time
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QObject, QThreadPool, QRunnable
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QTextEdit, QVBoxLayout, QPushButton

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

from pytest.common import hello

FORMAT = '%(asctime)s %(thread)d %(levelname)s %(filename)s:%(lineno)d %(message)s'

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[]
)

logger = logging.getLogger(__name__)


def f():
    logger.info('calling method g() in f()')
    return g()


def g():
    logger.info('calling method h() in g()')
    return h()


def h():
    logger.info('calling method i() in h()')
    return i()


def i():
    logger.info('append element i to gList in i()')

    raise Exception('exception has happen')


class LogSignal(QObject):
    update_signal = pyqtSignal(str)

    def __init__(self):
        super(LogSignal, self).__init__()


class DialogHandler(logging.StreamHandler):
    """
    提供qt窗口日志信息支持,当产生日志时,触发signal
    """
    def __init__(self):
        super(DialogHandler, self).__init__()

        self.log_signal = LogSignal()


    def emit(self, record):
        formated = self.format(record)

        self.log_signal.update_signal.emit(formated)


class LogDialog(QDialog):
    def __init__(self):
        super(LogDialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        self.qh_box_layout = QHBoxLayout(self)
        self.edit = QTextEdit(self)
        self.edit.setMinimumWidth(500)
        self.qh_box_layout.addWidget(self.edit)

        self.qv_box_layout = QVBoxLayout(self)
        self.qv_box_layout.setAlignment(Qt.AlignTop)

        self.button = QPushButton('日志', self)
        self.button.clicked.connect(self.generate_log)
        self.qv_box_layout.addWidget(self.button)

        self.button2 = QPushButton('Thread', self)
        self.button2.clicked.connect(self.create_thread)
        self.qv_box_layout.addWidget(self.button2)

        self.layout.addLayout(self.qh_box_layout)
        self.layout.addLayout(self.qv_box_layout)


    def generate_log(self):
        logger.debug('log')

    def create_thread(selfs):
        class MyLog(QRunnable):
            def run(self):
                for i in range(10):
                    logger.debug(i)
                    time.sleep(1)

        QThreadPool.globalInstance().start(MyLog())


    @pyqtSlot(str)
    def add_log(self, msg):
        self.edit.append(msg)

if __name__ == '__main__':
    # 设置异常回调
    sys.excepthook = traceback.print_exception

    # 测试模块输出
    hello()

    # 设置窗口作为输出handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(console)

    # 设置监控窗体作为输出handler
    dialog_handler = DialogHandler()
    dialog_handler.setLevel(logging.DEBUG)
    dialog_handler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(dialog_handler)

    # 开启窗口输出日志
    app = QApplication(sys.argv)
    log_dialog = LogDialog()

    # 链接槽
    dialog_handler.log_signal.update_signal.connect(log_dialog.add_log)

    log_dialog.show()
    sys.exit(app.exec_())

    # logger.debug('Information during calling f()')
    # try:
    #     f()
    # except Exception as ex:
    #     ty, tv, tb = sys.exc_info()
    #     logger.critical('{} {}'.format(ty, tv))
    #     logger.critical((traceback.format_tb(tb)))
    #     sys.exit(1)
