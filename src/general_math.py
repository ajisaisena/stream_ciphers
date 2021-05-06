def gcd(a, b):
    """
    最大公因数生成函数
    :param a:第一个整型输入值
    :param b:第二个整型输入值
    :return:a和b的整型最大公因数
    """
    return a if b == 0 else gcd(b, a % b)
