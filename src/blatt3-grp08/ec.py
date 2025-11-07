from sage.all import *

from modular import rfc_mod_inv

# secp256k1 ist eine Standard Kurve
#
# siehe https://en.bitcoin.it/wiki/Secp256k1

# Definieren Sie hier die Parameter a, b, sowie p um die richtige Kurve zu
# erstellen.

p = None
a = None
b = None


# Tragen Sie hier die Koordinaten des bei SECG/Bitcoin verwendeten Generators
# ein

GenCoords = (
    None,
    None,
)


# Definieren Sie hier die korrekten Parameter für die secp256k1
# Kurve. Informieren Sie sich dazu unter Sage zu `EllipticCurve`

secp256k1 = EllipticCurve(GF(p), [0, 0, 0, a, b])

# Wenn die Kurve und die Koordinaten des Generators korrekt definiert ist,
# entfernen Sie den Kommentar der folgenden Definition.

# G = secp256k1(GenCoords)


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

    return None

def ec_inv(P):
    """EC Punkt Inverses

    Implementieren Sie die additive Invertierung eines gegebenen Punktes `P`
    einer elliptischen Kurve.
    """

    return None


def ec_mul(n, P):
    """EC Skalarmultiplikation

    Implementieren Sie eine skalare Multiplikation eines Punktes `P` mit einer
    gegebenen ganzen Zahl `n`. Nutzen die das double-and-add Verfahren mit der
    Komplexität O(log(n)).
    """

    return None



def eulerCriterion(n, p):
    """Euler Kriterium

    Das Euler Kriterium entscheidet, ob eine Zahl `n` ein quadratischer Rest
    modulo `p` ist.
    """

    return None


def getQS(p):
    """Zerlegung von `p - 1 = 2^S * Q`

    Für den Algorithmus von Tonelli wird für die Primzahl `p > 2` die Zahl `p -
    1` in der Form `p - 1 = 2^S * Q` dargestellt.
    """

    return (None, None)


def findNonResidue(p):
    """Findet beliebigen nicht-quadratischen Rest in GF(p)
    """

    return None


def tonelli(n, p):
    """Wenn `n` ein quadratischer Rest modulo `p` ist, wird die Lösung
    zurückgegeben.

    Die Funktion liefert `None` wenn `n` kein quadratischer Rest ist

    Ansonsten wird (a, b) zurückgegeben mit `a\in GF(p)`, `b\in GF(p)` sowie
    `a^2 = n (mod p)` und `b^2 = n (mod p)`.
    """

    return None


def ec_mul_ml(n, P):
    """EC Skalarmultiplikation mit Montgomery Ladder

    Implementieren Sie eine skalare Multiplikation eines Punktes `P` mit einer
    gegebenen ganzen Zahl `n`. Nutzen die das Verfahren der Montgomery ladder mit
    Komplexität O(log(n)) und konstanter Dauer pro Schritt.

    Mit `Integer(100).bits()` bekommen Sie eine Liste von bits einer gegebenen
    ganzen Zahl.
    """

    return None


def uncompress_point(p_c):
    """Returns the uncompressed version of given point

    The point is given as string with a prefix of 0x02 or 0x03, assume it's on
    secp256k1, i.e., use a, b, p as above
    """

    return None
