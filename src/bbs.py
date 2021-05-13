from general_math import *


def bbs(p, q, s, rounds):
    """bbs伪随机数生成

    :param p: 参数p
    :type p: int
    :param q: 参数q
    :type q: int
    :param s: 种子s
    :type s: int
    :param rounds: 轮数
    :type rounds: int
    :raises ValueError: p,q,s等参数检查
    :return: bbs生成列表
    :rtype: list
    """
    result = []
    if p % 4 != 3 or q % 4 != 3:
        raise ValueError("You're trying to input illegal params: p or q")
    n = p * q
    if gcd(s, n) != 1:
        raise ValueError("You're trying to input illegal param: s")
    x = s ** 2 % n
    for i in range(rounds):
        x = x ** 2 % n
        result.append(x % 2)
    return result


def main():
    print(bbs(383, 503, 101355, 20))


if __name__ == "__main__":
    main()
