from luokat.huone import Huone


RUUTUTYYPIT = {'lattia': '.',
               'kivi': '#',
               'seinä': ['─', '│', '┌', '┐', '└', '┘', '├', '┤', '┬', '┴']}
# ─ 2500
# │ 2502
# ┌ 250C
# ┐ 2510
# └ 2514
# ┘ 2518
# ├ 251C
# ┤ 2524
# ┬ 252C
# ┴ 2534

# EI_LATTIA = '/'
LATTIA = '.'
SEINA = '#'

class Luolasto:
    def __init__(self, leveys=77, korkeus=19):
        self._leveys = leveys
        self._korkeus = korkeus
        self.tayta()
        self._huoneet = []

    def tayta(self):
        self.kartta = [[SEINA for _ in range(self._leveys)] for _ in range(self._korkeus) ]

    def kaiva(self, x, y):
        """Muuttaa annetun ruudun lattiaksi

        Args:
            y (_type_): _description_
            x (_type_): _description_
        """
        self.kartta[y][x] = LATTIA

    def kaiva_huone(self, huone: Huone):
        print(f'kaivetaan: y {huone.y} x {huone.x} korkeus {huone.korkeus} leveys {huone.leveys}')
        for y in range(huone.y, huone.y+huone.korkeus):
            for x in range(huone.x, huone.x+huone.leveys):
                self.kaiva(x, y)

    def rakenna(self, x, y):
        """Muuttaa annetun ruudun seinäksi

        Args:
            y (_type_): _description_
            x (_type_): _description_
        """
        self.kartta[y][x] = SEINA

    @property
    def leveys(self):
        return self._leveys

    @leveys.setter
    def leveys(self, leveys):
        self._leveys = leveys

    @property
    def korkeus(self):
        return self._korkeus

    @korkeus.setter
    def korkeus(self, korkeus):
        self._korkeus = korkeus

    @property
    def huoneet(self):
        return self._huoneet

    def lisaa_huone(self, huone: Huone):
        self._huoneet.append(huone)

    def nayta(self):
        for rivi in self.kartta:
            print(''.join(rivi))


if __name__ == "__main__":
    L = Luolasto()
    print(L.leveys, L.korkeus)
    L.nayta()