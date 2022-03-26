class Huone:
    def __init__(self, y, x, korkeus, leveys):
        self._y = y
        self._x = x
        self._korkeus = korkeus
        self._leveys = leveys

    @property
    def y(self):
        return self._y
    @property
    def korkeus(self):
        return self._korkeus
    @property
    def x(self):
        return self._x
    @property
    def leveys(self):
        return self._leveys

    def keskipiste(self):
        return (self.y+self.korkeus//2, self.x+self.leveys//2)

    def __lt__(self, toinen):
        if self.x == toinen.x:
            return self.y < toinen.y
        return self.x < toinen.x

    def __str__(self):
        return f'{self.y}, {self.x}, {self.korkeus}, {self.leveys}'


# 13 6 