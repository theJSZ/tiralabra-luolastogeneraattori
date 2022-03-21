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

    def tayta(self):
        self.kartta = [[SEINA for _ in range(self._leveys)] for _ in range(self._korkeus) ]

    def kaiva(self, x, y):
        """Muuttaa annetun ruudun lattiaksi

        Args:
            y (_type_): _description_
            x (_type_): _description_
        """
        self.kartta[y][x] = LATTIA

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

    def nayta(self):
        for rivi in self.kartta:
            print(''.join(rivi))


if __name__ == "__main__":
    L = Luolasto()
    print(L.leveys, L.korkeus)
    L.nayta()