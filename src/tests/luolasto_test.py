import unittest
import random
from algoritmit.bsp import validi_huone
from luokat.luolasto import Luolasto
from luokat.huone import Huone

class TestLuolasto(unittest.TestCase):
    def setUp(self):
        self.L = Luolasto(19, 77)

    def test_luolaston_koko(self):
        self.assertEqual(self.L.korkeus, 19)
        self.assertEqual(self.L.leveys, 77)

    def test_kaiva(self):
        x = random.randint(1, self.L.leveys-2)
        y = random.randint(1, self.L.korkeus-2)

        self.assertEqual(self.L.kartta[y][x].tyyppi, 'kallio')
        self.L.kaiva(x, y)
        self.assertEqual(self.L.kartta[y][x].tyyppi, 'lattia')

    def test_kaiva_huone(self):
        # arvotaan huoneen sijainti ja koko
        huone_x = random.randint(1, self.L.leveys-2)
        huone_y = random.randint(1, self.L.korkeus-2)
        huone_leveys = random.randint(1, self.L.leveys-huone_x)
        huone_korkeus = random.randint(1, self.L.korkeus-huone_y)
        H = Huone(huone_y, huone_x, huone_korkeus, huone_leveys)
        
        for y in range(huone_y, huone_y+huone_korkeus):
            for x in range(huone_x, huone_x+huone_leveys):
                self.assertEqual(self.L.kartta[y][x].tyyppi, 'kallio')

        self.L.kaiva_huone(H)

        for y in range(huone_y, huone_y+huone_korkeus):
            for x in range(huone_x, huone_x+huone_leveys):
                self.assertEqual(self.L.kartta[y][x].tyyppi, 'lattia')

    def test_kaiva_seinallinen_huone(self):
        # arvotaan huoneen sijainti ja koko
        huone_x = random.randint(1, self.L.leveys-2)
        huone_y = random.randint(1, self.L.korkeus-2)
        huone_leveys = random.randint(1, self.L.leveys-huone_x)
        huone_korkeus = random.randint(1, self.L.korkeus-huone_y)
        H = Huone(huone_y, huone_x, huone_korkeus, huone_leveys)

        self.L.kaiva_seinallinen_huone(H)

        # pitäisi nyt olla seinää ja lattiaa
        for y in range(huone_y, huone_y+huone_korkeus):
            for x in range(huone_x, huone_x+huone_leveys):
                if y in [huone_y, huone_y+huone_korkeus-1] or x in [huone_x, huone_x+huone_leveys-1]:
                    self.assertEqual(self.L.kartta[y][x].tyyppi, 'seinä')
                else:
                    self.assertEqual(self.L.kartta[y][x].tyyppi, 'lattia')

    def test_etsi_seinat(self):
        # valitaan kaivettava ruutu sallituista paikoista eli ei kiinni reunassa
        kaivettava_x = random.randint(1, self.L.leveys-2)
        kaivettava_y = random.randint(1, self.L.korkeus-2)

        self.L.kaiva(kaivettava_x, kaivettava_y)
        self.L.maarita_naapurit()
        self.L.etsi_seinat()

        # käydään läpi kaivetun ruudun ympäröivät ruudut
        for y in range(kaivettava_y-1, kaivettava_y+2):
            for x in range(kaivettava_x-1, kaivettava_x+2):
                if y == kaivettava_y and x == kaivettava_x:
                    continue
                self.assertEqual(self.L.kartta[y][x].tyyppi, 'seinä')

    def test_huone_kartan_ulkopuolella_ei_validi(self):
        H = Huone(50, 50, 10, 10)  # kartan ulkopuolella
        self.assertEqual(validi_huone(H, self.L), False)

    def test_huone_kiinni_reunassa_ei_validi(self):
        H = Huone(0, 0, 10, 10)  # kiinni reunassa, ei ok
        self.assertEqual(validi_huone(H, self.L), False)

    def test_huone_kiinni_toisessa_huoneessa_ei_ok(self):
        H1 = Huone(1, 1, 3, 3)
        self.L.kaiva_huone(H1)

        H2 = Huone(4, 1, 3, 3)  # tämä huone kiinni edellisessä, ei ok
        H3 = Huone(5, 1, 3, 3)  # tämä irrallaan, ok
        
        self.assertEqual(validi_huone(H2, self.L), False)
        self.assertEqual(validi_huone(H3, self.L), True)

    def test_validi_huone(self):
        H = Huone(1, 1, 10, 10)  # ei kiinni reunassa tai toisessa huoneessa, ok
        self.assertEqual(validi_huone(H, self.L), True)

        
