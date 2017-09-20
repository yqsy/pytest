def simple_coroutine():
    print('-> coroutine started')
    x = yield
    print('-> coroutine received:', x)


def main1():
    my_coro = simple_coroutine()
    print(my_coro)

    # 预激"prime"协程
    next(my_coro)

    # 触发协程
    my_coro.send(42)


def simple_coro2(a):
    print('-> Started: a =', a)
    b = yield a
    print('-> Received: b=', b)
    c = yield a + b
    print('-> Received: c=', c)


def main2():
    my_coro2 = simple_coro2(14)

    from inspect import getgeneratorstate

    # 状态是刚创建完毕,等待外面取走a
    print(getgeneratorstate(my_coro2))

    # 产生数字14
    print(next(my_coro2))

    # 产生数字 a + b
    print(my_coro2.send(28))


    # 协程终止
    # my_coro2.send(29)


if __name__ == '__main__':
    # main1()
    main2()
