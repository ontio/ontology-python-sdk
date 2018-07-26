from ontology.vm.params_builder import ParamsBuilder
from ontology.vm.op_code import CHECKSIG
from ontology.crypto.Digest import Digest
import base58
from binascii import b2a_hex, a2b_hex

ADDR_LEN = 20  # the size of address should be 20 bytes

ont_contract_address = bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x01])
ong_contract_address = bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x02])
ont_id_contract_address = bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x03])
param_contract_address = bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x04])
auth_contract_address = bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x06])
governance_contract_address = bytearray(
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
     0x07])


class Address(object):
    __zero_size = 20
    __COIN_VERSION = b'\x17'

    def __init__(self, value):
        self.ZERO = value

    @staticmethod
    def toScriptHash(byte_script):
        return Digest.hash160(msg=byte_script, is_hex=True)

    @staticmethod
    def address_from_bytes_pubkey(public_key: bytes):
        builder = ParamsBuilder()
        builder.emit_push_byte_array(bytearray(public_key))
        builder.emit(CHECKSIG)
        addr = Address(Address.toScriptHash(builder.to_array()))
        return addr

    @staticmethod
    def address_from_hexstr_pubkey(public_key):
        return Address.address_from_bytes_pubkey((public_key))

    def to_base58(self):
        sb = Address.__COIN_VERSION + bytearray.fromhex(self.ZERO)
        c256 = Digest.hash256(sb)[0:4]
        outb = sb + bytearray(c256)
        return base58.b58encode(bytes(outb)).decode()

    def to_array(self):
        return a2b_hex(self.ZERO)

    @staticmethod
    def decodeBase58(addr):
        data = base58.b58decode(addr)
        if len(data) != 25:
            raise TypeError
        if data[0] != int.from_bytes(Address.__COIN_VERSION, "little"):
            raise TypeError
        checksum = Digest.hash256(data[0:21])
        if data[21:25] != checksum[0:4]:
            raise TypeError
        return Address(b2a_hex(data[1:21]))
