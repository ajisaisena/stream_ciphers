def rc4(key, text):
    """rc4实现代码

    :param key: 密钥列表
    :type key: list[int]
    :param text: 明（密）文列表
    :type text: list[int]
    :return: 密（明）文列表
    :rtype: list[int]
    """
    result = []
    s = []
    t = []
    for i in range(256):
        s.append(i)
        t.append(key[i % len(key)])
    j = 0
    for i in range(256):
        j = (j + s[i] + t[i]) % 256
        s[i], s[j] = s[j], s[i]
    i, j = 0, 0
    for letter in text:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        tmp = (s[i] + s[j]) % 256
        k = s[tmp]
        result.append(k ^ letter)
    return res_format(result)


def to_list(string):
    """字符串转列表函数，2个字符作为一个字节写入

    :param string: 写入的字符串
    :type string: string
    :return: 生成的对应的列表
    :rtype: list
    """
    result = []
    for i in range(0, len(string), 2):
        result.append(int(string[i:i + 2], 16))
    return result


def rc4_string(key, text):
    """rc4 字符串传入实现

    :param key: 密钥
    :type key: string
    :param text: 明文
    :type text: string
    :return: rc4加/解密结果
    :rtype: string
    """
    key_int = to_list(key)
    text_int = to_list(text)
    return rc4(key_int, text_int)


def res_format(hexs):
    """rc4结果格式化

    :param hexs: rc4结果列表
    :type hexs: list[int]
    :return: rc416进制字符串
    :rtype: string
    """
    result = ''
    for num in hexs:
        result += '{:02X}'.format(num)
    return result


def main():
    print(rc4_string('6e6f742d736f2d72616e646f6d2d6b6579',
                     '476f6f6420796f752061726520636f7272656374'))


if __name__ == '__main__':
    main()
