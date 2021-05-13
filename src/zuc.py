from zuc_table import *


def rotate_left(x, times):
    """
    循环左移实现
    :param x: 输入参数x,int
    :param times: 左移位数,int
    :return: 循环左移结果,int
    """
    return ((x << times) | (x >> (32 - times))) & 0xffffffff


def s_box(input_x):
    """
    s盒输入处理
    :param input_x:输入参数,int
    :return: s盒输出
    """
    result = 0
    x = [input_x >> 24, (input_x >> 16) & 0xff,
         (input_x >> 8) & 0xff, input_x & 0xff]
    for i in range(4):
        result = (result << 8) | sbox[i % 2][x[i]]
    return result


def fn_l(x, mode):
    """
    l函数，包括l1和l2
    :param x: 输入的参数,int
    :param mode: 模式，1为l1,2为l2,int
    :raise IndexError: 输入模式错误
    :return: l函数计算结果，int
    """
    if mode == 1:
        return x ^ rotate_left(x, 2) ^ rotate_left(x, 10) ^ rotate_left(x, 18) ^ rotate_left(x, 24)
    elif mode == 2:
        return x ^ rotate_left(x, 8) ^ rotate_left(x, 14) ^ rotate_left(x, 22) ^ rotate_left(x, 30)
    else:
        raise IndexError('You should input 1 or 2 for mode')


def key_format(key, iv):
    """
    密钥装入函数
    :param key:输入的密钥，string
    :param iv: 输入的初始向量，string
    :return: 密钥装入后的s, list[int]
    """
    s = []
    for i in range(16):
        s.append(int('{:08b}'.format(int(key[2 * i:2 * (i + 1)], 16)) + '{:015b}'.format(d[i]) + '{:08b}'.format(
            int(iv[2 * i:2 * (i + 1)], 16)), 2))

    return s


def lfsr(s, u=0):
    """
    线性反馈移位寄存器实现，包括工作模式和初始化模式
    :param s: 生成的s参数，list[int]
    :param u: 初始化模式下的参数，int
    :return: 完成移位后的s,list[int]
    """
    result = (2 ** 15 * s[15] + 2 ** 17 * s[13] + 2 ** 21 * s[10] +
              2 ** 20 * s[4] + (1 + 2 ** 8) * s[0]) % (2 ** 31 - 1)
    result = (result + u) % (2 ** 31 - 1)
    if result == 0:
        result = 2 ** 31 - 1
    del s[0]
    s.append(result)
    return s


def bit_reconstruction(s):
    """
    比特重组实现，生成x0,x1,x2,x3
    :param s: 生成的s参数
    :return: 比特重组后生成的比特字列表，list[int]
    """
    return [((s[15] & 0x7fff8000) << 1) | (s[14] & 0xffff), ((s[11] & 0xffff) << 16) | (s[9] >> 15),
            ((s[7] & 0xffff) << 16) | (s[5] >> 15), ((s[2] & 0xffff) << 16) | (s[0] >> 15)]


def f(x, r1, r2):
    """
    f函数实现
    :param x:x0,x1,x2 list[int]
    :param r1: 参数r1
    :param r2: 参数r2
    :return: f函数执行结果, int
    """
    w = ((x[0] ^ r1) + r2) % (2 ** 32)
    w1 = (r1 + x[1]) % (2 ** 32)
    w2 = r2 ^ x[2]
    r1 = s_box(fn_l((((w1 & 0xffff) << 16) | (w2 >> 16)), 1))
    r2 = s_box(fn_l((((w2 & 0xffff) << 16) | (w1 >> 16)), 2))
    return [w, r1, r2]


def init_round(key, iv):
    """
    初始轮执行函数
    :param key: 密钥，string
    :param iv: 初始向量, string
    :return: 初始轮执行后的变量s和r1,r2, list[list,int,int]
    """
    s = key_format(key, iv)
    r1 = 0
    r2 = 0
    for i in range(32):
        x = bit_reconstruction(s)
        w, r1, r2 = f(x[:3], r1, r2)
        lfsr(s, w >> 1)
    return [s, r1, r2]


def work_round(s, r1, r2, rounds=2):
    """
    工作模式执行
    :param rounds: 生成轮，int
    :param s: 初始轮生成的s列表，list[int]
    :param r1: 初时轮生成的r1, int
    :param r2: 初始论生成的r2, int
    :return: rounds轮生成的z, list[int]
    """
    result = []
    x = bit_reconstruction(s)
    w, r1, r2 = f(x[:3], r1, r2)
    lfsr(s)
    for i in range(rounds):
        x = bit_reconstruction(s)
        w, r1, r2 = f(x[:3], r1, r2)
        z = w ^ x[3]
        result.append(z)
        lfsr(s)
    return result


def zuc(key, iv, rounds=2):
    """
    祖冲之算法执行主体
    :param rounds: 执行轮，int
    :param key:密钥, string
    :param iv: 初始向量, string
    :return: rounds轮生成的z,list int
    """
    s, r1, r2 = init_round(key, iv)
    return work_round(s, r1, r2, rounds)


def format_print(ls):
    """
    数组打印8位16进制
    :param ls: 需要打印的列表
    :return: void
    """
    for num in ls:
        print('{:08X}'.format(num))


def main():
    print('all zeros result:')
    format_print(zuc('00000000000000000000000000000000',
                 '00000000000000000000000000000000'))
    print('all f result:')
    format_print(zuc('ffffffffffffffffffffffffffffffff',
                 'ffffffffffffffffffffffffffffffff'))
    print('random test result:')
    format_print(zuc('3d4c4be96a82fdaeb58f641db17b455b',
                 '84319aa8de6915ca1f6bda6bfbd8c766'))


if __name__ == '__main__':
    main()
