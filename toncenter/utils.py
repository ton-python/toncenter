import base64
import binascii
import decimal
import struct

__all__ = [
    "raw_to_userfriendly",
    "to_amount",
    "to_nano",
    "userfriendly_to_raw",
]


_CRC16 = [
    0x0000,
    0x1021,
    0x2042,
    0x3063,
    0x4084,
    0x50A5,
    0x60C6,
    0x70E7,
    0x8108,
    0x9129,
    0xA14A,
    0xB16B,
    0xC18C,
    0xD1AD,
    0xE1CE,
    0xF1EF,
    0x1231,
    0x0210,
    0x3273,
    0x2252,
    0x52B5,
    0x4294,
    0x72F7,
    0x62D6,
    0x9339,
    0x8318,
    0xB37B,
    0xA35A,
    0xD3BD,
    0xC39C,
    0xF3FF,
    0xE3DE,
    0x2462,
    0x3443,
    0x0420,
    0x1401,
    0x64E6,
    0x74C7,
    0x44A4,
    0x5485,
    0xA56A,
    0xB54B,
    0x8528,
    0x9509,
    0xE5EE,
    0xF5CF,
    0xC5AC,
    0xD58D,
    0x3653,
    0x2672,
    0x1611,
    0x0630,
    0x76D7,
    0x66F6,
    0x5695,
    0x46B4,
    0xB75B,
    0xA77A,
    0x9719,
    0x8738,
    0xF7DF,
    0xE7FE,
    0xD79D,
    0xC7BC,
    0x48C4,
    0x58E5,
    0x6886,
    0x78A7,
    0x0840,
    0x1861,
    0x2802,
    0x3823,
    0xC9CC,
    0xD9ED,
    0xE98E,
    0xF9AF,
    0x8948,
    0x9969,
    0xA90A,
    0xB92B,
    0x5AF5,
    0x4AD4,
    0x7AB7,
    0x6A96,
    0x1A71,
    0x0A50,
    0x3A33,
    0x2A12,
    0xDBFD,
    0xCBDC,
    0xFBBF,
    0xEB9E,
    0x9B79,
    0x8B58,
    0xBB3B,
    0xAB1A,
    0x6CA6,
    0x7C87,
    0x4CE4,
    0x5CC5,
    0x2C22,
    0x3C03,
    0x0C60,
    0x1C41,
    0xEDAE,
    0xFD8F,
    0xCDEC,
    0xDDCD,
    0xAD2A,
    0xBD0B,
    0x8D68,
    0x9D49,
    0x7E97,
    0x6EB6,
    0x5ED5,
    0x4EF4,
    0x3E13,
    0x2E32,
    0x1E51,
    0x0E70,
    0xFF9F,
    0xEFBE,
    0xDFDD,
    0xCFFC,
    0xBF1B,
    0xAF3A,
    0x9F59,
    0x8F78,
    0x9188,
    0x81A9,
    0xB1CA,
    0xA1EB,
    0xD10C,
    0xC12D,
    0xF14E,
    0xE16F,
    0x1080,
    0x00A1,
    0x30C2,
    0x20E3,
    0x5004,
    0x4025,
    0x7046,
    0x6067,
    0x83B9,
    0x9398,
    0xA3FB,
    0xB3DA,
    0xC33D,
    0xD31C,
    0xE37F,
    0xF35E,
    0x02B1,
    0x1290,
    0x22F3,
    0x32D2,
    0x4235,
    0x5214,
    0x6277,
    0x7256,
    0xB5EA,
    0xA5CB,
    0x95A8,
    0x8589,
    0xF56E,
    0xE54F,
    0xD52C,
    0xC50D,
    0x34E2,
    0x24C3,
    0x14A0,
    0x0481,
    0x7466,
    0x6447,
    0x5424,
    0x4405,
    0xA7DB,
    0xB7FA,
    0x8799,
    0x97B8,
    0xE75F,
    0xF77E,
    0xC71D,
    0xD73C,
    0x26D3,
    0x36F2,
    0x0691,
    0x16B0,
    0x6657,
    0x7676,
    0x4615,
    0x5634,
    0xD94C,
    0xC96D,
    0xF90E,
    0xE92F,
    0x99C8,
    0x89E9,
    0xB98A,
    0xA9AB,
    0x5844,
    0x4865,
    0x7806,
    0x6827,
    0x18C0,
    0x08E1,
    0x3882,
    0x28A3,
    0xCB7D,
    0xDB5C,
    0xEB3F,
    0xFB1E,
    0x8BF9,
    0x9BD8,
    0xABBB,
    0xBB9A,
    0x4A75,
    0x5A54,
    0x6A37,
    0x7A16,
    0x0AF1,
    0x1AD0,
    0x2AB3,
    0x3A92,
    0xFD2E,
    0xED0F,
    0xDD6C,
    0xCD4D,
    0xBDAA,
    0xAD8B,
    0x9DE8,
    0x8DC9,
    0x7C26,
    0x6C07,
    0x5C64,
    0x4C45,
    0x3CA2,
    0x2C83,
    0x1CE0,
    0x0CC1,
    0xEF1F,
    0xFF3E,
    0xCF5D,
    0xDF7C,
    0xAF9B,
    0xBFBA,
    0x8FD9,
    0x9FF8,
    0x6E17,
    0x7E36,
    0x4E55,
    0x5E74,
    0x2E93,
    0x3EB2,
    0x0ED1,
    0x1EF0,
]


