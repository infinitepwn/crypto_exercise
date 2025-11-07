from sage.all import *
from Crypto.Util.number import *
from secret import flag, p2, p3
from random import sample

assert flag.startswith(b'minihash{')
flag = flag[9:]

flag_length = len(flag)
assert flag_length % 6 == 0
part_length = flag_length // 6
flag = [flag[i:i+part_length] for i in range(0, flag_length, part_length)]


# Fermat
p = getPrime(512)
q = next_prime(p)
n1 = p * q
e = 0x10001
c1 = pow(bytes_to_long(flag[0]), e, n1)
print("Chal 1:")
print(f"{n1 = }")
print(f"{c1 = }")

# Pollard's p-1
p = p2
q = getPrime(256)
n2 = p * q
c2 = pow(bytes_to_long(flag[1]), e, n2)
print("Chal 2:")
print(f"{n2 = }")
print(f"{c2 = }")

# Williams' p+1
p = p3
q = getPrime(320)
n3 = p * q
c3 = pow(bytes_to_long(flag[2]), e, n3)
print("Chal 3:")
print(f"{n3 = }")
print(f"{c3 = }")

# Pollard rho
p = getPrime(40)
q = getPrime(512)
r = getPrime(512)
s = getPrime(40)
n4 = p * q * r * s
assert (p*s > bytes_to_long(flag[3]))
c4 = pow(bytes_to_long(flag[3]), e, n4)
print("Chal 4:")
print(f"{n4 = }")
print(f"{c4 = }")

#ecm
a = 52
b = 117
p, q = getPrime(400), getPrime(400)
n5 = p * q
Zp, Zq = Zmod(p), Zmod(q)
Ep, Eq = EllipticCurve(Zp, [a, b]), EllipticCurve(Zq, [a, b])
En = EllipticCurve(Zmod(n5), [a, b])
x = 521171314
y = crt([int(Ep.lift_x(Zp(x)).xy()[1]), int(Eq.lift_x(Zq(x)).xy()[1])], [p, q])

hint = Ep.order()*Eq.order()

c5 = pow(bytes_to_long(flag[4]), e, n5)
print("Chal 5:")
print(f"{n5 = }")
print(f"{c5 = }")
print(f"{y = }")
print(f"{hint = }")

#Qsieve
p, q = getPrime(1024), getPrime(1024)
n6 = p * q

B = [getPrime(100) for _ in range(4)]
Zp, Zq = Zmod(p), Zmod(q)
res = {}
for _ in range(20):
    X = 0
    while ((pow(X, (p-1)//2, p)!=1) or (pow(X, (q-1)//2, q)!=1)):
        X = 1
        exps = sample(range(0, 11), 4)
        for b, e in zip(B, exps):
            X *= b**e
    exps = tuple(exps)
    if exps in res: continue
    sqrt_xp = int(Zp(X).nth_root(2))
    sqrt_xq = int(Zq(X).nth_root(2))
    sqrt_x = crt([sqrt_xp, sqrt_xq], [p, q])
    res[exps] = (sqrt_x, X)
c6 = pow(bytes_to_long(flag[5]), e, n6)
print("Chal 6:")
print(f"{n6 = }")
print(f"{c6 = }")
print(f"{res = }")
