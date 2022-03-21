from luokat.luolasto import Luolasto
from algoritmit.suunnattu_luola import suunnattu_luola
from algoritmit.stilisointi import stilisoi

# Nethack-standardi: 77*19
L = Luolasto(77, 19)

suunnattu_luola(L, 3, 65, 15, 1)
suunnattu_luola(L, 3, 65, 15, 1)
# suunnattu_luola(L, 3, 65, 15, -1)
# suunnattu_luola(L, 3, 65, 15, -1)

L.nayta()
print()
stilisoi(L)