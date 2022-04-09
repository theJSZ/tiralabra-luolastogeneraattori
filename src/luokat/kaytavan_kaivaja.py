from time import sleep
from luokat.luolasto import Luolasto
from heapq import heappop, heappush
import random
import os

class KaytavanKaivaja:
    def __init__(self, luolasto: Luolasto):
        self.luolasto = luolasto

    def kaiva_kaytavat(self, visualisointi):
        """Käytetään luolastolle jossa on huoneita (BSP).
        Järjestää huoneet vasemmalta oikealle ja yhdistää ne
        pari kerrallaan. Sen jälkeen yhdistää vaihtelevan
        määrän satunnaisia pareja (ei aina löydä parempia reittejä
        kuin olemassaolevat)
        """
        huoneet = self.luolasto.huoneet
        huoneet.sort()

        # yhdistäminen järjestyksessä
        for n in range(1, len(huoneet)):
            lahto_y = huoneet[n-1].keskipiste()[0]
            lahto_x = huoneet[n-1].keskipiste()[1]
            kohde_y = huoneet[n].keskipiste()[0]
            kohde_x = huoneet[n].keskipiste()[1]

            self.kaiva_kaytava(lahto_y, lahto_x, kohde_y, kohde_x, None, visualisointi)
        
        # yhdistäminen muutaman kerran satunnaisesti
        for _ in range(random.randint(6, 9)):
            lahtohuone = random.choice(huoneet)
            kohdehuone = lahtohuone
            while abs(huoneet.index(lahtohuone) - huoneet.index(kohdehuone)) <= 2:
                kohdehuone = random.choice(huoneet)
            uudet_painot = {'lattia': 15,
                            'käytävä': 3,
                            'kallio': 7,
                            'seinä': 50,
                            'ovi': 1}

            lahto_y = lahtohuone.keskipiste()[0]
            lahto_x = lahtohuone.keskipiste()[1]
            kohde_y = kohdehuone.keskipiste()[0]
            kohde_x = kohdehuone.keskipiste()[1]

            self.kaiva_kaytava(lahto_y, lahto_x, kohde_y, kohde_x, uudet_painot, visualisointi)

    def kaiva_kaytava(self, lahto_y, lahto_x, kohde_y, kohde_x, painot: dict = None, visualisointi: bool = False):
        """Yhdistää annetut koordinaatit
        mukautetulla A*-reittihaulla

        Args:
            lahto_y (int): y1
            lahto_x (int): x1
            kohde_y (int): y2
            kohde_x (int): x2
            painot (dict, optional): painojen säätämiseksi. Oletus None.
            visualisointi (bool, optional)
        """
        if not painot:
            painot = {'lattia': 0,
                       'käytävä': 1,
                       'kallio': 3,
                       'seinä': 25,
                       'ovi': 10}

        h_arvot = self.laske_h_arvot((kohde_y, kohde_x))
        kautta = [[None for _ in range(self.luolasto.leveys)] for _ in range(self.luolasto.korkeus)]
        hinta = [[10**9 for _ in range(self.luolasto.leveys)] for _ in range(self.luolasto.korkeus)]
        hinta[lahto_y][lahto_x] = 0

        jono = []
        heappush(jono, (0, (lahto_y, lahto_x)))
        while len(jono) > 0:
            sijainti = heappop(jono)[1]

            if sijainti == (kohde_y, kohde_x):
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

                for ruutu in reitti:
                    kohdetyyppi = 'käytävä'
                    if self.luolasto.kartta[ruutu[0]][ruutu[1]].tyyppi == 'seinä' or self.luolasto.kartta[ruutu[0]][ruutu[1]].tyyppi == 'ovi':
                        kohdetyyppi = 'ovi'
                    self.luolasto.kartta[ruutu[0]][ruutu[1]].sisalto = 'o'
                    if visualisointi and not self.luolasto.kartta[ruutu[0]][ruutu[1]].tyyppi in ['käytävä', 'lattia']:
                        self.luolasto.nayta()
                        self.luolasto.kartta[lahto_y][lahto_x].sisalto = 'O'
                        self.luolasto.kartta[kohde_y][kohde_x].sisalto = 'X'
                        sleep(0.1)
                    self.luolasto.kaiva(ruutu[1], ruutu[0], kohdetyyppi)
                    self.luolasto.kartta[ruutu[0]][ruutu[1]].sisalto = None
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
                
                satunnaisuuskerroin = 3 # sopivat arvot välillä 2..??, pienempi arvo tuottaa orgaanisempia käytäviä
                uusi_hinta = painot[self.luolasto.kartta[uusi_y][uusi_x].tyyppi]*((random.random()/satunnaisuuskerroin) + 1-(1/satunnaisuuskerroin*2))
                uusi_hinta = uusi_hinta + hinta[sijainti[0]][sijainti[1]] 
                if uusi_hinta < hinta[uusi_y][uusi_x]:
                    hinta[uusi_y][uusi_x] = uusi_hinta
                    kautta[uusi_y][uusi_x] = sijainti

                    heappush(jono, (hinta[sijainti[0]][sijainti[1]] + painot[self.luolasto.kartta[uusi_y][uusi_x].tyyppi] + h_arvot[uusi_y][uusi_x], (uusi_y, uusi_x)))

    def laske_h_arvot(self, kohderuutu):
        """Laskee kaikille ruuduille manhattan-etäisyyden
        annettuun kohderuutuun, tarvitaan A*-algoritmissa

        Args:
            kohderuutu (Ruutu): _description_

        Returns:
            [[]]: 2-ulotteinen taulukko
        """
        korkeus = self.luolasto.korkeus
        leveys = self.luolasto.leveys
        kohde_y = kohderuutu[0]
        kohde_x = kohderuutu[1]
        h_arvot = [[0 for _ in range(leveys)] for _ in range(korkeus)]
        for y in range(korkeus):
            for x in range(leveys):
                etaisyyden_painotus = 1.1
                h_arvot[y][x] = etaisyyden_painotus*(abs(y-kohde_y) + abs(x-kohde_x))
        return h_arvot

