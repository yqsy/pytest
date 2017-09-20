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


if __name__ == '__main__':
    main()
