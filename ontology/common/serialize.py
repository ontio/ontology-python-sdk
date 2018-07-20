from ontology.io.BinaryWriter import BinaryWriter
from ontology.io.MemoryStream import StreamManager


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
    ms = StreamManager.GetStream()
    writer = BinaryWriter(ms)
    writer.WriteUInt8(tx.version)
    writer.WriteUInt8(tx.tx_type)
    writer.WriteUInt32(tx.nonce)
    writer.WriteUInt64(tx.gas_price)
    writer.WriteUInt64(tx.gas_limit)
    writer.WriteBytes(tx.payer)
    writer.WriteBytes(tx.payload)
    writer.WriteVarInt(tx.attributes)
    ms.flush()
    res = ms.ToArray()
    StreamManager.ReleaseStream(ms)
    return res
