import decimal
from unittest import TestCase

from toncenter.utils import raw_to_userfriendly, to_amount, to_nano, userfriendly_to_raw

USERFRIENDLY_ADDRESS = "UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0"
USERFRIENDLY_TEST_ONLY = "0QCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxS_-"
USERFRIENDLY_BOUNCEABLE = "EQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxcmx"
RAW_ADDRESS = "0:83ae019a23a8162beaa5cb0ebdc56668b2eac6c6ba51808812915b206a152dc5"


class TestRawToUserfriendly(TestCase):
    def test_non_bounceable(self):
        result = raw_to_userfriendly(RAW_ADDRESS)
        self.assertEqual(result, USERFRIENDLY_ADDRESS)

    def test_bounceable(self):
        result = raw_to_userfriendly(RAW_ADDRESS, is_bounceable=True)
        self.assertEqual(result, USERFRIENDLY_BOUNCEABLE)

    def test_test_only(self):
        result = raw_to_userfriendly(RAW_ADDRESS, is_test_only=True)
        self.assertEqual(result, USERFRIENDLY_TEST_ONLY)

    def test_roundtrip(self):
        friendly = raw_to_userfriendly(RAW_ADDRESS)
        raw = userfriendly_to_raw(friendly)
        self.assertEqual(raw, RAW_ADDRESS)

    def test_bounceable_roundtrip(self):
        friendly = raw_to_userfriendly(RAW_ADDRESS, is_bounceable=True)
        raw = userfriendly_to_raw(friendly)
        self.assertEqual(raw, RAW_ADDRESS)


class TestUserfriendlyToRaw(TestCase):
    def test_url_safe(self):
        result = userfriendly_to_raw(USERFRIENDLY_ADDRESS)
        self.assertEqual(result, RAW_ADDRESS)

    def test_bounceable(self):
        result = userfriendly_to_raw(USERFRIENDLY_BOUNCEABLE)
        self.assertEqual(result, RAW_ADDRESS)

    def test_test_only(self):
        result = userfriendly_to_raw(USERFRIENDLY_TEST_ONLY)
        self.assertEqual(result, RAW_ADDRESS)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            userfriendly_to_raw("AAAA")

    def test_invalid_crc(self):
        import base64

        data = base64.urlsafe_b64decode(USERFRIENDLY_ADDRESS)
        corrupted = data[:34] + b"\x00\x00"
        corrupted_b64 = base64.urlsafe_b64encode(corrupted).decode()
        with self.assertRaises(ValueError):
            userfriendly_to_raw(corrupted_b64)


class TestToNano(TestCase):
    def test_int(self):
        self.assertEqual(to_nano(1), 1_000_000_000)

    def test_float(self):
        self.assertEqual(to_nano(1.5), 1_500_000_000)

    def test_str(self):
        self.assertEqual(to_nano("0.123456789"), 123_456_789)

    def test_decimal(self):
        self.assertEqual(to_nano(decimal.Decimal("2.5")), 2_500_000_000)

    def test_zero(self):
        self.assertEqual(to_nano(0), 0)

    def test_custom_decimals(self):
        self.assertEqual(to_nano(1, decimals=6), 1_000_000)

    def test_negative_decimals_raises(self):
        with self.assertRaises(ValueError):
            to_nano(1, decimals=-1)

    def test_negative_value_raises(self):
        with self.assertRaises(ValueError):
            to_nano(-1)


class TestToAmount(TestCase):
    def test_basic(self):
        self.assertEqual(to_amount(1_000_000_000), decimal.Decimal("1"))

    def test_fractional(self):
        self.assertEqual(to_amount(1_500_000_000), decimal.Decimal("1.5"))

    def test_zero(self):
        self.assertEqual(to_amount(0), decimal.Decimal("0"))

    def test_custom_decimals(self):
        self.assertEqual(to_amount(1_000_000, decimals=6), decimal.Decimal("1"))

    def test_precision(self):
        result = to_amount(1_123_456_789, precision=2)
        self.assertEqual(result, decimal.Decimal("1.12"))

    def test_negative_decimals_raises(self):
        with self.assertRaises(ValueError):
            to_amount(1, decimals=-1)

    def test_negative_value_raises(self):
        with self.assertRaises(ValueError):
            to_amount(-1)

    def test_roundtrip(self):
        nano = to_nano("1.23")
        amount = to_amount(nano)
        self.assertEqual(amount, decimal.Decimal("1.23"))
