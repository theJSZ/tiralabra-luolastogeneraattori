"""Luokka huoneen muuttujille ja metodeille
"""
class Huone:
    """Suorakaiteen muotoinen alue luolastoa
    """
    def __init__(self, huone_y, huone_x, korkeus, leveys):
        """Luokan konstruktori

        Args:
            y (int): vasen ylänurkka y
            x (int): vasen ylänurkka x
            korkeus (int): huoneen korkeus
            leveys (int): huoneen leveys
        """
        self._y = huone_y
        self._x = huone_x
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
        """Palauttaa huoneen keskimmäisen ruudun

        Returns:
            tuple: y, x koordinaatit
        """
        return (self.y+self.korkeus//2, self.x+self.leveys//2)

    def __lt__(self, toinen):
        if self.x == toinen.x:
            return self.y < toinen.y
        return self.x < toinen.x

    def __str__(self):
        return f'{self.y}, {self.x}, {self.korkeus}, {self.leveys}'
