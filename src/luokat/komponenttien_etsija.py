"""Sisältää luokan kaikkien yhtenäisten komponenttien löytämiseksi"""
from luokat.komponentti import Komponentti

class KomponenttienEtsija:
    """Käy luolaston läpi löytäen yhtenäiset komponentit
    """
    def __init__(self, luolasto):
        self.luolasto = luolasto
        self.vierailtu = []

    def etsi_komponentit(self):
        """Etsii käymättömiä ruutuja, aloittaen niistä syvyyshaun
        ja luomalla kulloinkin saavutetuista ruuduista uuden komponentin"""
        self.luolasto.komponentit = []
        leveys = self.luolasto.leveys
        korkeus = self.luolasto.korkeus

        self.vierailtu = [[False for _ in range(leveys)] for _ in range(korkeus)]
        komponentti_nr  = 0

        # syvyyshaku alkaa aina jos saavutaan ruutuun jossa voi kulkea
        # ja jossa ei vielä olla käyty.
        # sieltä saavutettavissa olevat ruudut kootaan yhdeksi komponentiksi
        for ruutu_y in range(1, korkeus):
            for ruutu_x in range(1, leveys):

                ruutu = self.luolasto.kartta[ruutu_y][ruutu_x]
                if ruutu.tyyppi not in ['käytävä', 'lattia', 'ovi']:
                    continue
                if self.vierailtu[ruutu_y][ruutu_x]:
                    continue

                ruudut = []  # tähän kerätään komponentin ruudut
                self.dfs(ruutu_y, ruutu_x, komponentti_nr, ruudut)

                komponentti = Komponentti(ruudut)
                self.luolasto.komponentit.append(komponentti)
                komponentti.valitse_kohderuutu()  # komponenttiin tehtävät käytävät
                                                  # tähtäävät tähän satunnaiseen ruutuun

                komponentti_nr += 1

        if len(self.luolasto.komponentit) == 1:  # poistetaan komponenttien tunnukset näkyvistä
            self.luolasto.poista_sisallot()

    def kartalla(self, ruutu_y, ruutu_x):
        """Tarkistaa onko annettu koordinaattipari kartalla"""
        if ruutu_y < 0 or ruutu_y >= self.luolasto.korkeus:
            return False
        if ruutu_x < 0 or ruutu_x >= self.luolasto.leveys:
            return False
        return True

    def dfs(self, ruutu_y, ruutu_x, komponentti_nr, ruudut):
        """Syvyyshaku, kerää myös komponenttiin kuuluvat ruudut listaan

        Args:
            y (int): y-koordinaatti
            x (int): x-koordinaatti
            komponentti_nr (int): juokseva numerointi
            ruudut (list): lista ruuduista komponentissa
        """
        if not self.kartalla(ruutu_y, ruutu_x):
            return

        ruutu = self.luolasto.kartta[ruutu_y][ruutu_x]
        if (ruutu.tyyppi not in ['käytävä', 'lattia', 'ovi']) or (self.vierailtu[ruutu_y][ruutu_x]):
            return

        self.vierailtu[ruutu_y][ruutu_x] = True

        # merkataan eri komponentit eri tunnuksin
        ruutu.sisalto = chr((komponentti_nr % 30) + 65)

        # lisätään ruutu listaan josta kootaan komponentti
        ruudut.append((ruutu_y, ruutu_x))

        # jälkimmäiset mukaan jos haluamme ajatella diagonaalit saavutettavina
        seuraavat = [(-1, 0), (1, 0), (0, -1), (0, 1)]  #, (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for seuraava in seuraavat:
            seuraava_y = ruutu_y+seuraava[0]
            seuraava_x = ruutu_x+seuraava[1]

            self.dfs(seuraava_y, seuraava_x, komponentti_nr, ruudut)
