from luokat.huone import Huone
class Ruutu:
    def __init__(self, y, x, tyyppi: str = None):
        self._tyyppi = tyyppi
        self._sisalto = None
        self._naapurit = [None for _ in range(8)]
        # naapurit:
        #
        # 035
        # 1.6
        # 247
        self.sijainti = (y, x)

    @property
    def naapurit(self):
        return [self._naapurit[i] for i in [1, 3, 4, 6]]

    @property
    def tyyppi(self):
        return self._tyyppi

    @tyyppi.setter
    def tyyppi(self, tyyppi: str):
        self._tyyppi = tyyppi

    @property
    def sisalto(self):
        return self._sisalto

    @sisalto.setter
    def sisalto(self, sisalto):
        self._sisalto = sisalto

    def __lt__(self, toinen):
        return True

    def seinan_esitys(self):
        """Yrittää löytää luontevimman ascii-esityksen
        seinäruudulle naapureista riippuen

        Returns:
            str: joku näistä: ┘ ┐ └ ┌ ┴ ┬ ├ ┤ ─ │
        """
        naapurityypit = []
        for naapuri in self._naapurit:
            if not naapuri:
                naapurityypit.append('tyhjä')
            else:
                naapurityypit.append(naapuri.tyyppi)

        # jos yhdessä diagonaalissa (0, 2, 5, 7) lattiaa mutta ei muualla:
        #   ┘ ┐ └ ┌
        if naapurityypit.count('lattia') == 1:
            if naapurityypit[0] == 'lattia':
                return '┘'
            if naapurityypit[2] == 'lattia':
                return '┐'
            if naapurityypit[5] == 'lattia':
                return '└'
            if naapurityypit[7] == 'lattia':
                return '┌'

        # Jos ei seinää kahdessa vierekkäisessä pääsuunnassa mutta kyllä kahdessa muussa:
        #   ┘ ┐ └ ┌
        if not 'seinä' in [naapurityypit[6], naapurityypit[4]]:
            if [naapurityypit[1], naapurityypit[3]] == ['seinä', 'seinä']:
                return '┘'
        if not 'seinä' in [naapurityypit[6], naapurityypit[3]]:
            if [naapurityypit[1], naapurityypit[4]] == ['seinä', 'seinä']:
                return '┐'
        if not 'seinä' in [naapurityypit[1], naapurityypit[4]]:
            if [naapurityypit[6], naapurityypit[3]] == ['seinä', 'seinä']:
                return '└'
        if not 'seinä' in [naapurityypit[1], naapurityypit[3]]:
            if [naapurityypit[6], naapurityypit[4]] == ['seinä', 'seinä']:
                return '┌'

        # Jos ei seinää vierekkäisissä diagonaaleissa mutta
        # kyllä kolmessa niihin liittyvässä pääsuunnassa:
        #   ┴ ┬ ├ ┤
        if not 'seinä' in [naapurityypit[0], naapurityypit[5]]:
            if [naapurityypit[1], naapurityypit[3], naapurityypit[6]] == ['seinä', 'seinä', 'seinä']:
                return '┴'

        if not 'seinä' in [naapurityypit[2], naapurityypit[7]]:
            if [naapurityypit[1], naapurityypit[4], naapurityypit[6]] == ['seinä', 'seinä', 'seinä']:
                return '┬'

        if not 'seinä' in [naapurityypit[5], naapurityypit[7]]:
            if [naapurityypit[3], naapurityypit[4], naapurityypit[6]] == ['seinä', 'seinä', 'seinä']:
                return '├'

        if not 'seinä' in [naapurityypit[0], naapurityypit[2]]:
            if [naapurityypit[3], naapurityypit[4], naapurityypit[1]] == ['seinä', 'seinä', 'seinä']:
                return '┤'

        # nyt jäljellä vain suoria pätkiä
        if [naapurityypit[1], naapurityypit[6]] == ['seinä', 'seinä']:
            return '─'
        if [naapurityypit[3], naapurityypit[4]] == ['seinä', 'seinä']:
            return '│'
        if 'seinä' in [naapurityypit[1], naapurityypit[6]]:
            return '─'
        if 'seinä' in [naapurityypit[3], naapurityypit[4]]:
            return '│'

        # jos mikään ehto ei täyttynyt, ei kyllä pitäisi tapahtua
        return '│'

    def __str__(self):
        # jos ruudussa on 'jotain', esim visualisaatioissa voi olla 'o'
        if self._sisalto:
            return str(self._sisalto)

        if not self._tyyppi:
            return ' '

        if self._tyyppi == 'seinä':
            return self.seinan_esitys()
        
        tyyppien_esitykset = {'kallio': ' ',
                              'lattia': '.',
                              'käytävä': '░',  # '▒' '▓'
                              'ovi': '+'} # oli ennen '+'
        
        return tyyppien_esitykset[self._tyyppi]


