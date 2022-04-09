import random

class Komponentti:
    def __init__(self, ruudut):
        self.ruudut = ruudut
        self.kohderuutu = None

    def valitse_kohderuutu(self):
        self.kohderuutu = random.choice(self.ruudut)

    def __str__(self):
        return f'kohderuutu {self.kohderuutu}'