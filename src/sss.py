import random
from typing import List, Tuple

import pytest
from sage.all import QQ, PolynomialRing

random.seed(1234)
RING = PolynomialRing(QQ, "x")


def main():
    secret = 12345

    min_number_to_solve = 2
    number_of_shares = 10
    print(f"1.: {createSecretSharing(secret, min_number_to_solve, number_of_shares)=}")
    secretSharing = createSecretSharing(secret, min_number_to_solve, number_of_shares)
    shares = secretSharing[0:min_number_to_solve]
    recovered_secret = restoreSecret(shares)
    print(f"1.: {(recovered_secret)=}")

    min_number_to_solve = 5
    number_of_shares = 20
    print(f"2.: {createSecretSharing(secret, min_number_to_solve, number_of_shares)=}")
    secretSharing = createSecretSharing(secret, min_number_to_solve, number_of_shares)
    shares = secretSharing[0:min_number_to_solve]
    recovered_secret = restoreSecret(shares)
    print(f"2.: {(recovered_secret)=}")

    print("")


def createSecretPolynom(secret: int, minNumberToSolve: int, minVal: int, maxVal: int):
    points = [(0, secret)]

    curve_values = random.sample(range(minVal, maxVal), minNumberToSolve)
    points.extend([(i, curve_values[i]) for i in range(1, minNumberToSolve)])

    return RING.lagrange_polynomial(points)


def createSecretSharing(secret: int, min_number_to_solve: int, number_of_shares: int):
    MAX_VALUE = min_number_to_solve * 2**15
    polynome = createSecretPolynom(
        secret, min_number_to_solve, minVal=-MAX_VALUE, maxVal=MAX_VALUE
    )
    return [(i, polynome(i)) for i in range(1, number_of_shares + 1)]


def restoreSecret(interpolationsPunkte: List[Tuple[int, int]]):
    return RING.lagrange_polynomial(interpolationsPunkte)(0)


def test_secret_sharing():
    for i in range(1000):
        secret = random.randint(0, 2**15)
        min_number_to_solve = random.randint(2, 100)
        number_of_shares = random.randint(min_number_to_solve, min_number_to_solve + 10)

        secretSharing = createSecretSharing(
            secret, min_number_to_solve, number_of_shares
        )
        shares = secretSharing[0:min_number_to_solve]
        shares = random.sample(secretSharing, min_number_to_solve)

        recovered_secret = restoreSecret(shares)
        assert recovered_secret == secret
        print(i)


def test_too_few_shares():
    for _ in range(1000):
        secret = random.randint(0, 2**15)
        min_number_to_solve = random.randint(2, 100)
        number_of_shares = min_number_to_solve - 1

        secretSharing = createSecretSharing(
            secret, min_number_to_solve, number_of_shares
        )
        shares = secretSharing

        recovered_secret = restoreSecret(shares)
        assert recovered_secret != secret


def run_test():
    pytest.main(["./src/sss.py", "-vv", "--durations=0"])


if __name__ == "__main__":
    run_test()
    # main()
