import contextlib


# 这个应该是传统的做法,重载两个函数
class LookingGlass:
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type: 异常类
        :param exc_val: 异常实例
        :param exc_tb: traceback对象
        :return:
        """
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True


@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)


def main():
    # with 会调用 __enter__ 以及 __exit__
    with LookingGlass() as what:
        print(what)

    # 模拟with
    manager = LookingGlass()
    monster = manager.__enter__()
    print(monster)
    manager.__exit__(None, None, None)
    print(monster)

    # contextlib.contextmanager 上下文管理
    with looking_glass() as what:
        print(what)

if __name__ == '__main__':
    main()
