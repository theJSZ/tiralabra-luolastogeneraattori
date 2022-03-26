from luokat.luolasto2 import Luolasto
from heapq import heappop, heappush

class KaytavanKaivaja:
    def __init__(self, luolasto: Luolasto):
        self.luolasto = luolasto
        self.painot = {'lattia': 1,
                       'käytävä': 2,
                       'kallio': 5,
                       'seinä': 1000}

    def kaiva_kaytavat(self):
        huoneet = self.luolasto.huoneet
        huoneet.sort()
        for huone in huoneet:
            print(huone)
        reitti = []
        jono = []
        self.kaiva_kaytava(huoneet[0], huoneet[1])

    def kaiva_kaytava(self, lahtohuone, kohdehuone):
        print(f'kaivetaan {lahtohuone} -> {kohdehuone}')
        lahtoruutu_y = lahtohuone.keskipiste()[0]
        lahtoruutu_x = lahtohuone.keskipiste()[1]

        kohderuutu = kohdehuone.keskipiste()
        # print(f'{lahtoruutu} -> {kohderuutu}')
        h_arvot = self.laske_h_arvot(kohderuutu)
        print(f'matkaa {h_arvot[lahtoruutu_y][lahtoruutu_x]}')

        jono = []
        heappush(jono, (0, (lahtoruutu_y, lahtoruutu_x)))
        while len(jono) > 0:
            kasiteltava = heappop(jono)
            print(f'ruudussa {kasiteltava}')
            kasiteltava_y = kasiteltava[1][0]
            kasiteltava_x = kasiteltava[1][1]

            naapurit = self.luolasto.kartta[kasiteltava_y][kasiteltava_x].naapurit
            for naapuri in naapurit:
                naapuri_y = naapuri.sijainti[0]
                naapuri_x = naapuri.sijainti[1]
                naapuri_paino = self.painot[naapuri.tyyppi]+h_arvot[naapuri_y][naapuri_x]
                print(naapuri, naapuri_paino)
                heappush(jono, (naapuri_paino+h_arvot[naapuri_y][naapuri_x], naapuri))

    def laske_h_arvot(self, kohderuutu):
        korkeus = self.luolasto.korkeus
        leveys = self.luolasto.leveys
        kohde_y = kohderuutu[0]
        kohde_x = kohderuutu[1]
        h_arvot = [[0 for _ in range(leveys)] for _ in range(korkeus)]
        for y in range(korkeus):
            for x in range(leveys):
                # manhattan-etäisyys
                h_arvot[y][x] = abs(y-kohde_y) + abs(x-kohde_x)
        return h_arvot