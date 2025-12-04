import ecdsa
from ecdsa import (deterministic_sign, generate_k, recover_key, secp256k1,
                   sign, verify)
from sage.all import randint

num_test = 500

msg1 = "Kryptographie ist klasse"
sig1 = (
    0x1EE3285C113BCFCE2DCCFE37BC2397F89CD650216F0FF3DC0ABEBA68A4A29813,
    0xCB0E3B1C1222ED814232C2D0486EA84F83B954481D5656082F667BA608ACAC34,
)

msg2 = "Schade, dass kein Haskell mehr genutzt wird!"
sig2 = (
    0xD15C1125E3D484EC38E1F3F22CBCD63DFB0BCDC3CD9CEA47806A3321BC06EE5C,
    0xDA721218E195131E43AA75D7AAA7B0B602721FC9A0CC7130F03FE0E9D6D768AD,
)


msg3 = "SageMath schein auch ganz gut zu sein!"
sig3 = (
    0xA0434D9E47F3C86235477C7B1AE6AE5D3442D49B1943C2B752A68E2A47E247C7,
    0x3B09D343C1A0020068E1D35EA2DFEFB56A055E0590C41E1470AFEF3255062838,
)


msg4 = "Und funktioniert anscheinend sogar gut als Jupyter Notebook"
sig4 = (
    0xA0434D9E47F3C86235477C7B1AE6AE5D3442D49B1943C2B752A68E2A47E247C7,
    0xA386C36BA006068505FB54A48FF5EFE9E0398A1F23D2E9B9667A4F7F8D8E16A2,
)


pubkey1 = (
    "0x7c43a2da60b9ffdf47ecec09c748f980832bfd3c0645d2fb428f5ee86fcea9d3",
    "0x8e7f1755547b31fd83ea1a21c4b7025d9deca1810a4051408831cd5a3a4fa8c",
    "0x1",
)

pubkey2 = (
    "0x34cc67e0a847c29b7e5fc44f81869f5b549356dcc0c54050958048730ea0389e",
    "0x7d950396500373a9cd111f4f8e041ace03a3cf5b5fbcc1c96a21226eed0d20b8",
    "0x1",
)

pubkey3 = (
    "0xfe8d1eb1bcb3432b1db5833ff5f2226d9cb5e65cee430558c18ed3a3c86ce1af",
    "0x7b158f244cd0de2134ac7c1d371cffbfae4db40801a2572e531c573cda9b5b4",
    "0x1",
)


def test_ecdsa():
    for i in range(0, num_test):

        # create random message
        msg = str(randint(1, 2**512))

        privkey = randint(1, 2**256)
        pubkey = privkey * ecdsa.G

        sig = sign(msg, privkey)
        assert verify(msg, sig, pubkey)


def test_recover():

    for i in range(0, num_test):

        # create random message
        msg1 = str(randint(1, 2**512))
        msg2 = str(randint(1, 2**512))
        k = randint(1, 2**256)

        privkey = randint(1, 2**256)
        pubkey = privkey * ecdsa.G

        sig1 = sign(msg1, privkey, k)
        sig2 = sign(msg2, privkey, k)

        assert privkey == recover_key(sig1, sig2, msg1, msg2)


def test_verify_testMessages():
    assert not verify(msg1, sig1, secp256k1(pubkey1[0], pubkey1[1], pubkey1[2]))
    assert verify(msg1, sig1, secp256k1(pubkey2[0], pubkey2[1], pubkey2[2]))
    assert not verify(msg1, sig1, secp256k1(pubkey3[0], pubkey3[1], pubkey3[2]))

    assert not verify(msg2, sig2, secp256k1(pubkey1[0], pubkey1[1], pubkey1[2]))
    assert verify(msg2, sig2, secp256k1(pubkey2[0], pubkey2[1], pubkey2[2]))
    assert not verify(msg2, sig2, secp256k1(pubkey3[0], pubkey3[1], pubkey3[2]))

    assert not verify(msg3, sig3, secp256k1(pubkey1[0], pubkey1[1], pubkey1[2]))
    assert not verify(msg3, sig3, secp256k1(pubkey2[0], pubkey2[1], pubkey2[2]))
    assert verify(msg3, sig3, secp256k1(pubkey3[0], pubkey3[1], pubkey3[2]))


def test_deterministic_sign():
    for i in range(0, num_test):
        # create random message
        msg = str(randint(1, 2**512))

        privkey = randint(1, 2**256)
        pubkey = privkey * ecdsa.G

        k = generate_k(msg, privkey)

        sig1 = sign(msg, privkey, k)
        sig2 = deterministic_sign(msg, privkey)
        assert verify(msg, sig1, pubkey)
        assert sig1 == sig2
