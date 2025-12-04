import hashlib
import hmac
from typing import Tuple

from modular import rfc_mod, rfc_mod_add, rfc_mod_inv, rfc_mod_mul, rfc_mod_sub
from sage.all import GF, EllipticCurve, randint

HASHFUNC = hashlib.sha256

# Parameter für die secp256k1 Kurve
p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
a = 0
b = 7


# Affine Koordinaten des Standard Generators
GenCoords = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)


secp256k1 = EllipticCurve(GF(p), [0, 0, 0, a, b])

G = secp256k1(GenCoords)
n = G.order()
N = secp256k1(0, 1, 0)


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


def hash_string(msg: str) -> str:
    return HASHFUNC(msg.encode()).hexdigest()


def hash_string_to_int(msg: str) -> int:
    return int(hash_string(msg), 16)


def sign(msg, privkey, fixed_k=None) -> Tuple[int, int]:
    ## Generation of privkey already happended
    # 1. Alice generiert ein Element 𝑑𝐴 ∈ [1; 𝑛 − 1], den privaten Schlüssel
    # privkey = randint(1, n - 1)
    # 2. Alice berechnet ein Element der Kurve als 𝑄𝐴 = 𝑑𝐴 ⋅ 𝑔, den öffentlichen Schlüssel
    # pubkey = privkey * G

    hashed_message = hash_string_to_int(msg)
    while True:
        # Signatur
        # 1. Alice generiert eine kryptographisch sichere zufällige Zahl 𝑘 ∈ [1; 𝑛 − 1]

        if fixed_k:
            k = fixed_k
        else:
            k = randint(1, n - 1)
        # 2. Alice berechnet die Signatur (𝑟, 𝑠)
        # ▶ (𝑥, 𝑦) = 𝑘 ⋅ 𝑔
        (x, _, _) = k * G

        # ▶ 𝑟 ≡ 𝑥 mod 𝑛 falls 𝑟 = 0 gilt, dann zurück zu 1
        # ▶ 𝑠 ≡ 𝑘^−1 ⋅ (𝐻(𝑀) + 𝑟 ⋅ 𝑑𝐴) mod 𝑛 falls 𝑠 = 0 gilt, zurück zu 1
        r = rfc_mod(x, n)
        s = rfc_mod_mul(
            rfc_mod_inv(k, n), hashed_message + rfc_mod_mul(r, privkey, n), n
        )
        if r != 0 and s != 0:
            break
        if fixed_k:
            break

    return (r, s)


def verify(msg, sig, pubkey) -> bool:
    (r, s) = sig
    hashed_message = hash_string_to_int(msg)

    # prüft Bob, dass 𝑄𝐴 ≠ 𝑂 und 𝑛 ⋅ 𝑄𝐴 = 𝑂 gilt
    if pubkey == N or n * pubkey != N:
        return False

    # 2. prüft Bob ob 𝑟, 𝑠 ∈ [1; 𝑛 − 1] gilt
    if r < 1 or s < 1 or r > n - 1 or s > n - 1:
        return False

    # 3. berechnet Bob
    # ▶ 𝑢1 ≡ 𝐻(𝑀) ⋅ 𝑠^-1 mod 𝑛
    u1 = rfc_mod_mul(hashed_message, rfc_mod_inv(s, n), n)
    # ▶ 𝑢2 ≡ 𝑟 ⋅ 𝑠^−1 mod 𝑛
    u2 = rfc_mod_mul(r, rfc_mod_inv(s, n), n)
    # ▶ 𝑃 = 𝑢1 ⋅ 𝑔 + 𝑢2 ⋅ 𝑄𝐴
    P = u1 * G + u2 * pubkey

    # ▶ wenn 𝑃 = 𝑂 gilt, dann ist die Signatur falsch
    if P == N:
        return False

    # ▶ wenn 𝑃 = (𝑥, 𝑦) mit 𝑟 ≡ 𝑥 mod 𝑛, dann ist die Signatur valide
    (x, _, _) = P
    if r == rfc_mod(x, n):
        return True
    return False


