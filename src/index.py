import os
from time import sleep
from algoritmit.drunkard import drunkard
from luokat.kaytavan_kaivaja import KaytavanKaivaja
from luokat.komponenttien_etsija import KomponenttienEtsija
from luokat.luolasto import Luolasto, Ruutu
from algoritmit.suunnattu_luola import suunnattu_luola
from algoritmit.bsp import bsp

def cls():
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
    if len(L.komponentit) > 1:
        print(komennot[-1])

    komento = input()
    if komento not in ['1', '2', '3', '4', '5']:
        continue

    if komento == '1':
        cls()
        leveys = min(int(input('luolaston leveys (max 77): ')), 77)
        korkeus = int(input('luolaston korkeus (suositeltu max 19): '))
        L = Luolasto(korkeus, leveys)
        K = KaytavanKaivaja(L)
        etsija = KomponenttienEtsija(L)

    if komento == '2':
        if bsp(L, 0):
            visualisointi = input('visualisointi k/e: ')
            K.kaiva_kaytavat(visualisointi == 'k')
        else:
            print('ei onnistu, kokeile isommalla luolastolla')
            sleep(3)

    if komento == '3':
        cls()
        L.nayta()
        tavoite = int(input('kaivamistavoite, % luolastosta (esim. 30): '))
        elinika = int(input('kaivajan elinikä (esim. 50): '))
        visualisointi = input('visualisointi k/e: ')
        cls()
        drunkard(L, tavoite, elinika, visualisointi=='k')

    if komento == '4':
        cls()
        L.nayta()
        mutkaisuus = int(input('käytävän mutkaisuus (0-100): '))
        vaihtelu = int(input('leveyden vaihtelu (0-100): '))
        suunta = input('aloitusreuna o/v: ')
        visualisointi = input('visualisointi k/e: ')
        cls()
        suunnattu_luola(L, 3, mutkaisuus, vaihtelu, suunta=='v', visualisointi=='k')

    if komento == '5':
        visualisointi = input('visualisointi k/e: ')
        cls()

        for i in range(1, len(L.komponentit)):
            lahto = L.komponentit[i].kohderuutu
            kohde = L.komponentit[i-1].kohderuutu
            K.kaiva_kaytava(lahto[0], lahto[1], kohde[0], kohde[1], None, visualisointi)
        
        etsija.etsi_komponentit()
        if not len(L.komponentit) == 1:
            print('jotain meni vikaan')
            sleep(3)

