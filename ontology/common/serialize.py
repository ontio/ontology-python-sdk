def write_byte(value):
    if isinstance(value, bytearray) or isinstance(value, bytes):
        return value
    elif isinstance(value, str):
        return value.encode()
    elif isinstance(value, int):
        return bytes([value])


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


def put_uint64(b: bytearray, v):
    b[0] = v
    b[1] = v >> 8
    b[2] = v >> 16
    b[3] = v >> 24
    b[4] = v >> 32
    b[5] = v >> 40
    b[6] = v >> 48
    b[7] = v >> 56
    return b


def write_uint16(val):
    b = bytearray(2)
    res = put_uint16(b, val)
    return res


def write_uint32(val):
    b = bytearray(4)
    res = put_uint32(b, val)
    return res


def write_uint64(val):
    b = bytearray(8)
    res = put_uint64(b, val)
    return res


def write_var_uint(value):
    buf = bytearray(1)
    if value < 0xFD:
        buf[0] = value
    elif value <= 0xFFFF:
        buf[0] = 0xFD
        temp = bytearray(2)
        buf += put_uint16(temp, value)
    elif value <= 0xFFFFFFFF:
        buf[0] = 0xFE
        temp = bytearray(4)
        buf += put_uint32(temp, value)
    else:
        buf[0] = 0xFF
        temp = bytearray(8)
        buf += put_uint64(temp, value)
    return buf


def serialize_unsigned(tx):
    res = bytearray()
    res += write_byte(tx.version)
    res += write_byte(tx.tx_type)
    res += write_uint32(tx.nonce)
    print('nonce')
    res += write_uint64(tx.gas_price)
    res += write_uint64(tx.gas_limit)
    res += tx.payer
    res += tx.payload
    res += write_var_uint(tx.attributes)
    return res


'''
payer = bytearray([196, 158, 110, 186, 14, 44, 238, 204, 26, 5, 15, 54, 183, 110, 158, 142, 32, 115, 243, 224])
res = Transaction(0, 209, 1531968852, 0, 0, payer, bytearray([7]), 0, 0, 0)
res = serialize_unsigned(res)
print(res)

b[0] is 117
b[1] is 13
b[2] is 80
b[3] is 91
'''

