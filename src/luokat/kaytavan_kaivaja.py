from time import sleep
from luokat.luolasto import Luolasto
from heapq import heappop, heappush
import random
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
        # print('käytävien kaivaminen alkaa')
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
            kohdehuone = random.choice(huoneet)
            while kohdehuone is lahtohuone:
                kohdehuone = random.choice(huoneet)

            # emme halua uusia reittejä vain jo olemassaolevia pitkin
            uudet_painot = {'lattia': 15, # 15
                            'käytävä': 0, # 3
                            'kallio': 7,  # 7
                            'seinä': 50,  # 50
                            'ovi': 1}     # 1

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

        # A* tarvitsee etäisyysarviot auttamaan reitin hakemisessa
        h_arvot = self.laske_h_arvot((kohde_y, kohde_x))

        # haluamme jälkeenpäin saada selville mistä ruudusta on menty mihinkin reitillä
        kautta = [[None for _ in range(self.luolasto.leveys)] for _ in range(self.luolasto.korkeus)]
        
        # aluksi joka paikkaan on 'ääretön' hinta
        hinta = [[10**9 for _ in range(self.luolasto.leveys)] for _ in range(self.luolasto.korkeus)]
        hinta[lahto_y][lahto_x] = 0

        jono = []
        heappush(jono, (0, (lahto_y, lahto_x)))
        while len(jono) > 0:
            sijainti = heappop(jono)[1]

            if sijainti == (kohde_y, kohde_x):  # kohde saavutettu
                reitti = [(kohde_y, kohde_x)]   # reitti otetaan muistiin lopusta alkaen

                for rivi in self.luolasto.kartta:  # tämä liittyy visualisointiin
                    for ruutu in rivi:
                        ruutu.sisalto = None

                while True:  # tutkimme minkä ruutujen kautta reitti löytyi
                    edellinen = kautta[sijainti[0]][sijainti[1]]
                    reitti.append(edellinen)
                    if edellinen == (lahto_y, lahto_x):
                        break
                    sijainti = edellinen

                reitti = reitti[::-1]  # käännetään reitti oikeinpäin

                # näytetään hetken ajan suunniteltu reitti
                if visualisointi:
                    for ruutu in reitti:
                        ruutu = self.luolasto.kartta[ruutu[0]][ruutu[1]]
                        if ruutu.tyyppi in ['käytävä', 'lattia']:
                            ruutu.sisalto = '▒'
                            continue
                        ruutu.sisalto = '▓'
                    self.luolasto.kartta[lahto_y][lahto_x].sisalto = 'O'
                    self.luolasto.kartta[kohde_y][kohde_x].sisalto = 'X'

                    self.luolasto.nayta()
                    sleep(1)

                for ruutu in reitti:
                    ruutu = self.luolasto.kartta[ruutu[0]][ruutu[1]]

                    # kallio kaivetaan käytäväksi, seinä oveksi
                    # vaikuttaa vain ulkoasuun
                    kohdetyyppi = 'käytävä'
                    if ruutu.tyyppi == 'seinä' or ruutu.tyyppi == 'ovi':
                        kohdetyyppi = 'ovi'

                    # visualisoinnin sujuvoittamiseksi hypätään
                    # jo kaivettujen ruutujen yli
                    if visualisointi and not ruutu.tyyppi in ['käytävä', 'lattia']:
                        ruutu.sisalto = 'o'  # 'kaivaja' on ruudussa
                        self.luolasto.nayta()
                        self.luolasto.kartta[lahto_y][lahto_x].sisalto = 'O'
                        self.luolasto.kartta[kohde_y][kohde_x].sisalto = 'X'
                        sleep(0.1)

                    ruutu.sisalto = None  # 'kaivaja' on poistunut ruudusta
                    self.luolasto.kaiva(ruutu.sijainti[1], ruutu.sijainti[0], kohdetyyppi)
                break  # kohde saavutettu ja tarvittavat toimenpiteet tehty

            # kohde ei vielä saavutettu:
            # naapurien tarkistus ja lisäys tarvittaessa jonoon
            naapurit = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for n in naapurit:
                uusi_y = sijainti[0] + n[0]
                uusi_x = sijainti[1] + n[1]
                # tarkistetaan rajat
                if uusi_y < 0 or uusi_y >= self.luolasto.korkeus:
                    continue
                if uusi_x < 0 or uusi_x >= self.luolasto.leveys:
                    continue

                satunnaisuuskerroin = 3  # sopivat arvot välillä 2..??, pienempi arvo tuottaa orgaanisempia käytäviä
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
                etaisyyden_painotus = 1.1  # isompi painotus lisää tehokkuutta mutta
                                           # tuottaa huonomman näköisiä käytäviä
                h_arvot[y][x] = etaisyyden_painotus*(abs(y-kohde_y) + abs(x-kohde_x))
        return h_arvot