def _crc16_xmodem(data: bytes) -> int:
    crc = 0
    for b in data:
        crc = ((crc << 8) ^ _CRC16[(crc >> 8) ^ b]) & 0xFFFF
    return crc


def raw_to_userfriendly(
    address: str,
    is_bounceable: bool = False,
    is_url_safe: bool = True,
    is_test_only: bool = False,
) -> str:
    """Convert a raw address to user-friendly format.

    :param address: Raw address string in ``workchain_id:key`` format.
    :param is_bounceable: Whether the address is bounceable.
    :param is_url_safe: Use URL-safe base64 encoding.
    :param is_test_only: Mark the address as test-only.
    :return: User-friendly address string encoded in base64.
    """
    wc_str, key_hex = address.split(":")
    wc = int(wc_str)
    hash_part = bytes.fromhex(key_hex)

    tag = 0x11 if is_bounceable else 0x51
    if is_test_only:
        tag |= 0x80

    payload = struct.pack("Bb", tag, wc) + hash_part
    crc = _crc16_xmodem(payload)
    data = payload + struct.pack(">H", crc)

    if is_url_safe:
        return base64.urlsafe_b64encode(data).decode()
    return base64.b64encode(data).decode()


def userfriendly_to_raw(address: str) -> str:
    """Convert a user-friendly TON address to raw format.

    :param address: User-friendly address in base64.
    :return: The TON address in raw format.
    :raises ValueError: If the address has invalid length, CRC, or tag.
    """
    try:
        data = base64.urlsafe_b64decode(address)
    except (ValueError, binascii.Error):
        try:
            data = base64.b64decode(address)
        except (ValueError, binascii.Error) as exc:
            raise ValueError(f"Invalid base64 address: {address}") from exc

    if len(data) != 36:
        raise ValueError(f"Invalid user-friendly address length: {len(data)}")

    payload, crc_bytes = data[:34], data[34:36]
    crc_stored = struct.unpack(">H", crc_bytes)[0]
    crc_computed = _crc16_xmodem(payload)
    if crc_stored != crc_computed:
        raise ValueError("Invalid address CRC")

    tag = payload[0]
    if tag & 0x80:
        tag ^= 0x80
    if tag not in (0x11, 0x51):
        raise ValueError(f"Unknown address tag: {tag:#04x}")

    wc = struct.unpack("b", payload[1:2])[0]
    hash_part = payload[2:34].hex()

    return f"{wc}:{hash_part}"


def to_nano(
    value: int | float | str | decimal.Decimal,
    decimals: int = 9,
) -> int:
    """Convert human-readable token amount to the smallest units (nanotons).

    :param value: Amount in human-readable format.
    :param decimals: Decimal places (default: 9 for TON).
    :return: Amount in the smallest units.
    :raises ValueError: If decimals < 0 or result is negative.
    """
    if decimals < 0:
        raise ValueError("Decimals must be >= 0.")
    if isinstance(value, float):
        value = str(value)

    d = decimal.Decimal(value)
    factor = decimal.Decimal(10) ** decimals

    with decimal.localcontext() as ctx:
        ctx.prec = decimals + 30
        nano = (d * factor).quantize(decimal.Decimal(1), rounding=decimal.ROUND_DOWN)
    if nano < 0:
        raise ValueError("Value must be >= 0.")
    return int(nano)


def to_amount(
    value: int,
    decimals: int = 9,
    *,
    precision: int | None = None,
) -> decimal.Decimal:
    """Convert the smallest units (nanotons) to human-readable decimal amount.

    :param value: Amount in the smallest units.
    :param decimals: Decimal places (default: 9 for TON).
    :param precision: Round result down to this many decimal places.
    :return: Human-readable ``Decimal`` amount.
    :raises ValueError: If decimals < 0 or value < 0.
    """
    if decimals < 0:
        raise ValueError("Decimals must be >= 0.")
    if value < 0:
        raise ValueError("Value must be >= 0.")
    if value == 0:
        return decimal.Decimal(0)

    with decimal.localcontext() as ctx:
        ctx.prec = decimals + 30
        amount = decimal.Decimal(value) / (decimal.Decimal(10) ** decimals)
    if precision is not None:
        quant = decimal.Decimal(1) / (decimal.Decimal(10) ** precision)
        amount = amount.quantize(quant, rounding=decimal.ROUND_DOWN)
    return amount
