from ec import secp256k1, ec_add, ec_inv, ec_mul, ec_mul_ml, G

from sage.all import *

H = (
    55585044667560533658782103119277438379139238629741365435910370101297866015577,
    88461069942941367001333561487083397685726353902841367592581534658190054257721,
)

n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


num_test = 1000


def test_ec_def():
    """Check if H is on defined curve, i.e. curve is SECP256K1"""

    assert n == secp256k1.order()
    try:
        _ = secp256k1(H)
    except Exception:
        assert False, "H is a secp256k1 point but not on defined curve"


def rand_ec_point(C):

    n = randint(0, 2 ** 256)
    m = randint(0, 20)          # generate point at infinity with probability
                                # 1/20
    if m == 0:
        n = 0

    return n * G  # multiply random scalar with Generator


def test_ec_add():
    """Check if EC addition is the same as SageMath EC addition"""

    for i in range(num_test):

        P = rand_ec_point(secp256k1)
        Q = rand_ec_point(secp256k1)

        assert (P + Q) == ec_add(P, Q)


def test_ec_inv():
    """Check if EC inversion works"""

    Neutral = secp256k1(0, 1, 0)  # point at infinity
    for i in range(num_test):
        P = rand_ec_point(secp256k1)

        try:
            I = ec_inv(P)
        except Exception:
            raise Exception("inversion is not possible for %s" % P)
            assert False
        assert ec_add(P, ec_inv(P)) == Neutral


def test_ec_mul():
    """Check if double and add works"""

    for i in range(num_test):
        P = rand_ec_point(secp256k1)
        n = randint(0, 2**256)

        assert n * P == ec_mul(n, P)


def test_ec_mul_ml():
    """Check if Montgomery ladder multiplication works"""

    for i in range(num_test):
        P = rand_ec_point(secp256k1)
        n = randint(0, 2**256)

        assert n * P == ec_mul_ml(n, P)


P = "0x0379BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798"


def test_uncompress():

    assert ec_add(uncompress_point(P), G).is_zero()
