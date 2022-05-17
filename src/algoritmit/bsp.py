import random
from luokat.huone import Huone
from luokat.luolasto import Luolasto

def jaa(alue: Huone, luolasto: Luolasto, alueet):
    """Jakaa annetun alueen kahdeksi uudeksi alueeksi,
    tai täyttää annettua listaa jos aluetta ei enää jaeta

    Args:
        alue (Huone): _description_
        luolasto (Luolasto): _description_
        alueet (list): _description_

    Returns:
        _type_: _description_
    """
    korkeus = alue.korkeus
    leveys = alue.leveys

    # alue on riittävän pieni
    if korkeus < 8 or leveys < 15 or korkeus*leveys < 21:
        return alue

    # välillä saa tulla isompiakin
    if random.random() < 0.2:
        return alue

    jakosuunta = random.choice(['y', 'y', 'x'])

    if jakosuunta == 'y':
        lapsi1 = Huone(alue.y, alue.x, korkeus, leveys//2)
        lapsi2 = Huone(alue.y, alue.x+leveys//2, korkeus, leveys-leveys//2)
    else:
        lapsi1 = Huone(alue.y, alue.x, korkeus//2, leveys)
        lapsi2 = Huone(alue.y+korkeus//2, alue.x, korkeus-korkeus//2, leveys)

    alueet.append(jaa(lapsi1, luolasto, alueet))
    alueet.append(jaa(lapsi2, luolasto, alueet))

    return None

def validi_huone(huone: Huone, luolasto: Luolasto):
    """Tarkistaa että luolastossa on tilaa halutulle huoneelle
    (emme halua huoneita kiinni toisiinsa)
    """
    laajennettu_huone = Huone(huone.y-1, huone.x-1, huone.korkeus+2, huone.leveys+2)

    for ruutu_y in range(laajennettu_huone.y, laajennettu_huone.y+laajennettu_huone.korkeus):
        for ruutu_x in range(laajennettu_huone.x, laajennettu_huone.x+laajennettu_huone.leveys):

            if not ruutu_y in range(0,luolasto.korkeus) or not ruutu_x in range(0,luolasto.leveys):
                # huone kiinni reunassa
                return False
            if not luolasto.kartta[ruutu_y][ruutu_x].tyyppi == 'kallio':
                # huone kiinni toisessa huoneessa
                return False

    return True

def bsp(luolasto: Luolasto, yritys, huoneiden_maara):
    """Jakaa luolastoa pienempiin alueisiin. Yrittää luoda
    huoneen jokaiseen lopulliseen alueeseen. Jos ei onnistu
    sadalla yrityksellä luomaan luolastoon haluttua määrää huoneita,
    palauttaa False

    Args:
        luolasto (Luolasto): Luolasto
        yritys (int): monesko yritys menossa
        huoneiden_maara (int): kuinka monta vähintään halutaan

    Returns:
        boolean: onnistui tai ei
    """

    # aloitus koko luolaston kokoisesta alueesta
    alue = Huone(1, 1, luolasto.korkeus-2, luolasto.leveys-2)
    luolasto.huoneet = []

    # tähän listaan kerätään rekursiivisen jaon lopputulos
    alueet = []

    jaa(alue, luolasto, alueet)

    alueet = [alue for alue in alueet if alue is not None]

    alustavat_huoneet = []
    for alue in alueet:

        if alue.leveys >= 5 and alue.korkeus >= 5:
            # suunnitellaan alueelle huone hieman satunnaisesti
            huone_y = random.randint(0, alue.korkeus-5)
            huone_x = random.randint(0, alue.leveys-5)
            huone_korkeus = random.randint(5, alue.korkeus-huone_y)
            huone_leveys = random.randint(5, alue.leveys-huone_x)

            uusi_huone = Huone(alue.y+huone_y, alue.x+huone_x, huone_korkeus, huone_leveys)
            alustavat_huoneet.append(uusi_huone)

    for huone in alustavat_huoneet:  # kaivetaan jokainen suunniteltu huone jos ok
        if validi_huone(huone, luolasto):
            luolasto.kaiva_seinallinen_huone(huone)
            luolasto.huoneet.append(huone)

    if len(luolasto.huoneet) >= huoneiden_maara:
        return True  # saatiin luotua tarpeeksi huoneita

    # ei saatu tarpeeksi huoneita
    luolasto.tayta()

    if yritys > 100:
        return False

    return bsp(luolasto, yritys+1, huoneiden_maara)
