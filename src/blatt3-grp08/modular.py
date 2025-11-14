#!/usr/bin/env sage

from sage.all import gcd


def rfc_mod(a, q):

    b = (a // q) * q
    return a - b


def rfc_mod_add(a, b, q):

    if a + b < q:
        return a + b
    else:
        return a + b - q


def rfc_mod_sub(a, b, q):

    if a - b >= 0:
        return a - b
    else:
        return a - b + q


def rfc_mod_mul(a, b, q):

    return a * b - ((a * b) // q) * q


def e_ggT(a, b):
    if b == 0:
        return (1, 0, a)
    else:
        (a0, b0, g) = e_ggT(b, a % b)
        return (b0, a0 - (a // b) * b0, g)


def coprime(a, b):
    return gcd(a, b) == 1


def rfc_mod_inv(a, q):
    (r, _, _) = e_ggT(a, q)
    return r % q


def rfc_mod_div(a, b, q):

    return rfc_mod_mul(a, rfc_mod_inv(b, q), q)


def even(n):
    return n % 2 == 0


def stein(a, b):
    if b > a:
        return stein(b, a)
    else:
        if b == 0:
            return a
        elif even(a) and even(b):
            return 2 * stein(a // 2, b // 2)
        elif even(a):
            return stein(a // 2, b)
        elif even(b):
            return stein(a, b // 2)
        else:
            return stein((a - b) // 2, b)
