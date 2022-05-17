import random
import os
from time import sleep
from luokat.luolasto import Luolasto

def cls():
    """Tyhjentää terminaalin
    """
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def drunkard(luolasto: Luolasto, tavoite: int, elinika: int, visualisointi: bool = False):
    """Kaivaa satunnaisesta kohdasta aloittaen ja satunnaisesti edeten
    kunnes joko
    a: elinikä loppuu, jolloin jatkaa uudesta satunnaisesta kohdasta alkuperäisellä eliniällä
    b: tavoitteeksi annettu osuus jäljellä olevasta luolastosta on kaivettu, jolloin lopettaa

    Args:
        luolasto (Luolasto): Luolasto
        tavoite (int): %-osuus kaivamatta olevista ruuduista jotka halutaan kaivaa
        elinika (int): kuinka monta siirtoa yksi kaivaja elää
        visualisointi (bool, optional)
    """
    liikkeet = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    tavoite = max(tavoite, 1)

    kaivamatta = int((tavoite / 100) * luolasto.kaivamatta)

    while True:
        elinikaa_jaljella = elinika
        kaivettava_y = random.randint(1, luolasto.korkeus - 2)
        kaivettava_x = random.randint(1, luolasto.leveys - 2)

        while elinikaa_jaljella:
            if kaivamatta == 0:
                return

            elinikaa_jaljella -= 1

            if luolasto.kartta[kaivettava_y][kaivettava_x].tyyppi in ['kallio', 'seinä']:
                luolasto.kaiva(kaivettava_x, kaivettava_y)
                kaivamatta -= 1

            if visualisointi:
                luolasto.kartta[kaivettava_y][kaivettava_x].sisalto = 'o'
                luolasto.nayta()
                print(f'elinikää jäljellä {elinikaa_jaljella}, kaivamatta {kaivamatta}')
                sleep(0.05)
                luolasto.kartta[kaivettava_y][kaivettava_x].sisalto = None

            liike = random.choice(liikkeet)
            kaivettava_y += liike[0]
            kaivettava_x += liike[1]

            kaivettava_y = min(kaivettava_y, luolasto.korkeus-2)
            kaivettava_y = max(kaivettava_y, 1)
            kaivettava_x = min(kaivettava_x, luolasto.leveys-2)
            kaivettava_x = max(kaivettava_x, 1)
