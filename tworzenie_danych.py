import random as r
import json
from math import log, sqrt, cos, sin, pi

# liczebnnosc zbiorow
n = 100

#rozklad normlany
def roz_normalny():
    srodek = 0
    odchylenie = 1
    normalny = []
    for i in range(n):
        normalny.append(r.normalvariate(srodek, odchylenie))
    return normalny

# losowanie
with open("r_normalny.json", 'w') as f:
    json.dump(roz_normalny(), f)

# rozklad plaski
def roz_plaski():
    a = 0 # poczatek
    b = 1 # koniec
    plaski = []
    for i in range(n):
        plaski.append(r.uniform(a, b))
    return plaski

# losowanie
with open('r_plaski.json', 'w') as f:
    json.dump(roz_plaski(), f)

# rozklad plaski pseudolosowy
def lcg():
    x = 123         # seed
    a = 22695477    # multiplier
    c = 1           # increment
    m = 2 ** 32     # modulus
    ran = []
    for i in range(n):
        x = (a * x + c) % m
        ran.append(x*2.32830643653870e-10)
    return ran

# losowanie
with open('r_lcg.json', 'w') as f:
    json.dump(lcg(), f)

# rozklad normalny pseudoloswy
def box_m(plaski):
    ran = []
    for i in range(len(plaski)//2):
        R = sqrt(-2*log(plaski[i*2]))
        O = 2*pi*plaski[i*2+1]
        ran.append(R*cos(O))
        ran.append(R*sin(O))
    return ran

# losowanie
with open('r_box.json', 'w') as f:
    json.dump(box_m(lcg()), f)