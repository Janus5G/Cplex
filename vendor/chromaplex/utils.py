"""Hjælpefunktioner til potenskonvertering."""

def number_to_exponent_remainder(n: int, base: int = 2) -> tuple:
    """Konverter et tal til eksponentiel repræsentation.

    Finder e og rest så: n = base^e + rest, hvor 0 <= rest < base^e.
    """
    if n < 0:
        raise ValueError("Kan ikke konvertere negative tal")
    if n == 0:
        return (0, 0)
    e = 0
    while base ** (e + 1) <= n:
        e += 1
    rest = n - base ** e
    return (e, rest)


def exponent_remainder_to_number(e: int, rest: int, base: int = 2) -> int:
    """Rekonstruer tal fra eksponentiel repræsentation."""
    return base ** e + rest


def find_optimal_exponent(value: int, max_exponent: int = 1000) -> int:
    """Find optimal eksponent for en given værdi."""
    e, _ = number_to_exponent_remainder(value)
    return min(e, max_exponent)
