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
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def kysy_luku(viesti: str):
    while True:
        try:
            vastaus = int(input(viesti))
            return vastaus
        except:
            continue

# Nethack-standardi: 77*19
L = Luolasto(19, 77)
K = KaytavanKaivaja(L)
etsija = KomponenttienEtsija(L)
komennot = ['1: uusi luolasto',
            '2: bsp rooms (jyrää tämänhetkisen luolaston)',
            '3: drunkard\'s walk',
            '4: basic directional dungeon',
            '5: yhdistä komponentit',
            't: suorituskykytesti (kestää muutaman minuutin, ei kerro kauheasti)',
            'q: lopeta']

while True:
    cls()
    etsija.etsi_komponentit()
    L.nayta()
    if len(L.komponentit) > 1:
        print(f'{len(L.komponentit)} yhtenäistä komponenttia')
    for komento in komennot[:-3]:
        print(komento)

    # komponenttien yhdistäminen järkevää vain jos niitä on useampia
    if len(L.komponentit) > 1:
        print(komennot[4])

    print(komennot[-2])
    print(komennot[-1])


    komento = input()
    if komento not in ['1', '2', '3', '4', '5', 't', 'q']:
        continue

    if komento == 'q':
        exit()

    if komento == '1':  # uusi luolasto
        cls()

        leveys = kysy_luku('luolaston leveys: ')
        korkeus = kysy_luku('luolaston korkeus: ')

        L = Luolasto(korkeus, leveys)
        K = KaytavanKaivaja(L)
        etsija = KomponenttienEtsija(L)

    if komento == '2':  # bsp
        huoneiden_maara = kysy_luku('huoneita vähintään: ')

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

        tavoite = kysy_luku('kaivamistavoite, % luolastosta (esim. 30): ')
        elinika = kysy_luku('kaivajan elinikä (esim. 50): ')

        visualisointi = input('visualisointi k/e: ')
        cls()
        drunkard(L, tavoite, elinika, visualisointi=='k')

    if komento == '4':  # directional dungeon
        cls()
        L.nayta()
        mutkaisuus = kysy_luku('käytävän mutkaisuus (0-100): ')
        vaihtelu = kysy_luku('leveyden vaihtelu (0-100): ')
        suunta = input('aloitusreuna o/v: ')
        visualisointi = input('visualisointi k/e: ')
        cls()
        suunnattu_luola(L, 3, mutkaisuus, vaihtelu, suunta=='v', visualisointi=='k')

    if komento == '5':  # yhdistä komponentit
        if len(L.komponentit) >= 1:
            visualisointi = input('visualisointi k/e: ')
            cls()

            alku = time()

            for i in range(1, len(L.komponentit)):
                lahto = L.komponentit[i].kohderuutu
                kohde = L.komponentit[i-1].kohderuutu
                K.kaiva_kaytava(lahto[0], lahto[1], kohde[0], kohde[1], None, visualisointi=='k')

            loppu = time()
            if not visualisointi == 'k':
                print(f'valmis, aikaa meni {loppu-alku:.03f} sekuntia')
                sleep(2)

            etsija.etsi_komponentit()
            if len(L.komponentit) != 1:
                print('jotain meni vikaan')
                sleep(3)

    if komento == 't':  # suorituskykytestit
        L = Luolasto(19,77)
        K = KaytavanKaivaja(L)
        etsija = KomponenttienEtsija(L)

        # print('luodaan 100 luolastoa (77*19), bsp ilman käytäviä')

        # alku = time()

        # for i in range(100):
        #     L.tayta()
        #     bsp(L, 0, 7)
        #     # K.kaiva_kaytavat(False)

        # loppu = time()

        # print(f'bsp: {loppu-alku} s.')

        for koko in [(50,50), (100,50), (100,100), (200,100), (200,200)]:
            print(f'luodaan 50 luolastoa ({koko[0]}*{koko[1]}), bsp + käytävät')

            L = Luolasto(koko[0], koko[1])
            K = KaytavanKaivaja(L)

            alku = time()

            for _ in range(50):
                L.tayta()
                bsp(L, 0, 7)
                K.kaiva_kaytavat(False)

            loppu = time()

            print(f'aika: {loppu-alku} s.')

        # print('luodaan 100 luolastoa (77*19), drunkard, ei käytäviä')

        # alku = time()

        # for i in range(100):
        #     L.tayta()
        #     drunkard(L, 30, 10, False)
        #     # etsija.etsi_komponentit()
        #     # for i in range(1, len(L.komponentit)):
        #     #     lahto = L.komponentit[i].kohderuutu
        #     #     kohde = L.komponentit[i-1].kohderuutu
        #         # print(f'käytävä {i+1}')
        #         # K.kaiva_kaytava(lahto[0], lahto[1], kohde[0], kohde[1], None, False)


        # loppu = time()

        # print(f'drunkard: {loppu-alku} s.')
        
        # print('luodaan 100 luolastoa (77*19), drunkard + käytävät')

        # alku = time()

        # for i in range(100):
        #     L.tayta()
        #     drunkard(L, 5, 10, False)
        #     etsija.etsi_komponentit()
        #     for i in range(1, len(L.komponentit)):
        #         lahto = L.komponentit[i].kohderuutu
        #         kohde = L.komponentit[i-1].kohderuutu
        #         # print(f'käytävä {i+1}')
        #         K.kaiva_kaytava(lahto[0], lahto[1], kohde[0], kohde[1], None, False)


        # loppu = time()

        # print(f'drunkard + käytävät: {loppu-alku} s.')
        sleep(20)