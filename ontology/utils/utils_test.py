from ontology.utils import util
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

c=[0, 198, 107, 20]
a = "44425ae42a394ec0c5f3e41d757ffafa790b53f7301147a291ab9b60a956394c"
b = bytearray.fromhex(a)
d=[68, 66, 90, 228, 42, 57, 78, 192, 197, 243, 228, 29, 117, 127, 250, 250, 121, 11, 83, 247, 48, 17, 71, 162, 145, 171, 155, 96, 169, 86, 57, 76]
d=bytearray(d)
print(d)
print(d.hex())
