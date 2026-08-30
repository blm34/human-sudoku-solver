ALL_DIGITS = 0b111111111


def digit_mask(digit: int) -> int:
    """The bit mask for the given digit."""
    return 1 << (digit - 1)
