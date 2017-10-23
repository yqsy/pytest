from decimal import Decimal, ROUND_05UP


def resize_precision():
    """
    价格计算时,保留三位精度decimal,从外部来源的字符串不确定其精度也不确定计算之后得到的数值的精度
    所以有必要resize精度
    (不知道一个系统的浮点数计算的最佳实践究竟该是怎样?不过价格这样做应该没有大问题的吧)
    :return:
    """
    pass


def main():
    pass

# print(Decimal('9.25') + Decimal('-11.111'))
#
# if Decimal('-1.1') < Decimal('0'):
#     print(1)
#
# if Decimal('0.000') == Decimal('0'):
#     print(2)
#
# print(Decimal('1') - Decimal('0.000000001'))

# print((Decimal('1') / Decimal('3')).quantize(Decimal('0.001'), rounding=ROUND_05UP))




if __name__ == '__main__':
    main()
