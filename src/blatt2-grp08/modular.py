from typing import Tuple

import pytest
from sage.all import gcd


def rfc_mod(a: int, q: int) -> int:
    return a - (a // q) * q


def rfc_mod_add(a: int, b: int, q: int) -> int:
    a = rfc_mod(a, q)
    b = rfc_mod(b, q)
    return a + b if a + b < q else a + b - q


def rfc_mod_sub(a: int, b: int, q: int) -> int:
    a = rfc_mod(a, q)
    b = rfc_mod(b, q)
    return a - b if a - b >= 0 else a - b + q


def rfc_mod_mul(a: int, b: int, q: int) -> int:
    a = rfc_mod(a, q)
    b = rfc_mod(b, q)
    return rfc_mod(a * b, q)


# returns (a0', b0', ggt(a, b))
def e_ggT(a: int, b: int) -> Tuple[int, int, int]:
    # Falls b = 0: (1, 0, a)
    if b == 0:
        return (1, 0, a)
    # Falls b != 0:
    else:
        #     1. Schritt:
        #     berechne (a0', b0', g) F= eggT(b, a mod b)
        (a0, b0, g) = e_ggT(b, a % b)
        #     2. Schritt:
        #     das gesuchte Ergebnis ist (b0', a0' - a / b * b0', g)
        return (b0, a0 - a // b * b0, g)


def coprime(a: int, b: int) -> bool:
    (_, _, ggt) = e_ggT(a, b)
    return ggt == 1


def rfc_mod_inv(a: int, q: int) -> int:
    (a_s, _, ggt) = e_ggT(a, q)
    assert ggt == 1
    return rfc_mod(a_s, q)


def rfc_mod_div(a: int, b: int, q: int) -> int:
    return rfc_mod_mul(a, rfc_mod_inv(b, q), q)


def stein(a: int, b: int) -> int:
    if b > a:
        return stein(b, a)
    if b == 0:
        return a

    a_even = not a & 1
    b_even = not b & 1

    if a_even and b_even:
        # ggT(a, b) = 2 · ggT(a/2, b/2), falls a und b gerade sind
        return 2 * stein(a >> 1, b >> 1)
    elif a_even and not b_even:
        # ggT(a/2, b), falls a gerade ist und b ungerade
        return stein(a >> 1, b)
    elif not a_even and b_even:
        # ggT(a, b/2), falls a ungerade ist und b gerade
        return stein(a, b >> 1)
    else:
        # ggT((a − b)/2, b), falls a und b ungerade sind
        assert not a_even and not b_even
        return stein((a - b) >> 1, b)


def run_test():
    pytest.main(["./test_mod.py", "-vv", "--durations=0"])


run_test()
