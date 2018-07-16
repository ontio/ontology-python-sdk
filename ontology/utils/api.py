import json


def get_version(data: bytearray) -> str:
    return data.decode()


def get_block(data: bytearray):
    data=data.decode()
