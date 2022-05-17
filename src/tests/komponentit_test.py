"""Testaa komponentteihin liittyviä asioita"""
import unittest
import random
from luokat.luolasto import Luolasto
from luokat.komponenttien_etsija import KomponenttienEtsija
from luokat.kaytavan_kaivaja import KaytavanKaivaja
from algoritmit.bsp import bsp

class TestKomponentit(unittest.TestCase):
    """Testaa komponenttien etsijää"""
    def setUp(self):
        self.luolasto = Luolasto(19, 77)
        self.etsija = KomponenttienEtsija(self.luolasto)
        self.kaivaja = KaytavanKaivaja(self.luolasto)

    def test_komponentit(self):
        """Testaa että komponenttien yhdistäminen toimii"""
        bsp(self.luolasto, 1, 7)  # luodaan vähintään 7 huonetta
        self.etsija.etsi_komponentit()
        # pitäisi olla vähintään 7 komponenttia
        self.assertGreaterEqual(len(self.luolasto.komponentit), 7)

        self.kaivaja.kaiva_kaytavat(False)  # yhdistetään komponentit
        self.etsija.etsi_komponentit()
        self.assertEqual(len(self.luolasto.komponentit), 1)

    def test_komponenttien_laskija(self):
        """Testaa että komponenttien määrä lasketaan oikein"""
        edellinen = None
        todelliset_komponentit = 0

        for rivi in range(1, 18):
            # kaivetaan joka riviltä satunnainen ruutu
            kaivetaan_x = random.choice(range(1, 76))
            self.luolasto.kaiva(kaivetaan_x, rivi)
            if kaivetaan_x == edellinen:
                # edellinen komponentti laajeni
                # ..x.....
                # .....x..
                # .x......
                # .X...... <-
                continue

                # luotiin uusi komponentti
                # .....x..
                # .x......
                # .x......
                # ...X.... <-
            edellinen = kaivetaan_x
            todelliset_komponentit += 1

        self.etsija.etsi_komponentit()
        loydetyt_komponentit = len(self.luolasto.komponentit)

        self.assertEqual(loydetyt_komponentit, todelliset_komponentit)
