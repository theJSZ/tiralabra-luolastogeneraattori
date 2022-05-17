"""Sisältää luokan joka etsii reitin käytävälle kahden ruudun välillä
annettujen painojen mukaan ja kaivaa sen käyttäen Luolaston metodeja"""
from time import sleep
from heapq import heappop, heappush
import random
from luokat.luolasto import Luolasto
class KaytavanKaivaja:
    """Luokka joka luo käytävät luolastoon"""
    def __init__(self, luolasto: Luolasto):
        self.luolasto = luolasto

    def kaiva_kaytavat(self, visualisointi, mutkaisuus = 9):
        """Käytetään luolastolle jossa on huoneita (BSP).
        Järjestää huoneet vasemmalta oikealle ja yhdistää ne
        pari kerrallaan. Sen jälkeen yhdistää vaihtelevan
        määrän satunnaisia pareja (ei aina löydä parempia reittejä
        kuin olemassaolevat)
        """
        huoneet = self.luolasto.huoneet
        huoneet.sort()

        # yhdistäminen järjestyksessä
        for huone in range(1, len(huoneet)):
            lahto_y, lahto_x = huoneet[huone-1].keskipiste()
            kohde_y, kohde_x = huoneet[huone].keskipiste()

            self.kaiva_kaytava(lahto_y, lahto_x, kohde_y, kohde_x, mutkaisuus, None, visualisointi)

        # yhdistäminen muutaman kerran satunnaisesti
        for _ in range(random.randint(6, 9)):
            lahtohuone = random.choice(huoneet)
            kohdehuone = random.choice(huoneet)
            while kohdehuone is lahtohuone:
                kohdehuone = random.choice(huoneet)

            # emme halua uusia reittejä vain jo olemassaolevia pitkin,
            # tällä kertaa huoneiden läpi on kalliimpaa kulkea
            uudet_painot = {'lattia': 15,
                            'käytävä': 0,
                            'kallio': 7,
                            'seinä': 50,
                            'ovi': 1}

            lahto_y, lahto_x = lahtohuone.keskipiste()
            kohde_y, kohde_x = kohdehuone.keskipiste()

            self.kaiva_kaytava(lahto_y,
                               lahto_x,
                               kohde_y,
                               kohde_x,
                               mutkaisuus,
                               uudet_painot,
                               visualisointi)

    def nayta_reitti(self, reitti, lahto_y, lahto_x, kohde_y, kohde_x):
        """Näyttää suunnitellun käytävän ennen kuin kaivaminen alkaa"""
        self.luolasto.poista_sisallot()

        for ruutu in reitti:
            ruutu = self.luolasto.kartta[ruutu[0]][ruutu[1]]
            if ruutu.tyyppi in ['käytävä', 'lattia']:
                ruutu.sisalto = '▒'
                continue
            ruutu.sisalto = '▓'  # merkataan kaivettavat ruudut selvemmin
        self.luolasto.kartta[lahto_y][lahto_x].sisalto = 'O'  # reitin lähtöruutu
        self.luolasto.kartta[kohde_y][kohde_x].sisalto = 'X'  # reitin kohderuutu

        self.luolasto.nayta()
        sleep(1)

    def nayta_askel(self, ruutu):
        """Näyttää yhden askeleen käytävän kaivamista"""
        ruutu.sisalto = 'o'  # 'kaivaja' on ruudussa
        self.luolasto.nayta()
        sleep(0.10)
        ruutu.sisalto = None  # 'kaivaja' on poistunut ruudusta


    def kaiva_kaytava(
        self,
        lahto_y,
        lahto_x,
        kohde_y,
        kohde_x,
        mutkaisuus,
        painot: dict = None,
        visualisointi: bool = False):
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
            painot = {'lattia': 4,
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

                while True:  # tutkimme minkä ruutujen kautta reitti löytyi
                    edellinen = kautta[sijainti[0]][sijainti[1]]
                    reitti.append(edellinen)
                    if edellinen == (lahto_y, lahto_x):
                        break
                    sijainti = edellinen

                reitti = reitti[::-1]  # käännetään reitti oikeinpäin

                if visualisointi:
                    # näytetään suunniteltu käytävä
                    self.nayta_reitti(reitti, lahto_y, lahto_x, kohde_y, kohde_x)

                for ruutu in reitti:
                    ruutu = self.luolasto.kartta[ruutu[0]][ruutu[1]]

                    # kallio kaivetaan käytäväksi, seinä oveksi
                    kohdetyyppi = 'käytävä'
                    if ruutu.tyyppi in ['seinä', 'ovi']:
                        kohdetyyppi = 'ovi'

                    # visualisoinnin sujuvoittamiseksi hypätään
                    # jo kaivettujen ruutujen yli
                    if visualisointi and ruutu.tyyppi not in ['käytävä', 'lattia']:
                        self.nayta_askel(ruutu)

                    self.luolasto.kaiva(ruutu.sijainti[1], ruutu.sijainti[0], kohdetyyppi)
                break  # kohde saavutettu ja tarvittavat toimenpiteet tehty

            # kohde ei vielä saavutettu:
            # naapurien tarkistus ja lisäys tarvittaessa jonoon
            naapurit = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for naapuri in naapurit:
                uusi_y = sijainti[0] + naapuri[0]
                uusi_x = sijainti[1] + naapuri[1]

                # tarkistetaan rajat
                if uusi_y < 0 or uusi_y >= self.luolasto.korkeus:
                    continue
                if uusi_x < 0 or uusi_x >= self.luolasto.leveys:
                    continue

                # kuinka paljon maksaa liikkua tähän ruutuun
                paino = painot[self.luolasto.kartta[uusi_y][uusi_x].tyyppi]

                # sopivat arvot välillä 2..??, pienempi arvo tuottaa enemmän ylimääräisiä mutkia
                kerroin = max(12 - mutkaisuus, 2)

                saadetty_paino = paino * ((random.random()/kerroin) + 1-(1/kerroin*2))
                uusi_hinta = saadetty_paino + hinta[sijainti[0]][sijainti[1]]

                # löytyi entistä parempi reitti
                if uusi_hinta < hinta[uusi_y][uusi_x]:
                    hinta[uusi_y][uusi_x] = uusi_hinta
                    kautta[uusi_y][uusi_x] = sijainti
                    h_arvo = h_arvot[uusi_y][uusi_x]

                    heappush(jono, (hinta[sijainti[0]][sijainti[1]]+paino+h_arvo, (uusi_y, uusi_x)))

    def laske_h_arvot(self, kohderuutu):
        """Laskee kaikille ruuduille manhattan-etäisyyden
        annettuun kohderuutuun, tarvitaan A*-algoritmissa
        """
        korkeus = self.luolasto.korkeus
        leveys = self.luolasto.leveys
        h_arvot = [[0 for _ in range(leveys)] for _ in range(korkeus)]
        etaisyyden_painotus = 1.1  # isompi painotus lisää tehokkuutta mutta
                                   # tuottaa huonomman näköisiä käytäviä

        kohde_y, kohde_x = kohderuutu

        for ruutu_y in range(korkeus):
            for ruutu_x in range(leveys):
                manhattan_etaisyys = abs(ruutu_y-kohde_y) + abs(ruutu_x-kohde_x)
                h_arvot[ruutu_y][ruutu_x] = etaisyyden_painotus * manhattan_etaisyys

        return h_arvot
