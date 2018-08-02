from ontology.core.program import ProgramBuilder
from ontology.vm.params_builder import ParamsBuilder
from ontology.vm.op_code import CHECKSIG
from ontology.crypto.digest import Digest
import base58
from binascii import a2b_hex


class Address(object):
    __zero_size = 20
    __COIN_VERSION = b'\x17'

    def __init__(self, value: bytes):
        self.ZERO = value  # 20 bytes

    @staticmethod
    def to_script_hash(byte_script):
        return a2b_hex(Digest.hash160(msg=byte_script, is_hex=True))

    @staticmethod
    def address_from_bytes_pubkey(public_key: bytes):
        builder = ParamsBuilder()
        builder.emit_push_byte_array(bytearray(public_key))
        builder.emit(CHECKSIG)
        addr = Address(Address.to_script_hash(builder.to_array()))
        return addr

    @staticmethod
    def address_from_multi_pubKeys(m: int, pubkeys: []):
        return Address(Address.to_script_hash(ProgramBuilder.program_from_multi_pubkey(m, pubkeys)))

    def to_base58(self):
        sb = Address.__COIN_VERSION + self.ZERO
        c256 = Digest.hash256(sb)[0:4]
        outb = sb + bytearray(c256)
        return base58.b58encode(bytes(outb))

    def to_array(self):
        return self.ZERO

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
        return Address(data[1:21])
