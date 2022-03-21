from luokat.luolasto import Luolasto
from algoritmit.suunnattu_luola import suunnattu_luola

L = Luolasto()

suunnattu_luola(L, 3, 50, 2, 1)
suunnattu_luola(L, 3, 50, 2, 1)
suunnattu_luola(L, 3, 50, 2, -1)
suunnattu_luola(L, 3, 50, 2, -1)

L.nayta()