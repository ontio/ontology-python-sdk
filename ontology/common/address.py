from ontology.utils import util

ADDR_LEN = 20  # the size of address should be 20 bytes


def address_parse_from_bytes(addr: bytearray) -> bytearray:
    if len(addr) != ADDR_LEN:
        raise ValueError("[common]: address_parse_from_bytes error, len != 20")
    return addr  # [20]byte


def address_from_hex_string(s: str) -> bytearray:
    hx = util.hex_to_bytes(s)
    return address_parse_from_bytes(util.to_array_reverse(hx))


def address_from_base58(encoded: str) -> bytearray:
    pass  # TODO


ont_contract_address = address_parse_from_bytes(bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x01]))
ong_contract_address = address_parse_from_bytes(bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x02]))
ont_id_contract_address = address_parse_from_bytes(bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x03]))
param_contract_address = address_parse_from_bytes(bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x04]))
auth_contract_address = address_parse_from_bytes(bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x06]))
governance_contract_address = address_parse_from_bytes(bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x07]))

from functools import singledispatch
from binascii import a2b_hex

from Core.scripts.ParamsBuilder import ParamsBuilder
from Core.scripts.OpCode import CHECKSIG
from Crypto.Digest import Digest


class Address(object):
    __zero_size = 20
    __COIN_VERSION = b'0x17'

    def __init__(self, value):
        self.ZERO = value

    @staticmethod
    def toScriptHash(byte_script):
        return Digest.hash160(byte_msg=byte_script, is_hex=True)

    @staticmethod
    def address_from_bytes_pubkey(public_key: bytes):
        builder = ParamsBuilder()
        builder.emit_push_byte_array(bytearray(public_key))
        builder.emit(CHECKSIG)
        addr = Address(Address.toScriptHash(builder.get_builder()))
        return addr

    @staticmethod
    def address_from_hexstr_pubkey(public_key: str):
        return Address.address_from_bytes_pubkey(a2b_hex(public_key))
