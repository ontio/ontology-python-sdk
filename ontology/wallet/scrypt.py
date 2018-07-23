MAX_INT = 9223372036854775807


class ScryptParam(object):
    def __init__(self, p=16384, n=8, r=8, DKLen=64):
        self.p = p
        self.n = n
        self.r = r
        self.DKLen = DKLen


def key(password, salt: bytearray, N, r, p, key_len: int):
    if N <= 1 or N & (N - 1) != 0:
        raise ValueError("scrypt: N should be greater than 1 and be a power of 2")
    if r * p >= 1 << 30 or r > MAX_INT / 128 / p or r > MAX_INT / 256 or N > MAX_INT / 128 / r:
        raise ValueError("scrypt: parameters are too large")


