from utils import util
import hashlib


def test_is_file_exist(file_path):
    res = util.is_file_exist(file_path)
    print(res)


def decode_string(s):
    if len(s) % 2 == 1:
        raise ValueError("invalid data")
    res = []
    for i in range(len(s) // 2):
        temp = calculate_hex(s[i * 2:i * 2 + 2])
        res.append(temp)
    return res


def calculate_hex(s):
    num = []
    for i in range(2):
        if '0' <= s[i] and s[i] <= '9':
            num.append(ord(s[i]) - ord('0'))
        elif 'a' <= s[i] and s[i] <= 'f':
            num.append(ord(s[i]) - ord('a') + 10)
        elif 'A' <= s[i] and s[i] <= 'F':
            num.append(ord(s[i]) - ord('A') + 10)
    return num[0] << 4 | num[1]


if __name__ == '__main__':
    if type("123")==int:
        print('good')
