# Aufgabe 4 - ecDSA

Q: Zeigen Sie: wenn (r, s) eine valide Signatur für eine Nachricht M und ein Schlüsselpaar
(Qa, dA) ist, dann ist auch (r, −s mod n) auch eine valide Signatur. Dabei ist n gleich
der Ordnung der unterliegenden elliptischen Kurve.
Fügen Sie die Lösung zum Repository hinzu, z.B. als PDF

A: Um eine Signatur zu verifizieren muss der Punkt P auf der elliptischen Kurve berechnet werden.

P = u1 * g + u2 * Q_A

P = (H(M) * s^-1 mod n) * g + (r * s^-1 mod n) * Q_A

Durch Ersetzen von s durch (-s mod n) erhalten wir:

P' = (H(M) * ((-s mod n)^-1 mod n)) * g + (r * ((-s mod n)^-1 mod n)) * Q_A

Da gilt (-s)^-1 mod n = -(s^-1) mod n können wir wie folgt umformen:

P' = (H(M) * (-(s^-1) mod n)) * g + (r * (-(s^-1) mod n)) * Q_A

P' = -(H(M) * (s^-1) mod n) * g - (r * (s^-1) mod n) * Q_A

P' = -((H(M) * (s^-1) mod n) * g + (r * (s^-1) mod n) * Q_A)

Wir haben dadurch gezeigt, dass

P' = -P

P' = P(x, -y)

P'(x, y) = P(x, -y)

P'_x = P_x

P' kann nur dem neutralen Element entsprechen, wenn auch P dem neutralen Element entspricht.
Darüber hinaus ist für die Verifikation der Signatur lediglich die x-Koordinate des Punktes P relevant, daher bestätigt auch P' die Signatur.
