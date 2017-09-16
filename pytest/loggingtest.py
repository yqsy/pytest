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


class ExceptionHandler(logging.StreamHandler):
    """
    提供qt错误窗口信息支持,当产生ERROR日志信息时,触发signal
    """

    def __init__(self):
        super(ExceptionHandler, self).__init__()
        self.log_signal = LogSignal()

    def emit(self, record):
        formated = self.format(record)
        self.log_signal.update_signal.emit(formated)

    def handler(self, etype, value, tb):
        err_str = '{} {} {}'.format(etype, value, traceback.format_tb(tb))
        logger.error(err_str)


class LogDialog(QDialog):
    def __init__(self):
        super(LogDialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.qh_box_layout = QHBoxLayout()
        self.edit = QTextEdit(self)
        self.edit.setMinimumWidth(500)
        self.qh_box_layout.addWidget(self.edit)

        self.qv_box_layout = QVBoxLayout()
        self.qv_box_layout.setAlignment(Qt.AlignTop)

        self.button = QPushButton('日志', self)
        self.button.clicked.connect(self.generate_log)
        self.qv_box_layout.addWidget(self.button)

        self.button2 = QPushButton('Thread', self)
        self.button2.clicked.connect(self.create_thread)
        self.qv_box_layout.addWidget(self.button2)

        self.button3 = QPushButton('除零', self)
        self.button3.clicked.connect(self.division)
        self.qv_box_layout.addWidget(self.button3)

        self.button4 = QPushButton('长串异常', self)
        self.button4.clicked.connect(self.errors)
        self.qv_box_layout.addWidget(self.button4)

        self.button5 = QPushButton('清空', self)
        self.button5.clicked.connect(self.clean_text)
        self.qv_box_layout.addWidget(self.button5)

        self.layout.addLayout(self.qh_box_layout)
        self.layout.addLayout(self.qv_box_layout)

    def clean_text(self):
        self.edit.clear()

    def errors(self):
        f()

    def division(self):
        0 / 0

    def generate_log(self):
        logger.debug('log')

    threadpool = QThreadPool()

    def create_thread(self):
        class MyLog(QRunnable):
            def run(self):
                for i in range(3):
                    logger.debug(i)
                    time.sleep(0.5)

                0 / 0

        self.threadpool.start(MyLog())

    @pyqtSlot(str)
    def add_log(self, msg):
        self.edit.append(msg)


class ErrorHandleDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(ErrorHandleDialog, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.front_box = QVBoxLayout()
        self.setLayout(self.front_box)
        self.hbox = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        self.front_box.addLayout(self.hbox)
        self.front_box.addLayout(self.hbox2)

        self.hbox2.setAlignment(Qt.AlignRight)

        self.error_edit = QTextEdit(self)
        self.hbox.addWidget(self.error_edit)

        self.send_email_button = QPushButton('send mail', self)
        self.hbox2.addWidget(self.send_email_button)

        self.setWindowTitle('发生了一个没有预料到的异常')

    @pyqtSlot(str)
    def error_handle(self, err):
        self.error_edit.setText(err)
        self.exec_()


if __name__ == '__main__':
    # 设置异常回调(临时)
    sys.excepthook = traceback.print_exception

    # 测试模块输出
    hello()

    # 设置cmd窗口作为输出handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(console)

    # 设置消息控制台作为输出handler
    dialog_handler = DialogHandler()
    dialog_handler.setLevel(logging.DEBUG)
    dialog_handler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(dialog_handler)

    # 设置异常窗体(发送邮件)
    exception_handler = ExceptionHandler()
    exception_handler.setLevel(logging.ERROR)
    exception_handler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(exception_handler)

    # 重置异常回调
    sys.excepthook = exception_handler.handler

    # 开启窗口输出日志
    app = QApplication(sys.argv)
    log_dialog = LogDialog()

    # 连接到消息控制台的日志增加槽函数
    dialog_handler.log_signal.update_signal.connect(log_dialog.add_log)

    # 连接到错误提示/发送邮件窗口的提示槽函数(exec_)
    error_handle_dialog = ErrorHandleDialog(log_dialog)
    exception_handler.log_signal.update_signal.connect(error_handle_dialog.error_handle)

    log_dialog.show()
    sys.exit(app.exec_())
