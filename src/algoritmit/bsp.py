import random
from time import sleep
from luokat.huone import Huone
from luokat.luolasto import Luolasto
from algoritmit.kaytava import kaytava

def jaa(alue: Huone, luolasto: Luolasto, alueet):
    y = alue.y
    x = alue.x
    korkeus = alue.korkeus
    leveys = alue.leveys

    if korkeus < 8 or leveys < 15 or korkeus*leveys < 21:
        return alue

    if random.random() < 0.2:
        return alue

    jakosuunta = random.choice(['y', 'y', 'x'])

    if jakosuunta == 'y':
        lapsi1 = Huone(y, x, korkeus, leveys//2)
        lapsi2 = Huone(y, x+leveys//2, korkeus, leveys-leveys//2)
    else:
        lapsi1 = Huone(y, x, korkeus//2, leveys)
        lapsi2 = Huone(y+korkeus//2, x, korkeus-korkeus//2, leveys)

    alueet.append(jaa(lapsi1, luolasto, alueet))
    alueet.append(jaa(lapsi2, luolasto, alueet))

def validi_huone(huone: Huone, luolasto: Luolasto):
    laajennettu_huone = Huone(huone.y-1, huone.x-1, huone.korkeus+2, huone.leveys+2)
    for y in range(laajennettu_huone.y, laajennettu_huone.y+laajennettu_huone.korkeus):
        for x in range(laajennettu_huone.x, laajennettu_huone.x+laajennettu_huone.leveys):
            if not luolasto.kartta[y][x].tyyppi == 'kallio':
                return False
    return True

def bsp(luolasto: Luolasto):
    h = Huone(1, 1, luolasto.korkeus-2, luolasto.leveys-2)
    alueet = []
    alustavat_huoneet = []
    n_huoneet = 0
    jaa(h, luolasto, alueet)
    for alue in alueet:
        if alue:
            if alue.leveys >= 5 and alue.korkeus >= 5:
                huone_y = random.randint(0, alue.korkeus-5)
                huone_x = random.randint(0, alue.leveys-5)
                huone_korkeus = random.randint(5, alue.korkeus-huone_y)
                huone_leveys = random.randint(5, alue.leveys-huone_x)

                uusi_huone = Huone(alue.y+huone_y, alue.x+huone_x, huone_korkeus, huone_leveys)
                alustavat_huoneet.append(uusi_huone)

    for huone in alustavat_huoneet:
        if huone.korkeus > 2*huone.leveys:
            huone = Huone(huone.y, huone.x, huone.korkeus // 2, huone.leveys)
        if validi_huone(huone, luolasto):
            luolasto.kaiva_seinallinen_huone(huone)
            n_huoneet += 1
            luolasto.huoneet.append(huone)

    ok = n_huoneet > 7 and n_huoneet < 12

    if not ok:
        luolasto.tayta()
        bsp(luolasto)

# 012345
# xxx...0
# xxx...1
# ......2
# ......3
# ......4