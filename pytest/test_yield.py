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


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count


def main3():
    coro_avg = averager()

    # 取第一个average,让协程函数等待在term = yield
    print(next(coro_avg))

    # 赋值term,并来到下一个yield,取出来average
    print(coro_avg.send(10))
    print(coro_avg.send(20))
    print(coro_avg.send(30))



if __name__ == '__main__':
    # main1()
    # main2()
    main3()
