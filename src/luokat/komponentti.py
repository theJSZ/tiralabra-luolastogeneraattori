"""Luokka komponentille"""
import random

class Komponentti:
    """Luokka yhtenäisen komponentin esittämiseen kun komponentteja
    on useampi
    """
    def __init__(self, ruudut):
        self.ruudut = ruudut
        self.kohderuutu = None

    def valitse_kohderuutu(self):
        """Arpoo mitä ruutua käytetään kohteena
        käytäviä luodessa"""
        self.kohderuutu = random.choice(self.ruudut)

    def __str__(self):
        return f'kohderuutu {self.kohderuutu}'
