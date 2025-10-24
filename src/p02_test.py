import random

from sage.all import gcd, randint

from .p02 import (coprime, rfc_mod, rfc_mod_add, rfc_mod_div, rfc_mod_inv,
                  rfc_mod_mul, rfc_mod_sub, stein)

num_tests = 10000
upper_bound = 2**128


def get_rands():
    """Generiere Zufallszahlen der Form

    p, q -- Zufallszahlen, können auch negativ oder 0 sein
    m    -- Zufallszahl > 0
    """

    m = randint(1, upper_bound)
    p = rfc_mod(randint(-upper_bound, upper_bound), m)
    q = rfc_mod(randint(-upper_bound, upper_bound), m)
    return (p, q, m)


def test_mod():
    """Test ob rfc_mod richtig arbeitet

    Es muss folgendes gelten: x == (x / y) * y + (x % y)
    """

    for i in range(num_tests):
        a = randint(1, 2**128)
        b = randint(1, 2**128)

        x = max(a, b)
        y = min(a, b)

        m = rfc_mod(x, y)

        assert x == (x // y) * y + m


def test_add():
    """Test der modularen Addition"""

    for i in range(num_tests):
        (a, b, p) = get_rands()

        assert ((a + b) % p) == rfc_mod_add(a, b, p)


def test_sub():
    """Test der modularen Subtraktion"""

    for i in range(num_tests):
        (a, b, p) = get_rands()

        assert ((a - b) % p) == rfc_mod_sub(a, b, p)


def test_mul():
    """Test der modularen Multiplikation"""

    for i in range(num_tests):
        (a, b, p) = get_rands()

        assert ((a * b) % p) == rfc_mod_mul(a, b, p)


def test_inv():
    """Test der modularen Inversen

    Es muss gelten, dass wenn a, p coprim sind, dann gilt auch
    a * inv(a) = 1  mod p
    """

    for i in range(num_tests):
        (a, _, p) = get_rands()
        while not (coprime(a, p) and p > 1):  # p == 1 does not really make
            # sense
            (a, _, p) = get_rands()

        assert rfc_mod_mul(a, rfc_mod_inv(a, p), p) == 1


def test_stein():
    """Test ob der Algorithmus von Stein den ggT berechnet"""

    for i in range(num_tests):
        (a, b, _) = get_rands()

        assert gcd(a, b) == stein(a, b)
