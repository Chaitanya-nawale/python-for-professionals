from decimal import Decimal
from fractions import Fraction


def main():
    # ==========================
    # Basic Primitives
    # ==========================
    print("Hello from learn-python!")
    print(bool(108989))  # True
    print(bool(0))  # False
    print(bool(1) + bool(1) + bool(1))  # 3
    # These values are falsy: False, None, 0, "" (empty string),
    # empty lists, empty dictionaries, empty sets, and empty tuples
    print(bool(""), bool([]), bool({}), bool(None))  # False False False False
    # Truthiness is useful, but be careful when the distinction between None,
    # "", and False matters.

    print(int(True))  # 1
    print(float("234.897"))  # 234.897
    print(complex(2, 3))  # (2+3j) (complex)
    print(None)  # None (NoneType)

    # bytes for Network I/O, Binary Files, Cryptography
    print(bytes(b"hello"))  # b'hello' (bytes)

    # bytearray for Mutable data buffers, Packet/Image manipulation
    print(bytearray([65, 66, 67]))  # bytearray(b'ABC')

    # Creating a memoryview over a bytearray
    data = bytearray(b"Hello")
    view = memoryview(data)

    # A memoryview allows you to slice the data without copying it.
    # Note: data[0] will work and won't create a copy,
    # but slicing will create a new bytearray object.
    # Slicing with memoryview is more efficient for larger data.
    print(view[0])  # 72 (ASCII code for 'H')
    view[0] = 74  # Modify memory directly
    print(data)  # bytearray(b'Jello')

    # str for Textual Data, User Input, Logging
    print(str(100))  # '100' (str)

    # ==========================
    # Advanced Numerics
    # ==========================
    # Pass values as STRINGS to avoid float conversion errors before creation
    print(Decimal("0.1") + Decimal("0.2"))  # 0.3 (Decimal)
    print(Fraction(1, 3))  # 1/3 (Fraction)


if __name__ == "__main__":
    main()
