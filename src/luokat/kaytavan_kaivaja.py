from time import sleep
from luokat.luolasto2 import Luolasto
from heapq import heappop, heappush
import random
import os
class KaytavanKaivaja:
    def __init__(self, luolasto: Luolasto):
        self.luolasto = luolasto
        # painot = {'lattia': 0,
        #                'käytävä': 2,
        #                'kallio': 20,
        #                'seinä': 100}

    def kaiva_kaytavat(self):
        huoneet = self.luolasto.huoneet
        huoneet.sort()
        # for huone in huoneet:
        #     print(huone)
        for n in range(1, len(huoneet)):
            self.kaiva_kaytava(huoneet[n-1], huoneet[n])

        
        for _ in range(random.randint(3, 6)):
            lahtohuone = random.choice(huoneet)
            kohdehuone = lahtohuone
            while abs(huoneet.index(lahtohuone) - huoneet.index(kohdehuone)) <= 2:
                kohdehuone = random.choice(huoneet)
            uudet_painot = {'lattia': 6,
                            'käytävä': 3,
                            'kallio': 6,
                            'seinä': 50,
                            'ovi': 1}
            self.kaiva_kaytava(lahtohuone, kohdehuone, uudet_painot, False)

    def kaiva_kaytava(self, lahtohuone, kohdehuone, painot: dict = None, visualisointi: bool = False):
        if not painot:
            painot = {'lattia': 0,
                       'käytävä': 0,
                       'kallio': 2,
                       'seinä': 25,
                       'ovi': 10}

        # print(f'kaivetaan {lahtohuone+1} -> {kohdehuone+1}')

        # Nethack ilmeisesti yhdistää huoneiden keskipisteet
        lahto_y = lahtohuone.keskipiste()[0]
        lahto_x = lahtohuone.keskipiste()[1]
        kohde_y = kohdehuone.keskipiste()[0]
        kohde_x = kohdehuone.keskipiste()[1]

        if visualisointi:
            self.luolasto.kartta[kohde_y][kohde_x].sisalto = 'X'

        # lahto_y = random.randint(lahtohuone.y+1, lahtohuone.y + lahtohuone.korkeus-2)
        # lahto_x = random.randint(lahtohuone.x+1, lahtohuone.x + lahtohuone.leveys-2)
        # kohde_y = random.randint(kohdehuone.y+1, kohdehuone.y + kohdehuone.korkeus-2)
        # kohde_x = random.randint(kohdehuone.x+1, kohdehuone.x + kohdehuone.leveys-2)


        # print(f'{lahto_y, lahto_x} -> {kohde_y, kohde_x}')
        h_arvot = self.laske_h_arvot((kohde_y, kohde_x))
        kautta = [[None for _ in range(self.luolasto.leveys)] for _ in range(self.luolasto.korkeus)]
        hinta = [[10**9 for _ in range(self.luolasto.leveys)] for _ in range(self.luolasto.korkeus)]
        hinta[lahto_y][lahto_x] = 0
        # print(f'matkaa {h_arvot[lahto_y][lahto_x]}')

        jono = []
        heappush(jono, (0, (lahto_y, lahto_x)))
        while len(jono) > 0:
            sijainti = heappop(jono)[1]

            if visualisointi:
                self.luolasto.kartta[sijainti[0]][sijainti[1]].sisalto = None
                os.system('clear')
                self.luolasto.nayta()
                print(f'yhdistetään honeet {self.luolasto.huoneet.index(lahtohuone)} ja {self.luolasto.huoneet.index(kohdehuone)}')
                print('o: ruutu on A*-jonossa')
                sleep(0.05)

            if sijainti == (kohde_y, kohde_x):
                # print('reitti löytyi:')
                reitti = [(kohde_y, kohde_x)]

                for rivi in self.luolasto.kartta:
                    for ruutu in rivi:
                        ruutu.sisalto = None

                while True:
                    edellinen = kautta[sijainti[0]][sijainti[1]]
                    reitti.append(edellinen)
                    if edellinen == (lahto_y, lahto_x):
                        break
                    sijainti = edellinen

                reitti = reitti[::-1]
                # print(reitti)

                for ruutu in reitti:
                    kohdetyyppi = 'käytävä'
                    if self.luolasto.kartta[ruutu[0]][ruutu[1]].tyyppi == 'seinä' or self.luolasto.kartta[ruutu[0]][ruutu[1]].tyyppi == 'ovi':
                        kohdetyyppi = 'ovi'
                    self.luolasto.kaiva(ruutu[1], ruutu[0], kohdetyyppi)
                break

            # naapurien tarkistus
            naapurit = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for n in naapurit:
                uusi_y = sijainti[0] + n[0]
                uusi_x = sijainti[1] + n[1]
                # tarkistetaan rajat
                if uusi_y < 0 or uusi_y >= self.luolasto.korkeus:
                    continue
                if uusi_x < 0 or uusi_x >= self.luolasto.leveys:
                    continue
                
                uusi_hinta = hinta[sijainti[0]][sijainti[1]] + painot[self.luolasto.kartta[uusi_y][uusi_x].tyyppi]*(random.random()/20+0.975)
                if uusi_hinta < hinta[uusi_y][uusi_x]:
                    hinta[uusi_y][uusi_x] = uusi_hinta
                    kautta[uusi_y][uusi_x] = sijainti

                    if visualisointi:
                        self.luolasto.kartta[sijainti[0]][sijainti[1]].sisalto = 'o'

                    heappush(jono, (hinta[sijainti[0]][sijainti[1]] + painot[self.luolasto.kartta[uusi_y][uusi_x].tyyppi] + h_arvot[uusi_y][uusi_x], (uusi_y, uusi_x)))

    def laske_h_arvot(self, kohderuutu):
        korkeus = self.luolasto.korkeus
        leveys = self.luolasto.leveys
        kohde_y = kohderuutu[0]
        kohde_x = kohderuutu[1]
        h_arvot = [[0 for _ in range(leveys)] for _ in range(korkeus)]
        for y in range(korkeus):
            for x in range(leveys):
                # manhattan-etäisyys
                h_arvot[y][x] = 5.5*(abs(y-kohde_y) + abs(x-kohde_x))
        return h_arvot

