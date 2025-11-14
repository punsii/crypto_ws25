import pytest
from modular import rfc_mod, rfc_mod_inv
from sage.all import GF, EllipticCurve

# secp256k1 ist eine Standard Kurve
#
# siehe https://en.bitcoin.it/wiki/Secp256k1

# Definieren Sie hier die Parameter a, b, sowie p um die richtige Kurve zu
# erstellen.

p = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F", base=16)
a = int("0000000000000000000000000000000000000000000000000000000000000000", base=16)
b = int("0000000000000000000000000000000000000000000000000000000000000007", base=16)


# Tragen Sie hier die Koordinaten des bei SECG/Bitcoin verwendeten Generators
# ein

GenCoords = (
    # G in compressed form = 02 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798
    # uncompressed: Prefix 04  ??
    int("79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798", base=16),
    int("483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8", base=16),
)


# Definieren Sie hier die korrekten Parameter für die secp256k1
# Kurve. Informieren Sie sich dazu unter Sage zu `EllipticCurve`

secp256k1 = EllipticCurve(GF(p), [0, 0, 0, a, b])

# Wenn die Kurve und die Koordinaten des Generators korrekt definiert ist,
# entfernen Sie den Kommentar der folgenden Definition.

G = secp256k1(GenCoords)


def ec_add(P, Q):
    """EC Punktaddition von P und Q, gibt P + Q als Ergebnis zurück.

    Implementieren Sie die Addition von Punkten auf elliptischen Kurven so wie
    in RFC6090 Section 3 definiert. Gehen Sie davon aus, dass P und Q Punkte der
    selben Kurve sind.

    mit P.curve() bekomment Sie die Kurve als Objekt auf der der Punkt P liegt

    mit P.is_zero() können Sie abfragen, ob ein Punkt der Point at infinity ist

    Mit `int(P[0]) / int(P[1])` können Sie die x / y Koordinate als integer Wert
    bekommen.

    Wenn Sie eine x / y Koordinate haben und eine Kurve C, dann können Sie mit
    `C(x,y)` einen Punkt konstruieren. Mit `C(0, 1, 0)` bekommen Sie das
    neutrale Element, den Point at Infinity.
    """
    (x1, y1) = (int(P[0]), int(P[1]))
    (x2, y2) = (int(Q[0]), int(Q[1]))

    C = P.curve()
    N = C(0, 1, 0)

    if P.is_zero():
        return Q
    if Q.is_zero():
        return P
    if (P != Q and x1 == x2) or (P == Q and y1 == 0):
        return N

    if P != Q and x1 != x2:
        x3 = rfc_mod(((y2 - y1) * rfc_mod_inv(x2 - x1, p)) ** 2 - x1 - x2, p)
        y3 = rfc_mod((x1 - x3) * (y2 - y1) * rfc_mod_inv(x2 - x1, p) - y1, p)
    else:  # P == Q and y1 != 0
        x3 = rfc_mod(((3 * x1**2 + a) * rfc_mod_inv(2 * y1, p)) ** 2 - 2 * x1, p)
        y3 = rfc_mod((x1 - x3) * (3 * x1**2 + a) * rfc_mod_inv(2 * y1, p) - y1, p)
    return C(x3, y3)


def ec_inv(P):
    """EC Punkt Inverses

    Implementieren Sie die additive Invertierung eines gegebenen Punktes `P`
    einer elliptischen Kurve.
    """

    pass


def ec_mul(n, P):
    """EC Skalarmultiplikation

    Implementieren Sie eine skalare Multiplikation eines Punktes `P` mit einer
    gegebenen ganzen Zahl `n`. Nutzen die das double-and-add Verfahren mit der
    Komplexität O(log(n)).
    """

    pass


def eulerCriterion(n, p):
    """Euler Kriterium

    Das Euler Kriterium entscheidet, ob eine Zahl `n` ein quadratischer Rest
    modulo `p` ist.
    """

    pass


def getQS(p):
    """Zerlegung von `p - 1 = 2^S * Q`

    Für den Algorithmus von Tonelli wird für die Primzahl `p > 2` die Zahl `p -
    1` in der Form `p - 1 = 2^S * Q` dargestellt.
    """

    return (None, None)


def findNonResidue(p):
    """Findet beliebigen nicht-quadratischen Rest in GF(p)"""

    pass


def tonelli(n, p):
    """Wenn `n` ein quadratischer Rest modulo `p` ist, wird die Lösung
    zurückgegeben.

    Die Funktion liefert `None` wenn `n` kein quadratischer Rest ist

    Ansonsten wird (a, b) zurückgegeben mit `a  in GF(p)`, `b in GF(p)` sowie
    `a^2 = n (mod p)` und `b^2 = n (mod p)`.
    """

    pass


def ec_mul_ml(n, P):
    """EC Skalarmultiplikation mit Montgomery Ladder

    Implementieren Sie eine skalare Multiplikation eines Punktes `P` mit einer
    gegebenen ganzen Zahl `n`. Nutzen die das Verfahren der Montgomery ladder mit
    Komplexität O(log(n)) und konstanter Dauer pro Schritt.

    Mit `Integer(100).bits()` bekommen Sie eine Liste von bits einer gegebenen
    ganzen Zahl.
    """

    pass


def uncompress_point(p_c):
    """Returns the uncompressed version of given point

    The point is given as string with a prefix of 0x02 or 0x03, assume it's on
    secp256k1, i.e., use a, b, p as above
    """

    pass
