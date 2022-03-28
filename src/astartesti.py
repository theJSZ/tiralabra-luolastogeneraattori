import os
from time import sleep
from algoritmit.drunkard import drunkard
from luokat.kaytavan_kaivaja import KaytavanKaivaja
from luokat.luolasto2 import Luolasto, Ruutu
from algoritmit.suunnattu_luola import suunnattu_luola
from algoritmit.bsp import bsp
from algoritmit.stilisointi import stilisoi

def cls():
    os.system('clear')

L = Luolasto(19, 77)
K = KaytavanKaivaja(L)

bsp(L)
L.maarita_naapurit()
L.etsi_seinat()
L.nayta()