import unittest
import random
from luokat.luolasto import Luolasto
from luokat.komponenttien_etsija import KomponenttienEtsija
from luokat.kaytavan_kaivaja import KaytavanKaivaja
from algoritmit.bsp import bsp

class TestKomponentit(unittest.TestCase):
    def setUp(self):
        self.L = Luolasto(19, 77)
        self.etsija = KomponenttienEtsija(self.L)
        self.kaivaja = KaytavanKaivaja(self.L)

    def test_komponentit(self):
        bsp(self.L, 1, 7)
        self.etsija.etsi_komponentit()
        # pitäisi olla vähintään 7
        self.assertGreaterEqual(len(self.L.komponentit), 7)

        self.kaivaja.kaiva_kaytavat(False)  # yhdistetään komponentit
        self.etsija.etsi_komponentit()
        self.assertEqual(len(self.L.komponentit), 1)

    def test_komponenttien_laskija(self):
        edellinen = None
        todelliset_komponentit = 0
        for rivi in range(1, 18):
            # kaivetaan joka riviltä satunnainen ruutu
            kaivetaan_x = random.choice(range(1, 76))
            self.L.kaiva(kaivetaan_x, rivi)
            if kaivetaan_x == edellinen:
                # edellinen komponentti laajeni
                continue
            else:
                # luotiin uusi komponentti
                edellinen = kaivetaan_x
                todelliset_komponentit += 1
            
        self.etsija.etsi_komponentit()
        loydetyt_komponentit = len(self.L.komponentit)

        self.assertEqual(loydetyt_komponentit, todelliset_komponentit)