from ontology.core.transaction import Transaction


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


def serialize_unsigned(tx: Transaction):
    res = bytearray()
    res += write_byte(tx.version)
    res += write_byte(tx.tx_type)
    res += write_uint32(tx.nonce)
    res += write_uint64(tx.gas_price)
    res += write_uint64(tx.gas_limit)
    res+=

    '''
    if err := tx.Payer.Serialize(w); err != nil {
		return errors.NewDetailErr(err, errors.ErrNoCode, "[SerializeUnsigned], Transaction payer failed.")
	}
	//Payload
	if tx.Payload == nil {
		return errors.NewErr("Transaction Payload is nil.")
	}
	if err := tx.Payload.Serialize(w); err != nil {
		return errors.NewDetailErr(err, errors.ErrNoCode, "[SerializeUnsigned], Transaction payload failed.")
	}

	err := serialization.WriteVarUint(w, uint64(tx.attributes))
	if err != nil {
		return errors.NewDetailErr(err, errors.ErrNoCode, "[SerializeUnsigned], Transaction item txAttribute length serialization failed.")
	}

    '''
