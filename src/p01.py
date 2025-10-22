import math
import random

import pytest
from sage.all import is_square, next_prime

random.seed(1234)


def myFactor(n: int) -> tuple[int, int]:
    q = 2

    while q <= int(math.sqrt(n)):
        if (n % q) == 0:
            return (n // q, q)
        q += 1

    return (n, 1)


def myFactorPrime(n: int) -> tuple[int, int]:
    q = 2

    while q <= int(math.sqrt(n)):
        if (n % q) == 0:
            return (n // q, q)
        q = next_prime(q)

    return (n, 1)


def fermatFactor(n: int) -> tuple[int, int]:
    # Fermat will only work if both factors are primes and larger than 2
    for a in range(math.ceil(math.sqrt(n)), int(n / 3)):
        b_squared = a * a - n
        if is_square(b_squared):
            b = math.sqrt(b_squared)
            assert b == int(b)
            b = int(b)
            return (a + b, a - b)
    # Fermat will not work in all cases => no valid solution (may call myFactorPrime() instead)
    return (0, 0)


class TestMyFactor:
    def testSimpleResults(self):
        assert (11, 2) == myFactor(22)
        assert (13, 13) == myFactor(169)
        assert (13, 7) == myFactor(91)


class TestMyFactorPrime:
    def testSimpleResults(self):
        assert (11, 2) == myFactorPrime(22)
        assert (13, 13) == myFactorPrime(169)
        assert (13, 7) == myFactorPrime(91)

    def testPowersOfTwo(self):
        for i in range(4, 256):
            assert myFactorPrime(2**i) == (2 ** (i - 1), 2)

    def testMultiplyPrimesClose(self):
        p = next_prime(2**10)
        for _ in range(1000):
            q = next_prime(p)
            p = next_prime(q)
            assert myFactorPrime(p * q) == (p, q)

    def testMultiplyPrimesFar(self):
        q = 3
        for i in range(1, 200):
            q = next_prime(q)
            p = next_prime(q * i)
            assert myFactorPrime(p * q) == (p, q)


class TestFermatFactor:
    def testSimpleResults(self):
        assert (11, 7) == fermatFactor(77)
        assert (13, 13) == fermatFactor(169)
        assert (13, 7) == fermatFactor(91)

    def testMultiplyPrimesClose(self):
        p = next_prime(2**10)
        for _ in range(1000):
            q = next_prime(p)
            p = next_prime(q)
            assert fermatFactor(p * q) == (p, q)

    def testMultiplyPrimesFar(self):
        q = 3
        for i in range(1, 200):
            q = next_prime(q)
            p = next_prime(q * i)
            assert fermatFactor(p * q) == (p, q)

    def testSquaredPrimes(self):
        p = 3
        for _ in range(100):
            p = next_prime(p)
            assert fermatFactor(p * p) == (p, p)

    def testRandom(self):
        for _ in range(100):
            p = next_prime(random.randint(6000, 10000))
            q = next_prime(random.randint(3, p - 1000))
            assert fermatFactor(p * q) == (p, q)

    # Fermats algorithm can not work if p or q are even
    def noEvenFactors(self):
        for _ in range(100):
            p = next_prime(random.randint(6000, 10000)) + 1
            q = next_prime(random.randint(3, p - 1000))
            assert fermatFactor(p * q) == (0, 0)

        for _ in range(100):
            p = next_prime(random.randint(6000, 10000))
            q = next_prime(random.randint(3, p - 1000)) - 1
            assert fermatFactor(p * q) == (0, 0)

    # Fermats algorithm can not work if p or q are smaller than 3
    def noSmallFactors(self):
        q = 1
        for _ in range(100):
            p = next_prime(random.randint(1000, 10000))
            assert fermatFactor(p * q) == (0, 0)

        q = 2
        for _ in range(100):
            p = next_prime(random.randint(1000, 10000))
            assert fermatFactor(p * q) == (0, 0)


class TestEquivalence:
    def testEquivalence(self):
        for i in range(1, 10000):
            assert myFactor(i) == myFactorPrime(i)

    def testPrimeEquivalence(self):
        i = next_prime(1)
        for i in range(5000):
            i = next_prime(i)
            assert myFactor(i) == myFactorPrime(i)


def run_test():
    pytest.main(["./src/p01.py", "-vv", "--durations=0"])
    print(f"{fermatFactor(15241580725499173)=}")


run_test()