class Luolasto:
    def __init__(self, korkeus, leveys):
        self._korkeus = korkeus
        self._leveys = leveys
        self.kartta = [[Ruutu(y, x, 'kallio') for x in range(leveys)] for y in range(korkeus)]
        self.huoneet = []
        self.komponentit = []

    @property
    def korkeus(self):
        return self._korkeus

    @korkeus.setter
    def korkeus(self, korkeus):
        self._korkeus = korkeus

    @property
    def leveys(self):
        return self._leveys

    @leveys.setter
    def leveys(self, leveys):
        self._leveys = leveys

    def kaiva(self, x, y, kohdetyyppi: str = 'lattia'):
        """Muuttaa ruututyypin 'kallio' tai 'seinä' annetuksi tyypiksi

        Args:
            x (int): x-koordinaatti
            y (int): y-koordinaatti
            kohdetyyppi (str, optional): _description_. Defaults to 'lattia'.
        """
        if self.kartta[y][x].tyyppi in ['lattia', 'käytävä']:
            return
        self.kartta[y][x].tyyppi = kohdetyyppi

    def kaiva_huone(self, huone: Huone):
        """Kaivaa suorakulmion

        Args:
            huone (Huone): _description_
        """
        for y in range(huone.y, huone.y+huone.korkeus):
            for x in range(huone.x, huone.x+huone.leveys):
                self.kaiva(x, y)

    def kaiva_seinallinen_huone(self, huone: Huone):
        """Kaivaa suorakulmion, tekee reunoista tyyppiä 'seinä'

        Args:
            huone (Huone): _description_
        """
        for y in range(huone.y, huone.y+huone.korkeus):
            for x in range(huone.x, huone.x+huone.leveys):
                self.kartta[y][x].tyyppi = 'seinä'

        for y in range(huone.y+1, huone.y+huone.korkeus-1):
            for x in range(huone.x+1, huone.x+huone.leveys-1):
                self.kaiva(x, y)
        
    def tayta(self):
        """Täyttää luolaston kalliolla
        """
        self.huoneet = []
        for rivi in self.kartta:
            for ruutu in rivi:
                ruutu.tyyppi = 'kallio'

    def nayta(self):
        """Tulostaa luolaston
        """
        self.maarita_naapurit()
        self.etsi_seinat()
        for rivi in self.kartta:
            for ruutu in rivi:
                print(ruutu, end="")
            print()

    def maarita_naapurit(self):
        """Tarvitaan seinien oikein piirtymiseksi
        """
        naapurilokaatiot = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for y, rivi in enumerate(self.kartta):
            for x, ruutu in enumerate(rivi):
                for naapuri, lokaatio in enumerate(naapurilokaatiot):
                    naapuri_y = y+lokaatio[0]
                    naapuri_x = x+lokaatio[1]
                    # tarkistus onko naapuri kartan ulkopuolella
                    if naapuri_y < 0 or naapuri_y > self.korkeus-1:
                        ruutu._naapurit[naapuri] = None
                    elif naapuri_x < 0 or naapuri_x > self.leveys-1:
                        ruutu._naapurit[naapuri] = None
                    else:
                        ruutu._naapurit[naapuri] = self.kartta[naapuri_y][naapuri_x]

    def etsi_seinat(self):
        """Muuttaa lattian vieressä olevat kallioruudut
        seinäruuduiksi
        """
        for rivi in self.kartta:
            for ruutu in rivi:
                if ruutu.tyyppi == 'kallio':
                    for naapuri in ruutu._naapurit:
                        if naapuri and naapuri.tyyppi == 'lattia':
                            ruutu.tyyppi = 'seinä'

    def poista_sisallot(self):
        for rivi in self.kartta:
            for ruutu in rivi:
                ruutu.sisalto = None