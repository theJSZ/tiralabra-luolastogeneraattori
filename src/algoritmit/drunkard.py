import random
import os
from time import sleep
from luokat.luolasto import Luolasto

def drunkard(luolasto: Luolasto, tavoite: int, elinika: int, visualisointi: bool = False):
    LIIKKEET = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    if tavoite < 1:
        tavoite = 1
    if tavoite > 90:
        tavoite = 90
    kaivamatta = int((tavoite / 100) * (luolasto.korkeus * luolasto.leveys))
    
    y = random.randint(1, luolasto.korkeus - 2)
    x = random.randint(1, luolasto.leveys - 2)
    validit_lahtopisteet = [(y, x)]    

    while True:
        elinikaa_jaljella = elinika
        y = random.randint(1, luolasto.korkeus - 2)
        x = random.randint(1, luolasto.leveys - 2)

        while elinikaa_jaljella:
            elinikaa_jaljella -= 1
            if luolasto.kartta[y][x].tyyppi in ['kallio', 'seinä']:
                luolasto.kaiva(x, y)
                kaivamatta -= 1
                if kaivamatta == 0:
                    return
            
            
            if visualisointi:
                # os.system('clear')
                luolasto.kartta[y][x].sisalto = 'o'
                luolasto.nayta()
                print(f'elinikää jäljellä {elinikaa_jaljella}, kaivamatta {kaivamatta}')
                sleep(0.05)
                luolasto.kartta[y][x].sisalto = None
                print('\n'*20)
            
            liike = random.choice(LIIKKEET)
            y += liike[0]
            x += liike[1]

            y = min(y, luolasto.korkeus-2)
            y = max(y, 1)
            x = min(x, luolasto.leveys-2)
            x = max(x, 1)