def recover_key(sig1, sig2, msg1, msg2):
    """Berechne privaten Schlüssel, falls möglich"""
    assert sig1[0] == sig2[0]
    r = sig1[0]
    s1 = sig1[1]
    s2 = sig2[1]

    k = rfc_mod_mul(
        rfc_mod_sub(hash_string_to_int(msg1), hash_string_to_int(msg2), n),
        rfc_mod_inv(rfc_mod_sub(s1, s2, n), n),
        n,
    )

    (r, _, _) = k * G
    dA = rfc_mod_mul(
        rfc_mod_inv(r, n),
        rfc_mod_sub(rfc_mod_mul(k, s1, n), hash_string_to_int(msg1), n),
        n,
    )

    return dA


def _int2octets(x: int) -> bytes:
    """Convert integer x to a fixed-length big-endian octet string (rlen bytes)."""
    qlen = n.bit_length()
    rlen = (qlen + 7) // 8
    return x.to_bytes(rlen, "big")


def _bits2int(b: bytes) -> int:
    """Convert leftmost qlen bits of b to an integer."""
    qlen = n.bit_length()
    blen = len(b) * 8
    i = int.from_bytes(b, "big")
    if blen > qlen:
        i >>= blen - qlen
    return i


def _bits2octets(b: bytes) -> bytes:
    z1 = _bits2int(b)
    if z1 >= n:
        z1 -= n
    return _int2octets(z1)


def generate_k(msg: str, privkey: int) -> int:
    x = privkey
    qlen = n.bit_length()

    # a: h1 = H(m)
    h1 = HASHFUNC(msg.encode()).digest()

    hlen = HASHFUNC().digest_size * 8
    v_len = (hlen + 7) // 8  # == HASHFUNC().digest_size for common hashes

    # b: V = 0x01 ... 0x01
    V = b"\x01" * v_len

    # c: K = 0x00 ... 0x00
    K = b"\x00" * v_len

    # d: K = HMAC_K(V || 0x00 || int2octets(x) || bits2octets(h1))
    K = hmac.new(
        K,
        V + b"\x00" + _int2octets(x) + _bits2octets(h1),
        HASHFUNC,
    ).digest()

    # e: V = HMAC_K(V)
    V = hmac.new(K, V, HASHFUNC).digest()

    # f: K = HMAC_K(V || 0x01 || int2octets(x) || bits2octets(h1))
    K = hmac.new(
        K,
        V + b"\x01" + _int2octets(x) + _bits2octets(h1),
        HASHFUNC,
    ).digest()

    # g: V = HMAC_K(V)
    V = hmac.new(K, V, HASHFUNC).digest()

    # h: loop until we get a valid k in [1, q-1]
    while True:
        T = b""
        while len(T) * 8 < qlen:
            V = hmac.new(K, V, HASHFUNC).digest()
            T += V

        k = _bits2int(T)

        # check if k is suitable.
        if 1 <= k < n:
            # check that k does not result in an r value of 0
            (x, _, _) = k * G
            r = rfc_mod(x, n)
            if r != 0:
                return k

        # Otherwise, update K and V and try again
        K = hmac.new(K, V + b"\x00", HASHFUNC).digest()
        V = hmac.new(K, V, HASHFUNC).digest()


def deterministic_sign(msg, privkey) -> Tuple[int, int]:
    # almoste the same as in sign()
    hashed_message = hash_string_to_int(msg)
    while True:
        k = generate_k(msg, privkey)
        (x, _, _) = k * G

        # Checking that r != 0 happens in generate_k() already, but it does'nt hurt to check again
        r = rfc_mod(x, n)
        s = rfc_mod_mul(
            rfc_mod_inv(k, n), hashed_message + rfc_mod_mul(r, privkey, n), n
        )
        if r != 0 and s != 0:
            break

    return (r, s)


def testECDSA():

    n = G.order()
    dA = randint(1, n - 1)
    k = randint(1, n - 1)

    msg = str(randint(0, 2**256))

    pub_key = dA * G

    sig = sign(msg, dA)

    print("signature: ", sig)
    print("privkey: ", dA)
    print("k: ", k)
    print("order: ", n)
    print("order * G (must be neutral element): ", n * G)
    if verify(msg, sig, pub_key):
        print("verification: ok")
    else:
        print("verification: error")
