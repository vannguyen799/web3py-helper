from datetime import datetime
from eth_utils import is_address


def get_deadline(after_minutes=30):
    return int(datetime.now().timestamp() + 60 * after_minutes)


def parse_unit(amount, decimals):
    if decimals < 0:
        raise ValueError('decimal must >= 0')
    return int(amount * pow(10, decimals))


def to_byte32_address(address):
    if is_address(address):
        return f'0x000000000000000000000000{address[2:]}'
    else:
        raise ValueError(f'not valid address: got {address}')


def int_to_064x(value: int) -> str:
    return format(value, '064x')
