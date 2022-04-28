import os
from time import sleep, time
import sys
from algoritmit.bsp import bsp
from algoritmit.drunkard import drunkard
from algoritmit.suunnattu_luola import suunnattu_luola
from luokat.kaytavan_kaivaja import KaytavanKaivaja
from luokat.komponenttien_etsija import KomponenttienEtsija
from luokat.luolasto import Luolasto

sys.setrecursionlimit(100000)

def cls():
    """Tyhjentää terminaalin
    """
    os.system('clear')

# Nethack-standardi: 77*19
L = Luolasto(19, 77)
K = KaytavanKaivaja(L)
etsija = KomponenttienEtsija(L)
komennot = ['1: uusi luolasto',
            '2: bsp rooms (jyrää tämänhetkisen luolaston)',
            '3: drunkard\'s walk',
            '4: basic directional dungeon',
            '5: yhdistä komponentit']

while True:
    cls()
    etsija.etsi_komponentit()
    L.nayta()
    if len(L.komponentit) > 1:
        print(f'{len(L.komponentit)} yhtenäistä komponenttia')
    for komento in komennot[:-1]:
        print(komento)

    # komponenttien yhdistäminen järkevää vain jos niitä on useampia
    if len(L.komponentit) > 1:
        print(komennot[-1])

    komento = input()
    if komento not in ['1', '2', '3', '4', '5']:
        continue

    if komento == '1':  # uusi luolasto
        cls()
        leveys = min(int(input('luolaston leveys: ')), 7700)
        korkeus = int(input('luolaston korkeus: '))
        L = Luolasto(korkeus, leveys)
        K = KaytavanKaivaja(L)
        etsija = KomponenttienEtsija(L)

    if komento == '2':  # bsp
        huoneiden_maara = int(input('huoneita vähintään: '))
        
        alku = time()
        if bsp(L, 0, huoneiden_maara):
            loppu = time()
            print(f'bsp ok, aikaa meni {loppu-alku:.03f} sekuntia')
            visualisointi = input('visualisointi k/e: ')
            K.kaiva_kaytavat(visualisointi == 'k')
        else:  # 100 yritystä ei tuottanut kelvollista luolastoa
            print('ei onnistu, kokeile isommalla luolastolla')
            sleep(3)

    if komento == '3':  # drunkard
        cls()
        L.nayta()
        tavoite = int(input('kaivamistavoite, % luolastosta (esim. 30): '))
        elinika = int(input('kaivajan elinikä (esim. 50): '))
        visualisointi = input('visualisointi k/e: ')
        cls()
        drunkard(L, tavoite, elinika, visualisointi=='k')

    if komento == '4':  # directional dungeon
        cls()
        L.nayta()
        mutkaisuus = int(input('käytävän mutkaisuus (0-100): '))
        vaihtelu = int(input('leveyden vaihtelu (0-100): '))
        suunta = input('aloitusreuna o/v: ')
        visualisointi = input('visualisointi k/e: ')
        cls()
        suunnattu_luola(L, 3, mutkaisuus, vaihtelu, suunta=='v', visualisointi=='k')

    if komento == '5':  # yhdistä komponentit
        visualisointi = input('visualisointi k/e: ')
        cls()

        alku = time()

        for i in range(1, len(L.komponentit)):
            lahto = L.komponentit[i].kohderuutu
            kohde = L.komponentit[i-1].kohderuutu
            print(f'käytävä {i+1}')
            K.kaiva_kaytava(lahto[0], lahto[1], kohde[0], kohde[1], None, visualisointi=='k')

        loppu = time()
        if not visualisointi == 'k':
            print(f'valmis, aikaa meni {loppu-alku:.03f} sekuntia')
            sleep(2)

        etsija.etsi_komponentit()
        if len(L.komponentit) != 1:
            print('jotain meni vikaan')
            sleep(3)
