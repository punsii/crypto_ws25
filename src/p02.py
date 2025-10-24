import random

import pytest
from sage.all import gcd


def rfc_mod(a: int, q: int) -> int:
    #  Slow as f***
    # while a > q:
    #     a = a - q
    # return a
    return a % q


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


def e_ggT(a: int, b: int) -> int:

    return 0


def coprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1


def rfc_mod_inv(a: int, q: int) -> int:
    return 0


def rfc_mod_div(a: int, b: int, q: int) -> int:
    return 0


def stein(a: int, b: int) -> int:
    return 0


def run_test():
    pytest.main(["./src/p02_test.py", "-vv", "--durations=0"])


run_test()
