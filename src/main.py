import os
from time import sleep
from algoritmit.drunkard import drunkard
from luokat.kaytavan_kaivaja import KaytavanKaivaja
from luokat.luolasto2 import Luolasto, Ruutu
from algoritmit.suunnattu_luola import suunnattu_luola
from algoritmit.bsp import bsp
from algoritmit.stilisointi import stilisoi

# Nethack-standardi: 77*19
# L = Luolasto(77, 19)



# drunkard(L, 20, 60)
# suunnattu_luola(L, 3, 65, 2, 1)
# suunnattu_luola(L, 3, 65, 2, -1)
# suunnattu_luola(L, 3, 65, 2, 1)
# suunnattu_luola(L, 3, 65, 2, -1)
# bsp(L)
# print('valmis luolasto:')
# L.nayta()
# print()
# stilisoi(L)

# L = Luolasto(19, 72)
# K = KaytavanKaivaja(L)
# drunkard(L, 30, 50, True)
# suunnattu_luola(L, 3, 65, 2, 1, True)
# suunnattu_luola(L, 3, 65, 2, -1, True)
# L.maarita_naapurit()
# L.etsi_seinat()
# sleep(2)
# print('\n'*20)

# L.nayta()
# print()

# L.maarita_naapurit()
# L.etsi_seinat()
# L.nayta()
# print()

# suunnattu_luola(L, 3, 65, 2, -1)
# L.maarita_naapurit()
# # L.nayta()
# L.etsi_seinat()
# L.nayta()
# print()
# bsp(L)
# L.maarita_naapurit()
# L.etsi_seinat()
# L.nayta()
# K.kaiva_kaytavat()

# ruutu = L.kartta[1][1]

def cls():
    os.system('clear')

L = Luolasto(19, 77)

komennot = ['1: uusi luolasto',
            '2: bsp rooms (jyrää tämänhetkisen luolaston)',
            '3: drunkard\'s walk',
            '4: basic directional dungeon']


while True:
    cls()
    L.maarita_naapurit()
    L.etsi_seinat()
    L.nayta()
    for komento in komennot:
        print(komento)
    
    komento = input()
    if komento not in ['1', '2', '3', '4']:
        continue

    if komento == '1':
        cls()
        leveys = min(int(input('luolaston leveys (max 77): ')), 77)
        korkeus = int(input('luolaston korkeus: (suositeltu max 19)'))
        L = Luolasto(korkeus, leveys)
        continue

    if komento == '2':
        bsp(L)
        continue

    if komento == '3':
        cls()
        L.nayta()
        tavoite = int(input('kaivamistavoite, % luolastosta (esim. 30): '))
        elinika = int(input('kaivajan elinikä (esim. 50): '))
        visualisointi = input('visualisointi k/e: ')
        cls()
        drunkard(L, tavoite, elinika, visualisointi=='k')
        continue

    if komento == '4':
        cls()
        L.nayta()
        mutkaisuus = int(input('käytävän mutkaisuus (0-100): '))
        vaihtelu = int(input('leveyden vaihtelu (0-100): '))
        suunta = input('aloitusreuna o/v: ')
        visualisointi = input('visualisointi k/e')
        cls()
        suunnattu_luola(L, 3, mutkaisuus, vaihtelu, suunta=='v', visualisointi=='k')