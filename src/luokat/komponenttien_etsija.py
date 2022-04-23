from luokat.komponentti import Komponentti


class KomponenttienEtsija:
    """Käy luolaston läpi syvyyshaulla löytäen yhtenäiset komponentit
    """
    def __init__(self, luolasto):
        self.luolasto = luolasto

    def etsi_komponentit(self):
        self.luolasto.komponentit = []

        self.visited = [[False for _ in range(self.luolasto.leveys)] for _ in range(self.luolasto.korkeus)]
        komponentti_nr  = 0

        # syvyyshaku alkaa aina jos saavutaan ruutuun jossa voi kulkea
        # ja jossa ei vielä olla käyty.
        # saavutettavissa olevat ruudut kootaan yhdeksi komponentiksi
        for y in range(1, self.luolasto.korkeus):
            for x in range(1, self.luolasto.leveys):
                ruudut = []
                ruutu = self.luolasto.kartta[y][x]
                if (ruutu.tyyppi not in ['käytävä', 'lattia', 'ovi']) or (self.visited[y][x]):
                    continue

                self.dfs(y, x, komponentti_nr, ruudut)

                komponentti = Komponentti(ruudut)
                self.luolasto.komponentit.append(komponentti)
                komponentti.valitse_kohderuutu()  # käytävän kaivamista varten
                komponentti_nr += 1

        if len(self.luolasto.komponentit) == 1:  # poistetaan komponenttien tunnukset tarpeettomina
            self.luolasto.poista_sisallot()

    def kartalla(self, y, x):
        if y < 0 or y >= self.luolasto.korkeus:
            return False
        if x < 0 or x >= self.luolasto.leveys:
            return False
        return True

    def dfs(self, y, x, komponentti_nr, ruudut):
        """Syvyyshaku, kerää myös komponenttiin kuuluvat ruudut listaan

        Args:
            y (_type_): _description_
            x (_type_): _description_
            komponentti_nr (_type_): _description_
            ruudut (_type_): _description_
        """
        if not self.kartalla(y, x):
            return
        ruutu = self.luolasto.kartta[y][x]
        if (ruutu.tyyppi not in ['käytävä', 'lattia', 'ovi']) or (self.visited[y][x]):
            return

        self.visited[y][x] = True

        # merkataan eri komponentit eri tunnuksin
        ruutu.sisalto = chr((komponentti_nr % 30) +65)

        # lisätään ruutu listaan josta kootaan komponentti
        ruudut.append((y, x))

        # jälkimmäiset mukaan jos haluamme liittää diagonaalit
        seuraavat = [(-1, 0), (1, 0), (0, -1), (0, 1)]  #, (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for seuraava in seuraavat:
            seuraava_y = y+seuraava[0]
            seuraava_x = x+seuraava[1]

            self.dfs(seuraava_y, seuraava_x, komponentti_nr, ruudut)