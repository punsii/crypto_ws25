import random

import pytest
from sage.all import QQ, PolynomialRing


def main():
    secret = 12345

    polynom = createSecretPolynom(secret, 3, 1, 100)

    print(polynom)
    # createSecretPolynom(secret, 2, 3)


def createSecretPolynom(secret, n, minVal, maxVal):
    points = [(0, secret)]

    curve_values = random.sample(range(minVal, maxVal), n + 1)
    points.extend([(i, curve_values[i]) for i in range(1, n)])

    R = PolynomialRing(QQ, "x")
    return R.lagrange_polynomial(points)


def createSecretSharing(secret, n, m):
    pass
    # polynome = createSecretPolynom(secret, n, 1, 10)
    # for i in range(n):
    #     print(i)
    # olynom = R.lagrange_polynomial([(0, 1), (1, 2), (1, 2)])


def restoreSecret(interpolationsPunkte):
    pass


def run_test():
    pytest.main(["./src/p01.py"])


if __name__ == "__main__":
    main()
