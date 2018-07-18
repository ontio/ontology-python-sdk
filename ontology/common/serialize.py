def put_uint16(b: bytearray, v):
    b[0] = v
    b[1] = v >> 8
    return b


def put_uint32(b: bytearray, v):
    b[0] = v
    b[1] = v >> 8
    b[2] = v >> 16
    b[3] = v >> 24
    return b

