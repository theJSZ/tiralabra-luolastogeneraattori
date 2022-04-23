import random
from time import sleep
from luokat.huone import Huone
from luokat.luolasto import Luolasto

def jaa(alue: Huone, luolasto: Luolasto, alueet):
    """Jakaa annetun alueen kahdeksi uudeksi alueeksi,
    täyttää annettua listaa aina kun jako ei enää onnistu

    Args:
        alue (Huone): _description_
        luolasto (Luolasto): _description_
        alueet (list): _description_

    Returns:
        _type_: _description_
    """
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
    """Tarkistaa että luolastossa on tilaa halutulle huoneelle
    (emme halua huoneita kiinni toisiinsa)

    Args:
        huone (Huone): _description_
        luolasto (Luolasto): _description_

    Returns:
        bool: _description_
    """
    laajennettu_huone = Huone(huone.y-1, huone.x-1, huone.korkeus+2, huone.leveys+2)
    for y in range(laajennettu_huone.y, laajennettu_huone.y+laajennettu_huone.korkeus):
        for x in range(laajennettu_huone.x, laajennettu_huone.x+laajennettu_huone.leveys):
            if not luolasto.kartta[y][x].tyyppi == 'kallio':
                return False
    return True

def bsp(luolasto: Luolasto, yritys, huoneiden_maara):
    """Jakaa luolastoa pienempiin alueisiin. Yrittää luoda
    huoneen jokaiseen lopulliseen alueeseen. Jos ei onnistu
    sadalla yrityksellä luomaan luolastoon 7-11 huonetta,
    palauttaa False

    Args:
        luolasto (Luolasto): _description_
        yritys (_type_): _description_

    Returns:
        _type_: _description_
    """

    # aloitus koko luolaston kokoisesta alueesta
    h = Huone(1, 1, luolasto.korkeus-2, luolasto.leveys-2)
    luolasto.huoneet = []
    
    # tähän listaan kerätään rekursiivisen jaon lopputulos
    alueet = []
    
    jaa(h, luolasto, alueet)


    alustavat_huoneet = []
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
        if validi_huone(huone, luolasto):
            luolasto.kaiva_seinallinen_huone(huone)
            # n_huoneet += 1
            luolasto.huoneet.append(huone)

    # n_huoneet = len(luolasto.huoneet)
    if (len(luolasto.huoneet) >= huoneiden_maara): # and n_huoneet < 12):
        ok = True
    else:
        ok = False

    if not ok:
        luolasto.tayta()
        if yritys > 100:
            return False
        return bsp(luolasto, yritys+1, huoneiden_maara)
    return True
