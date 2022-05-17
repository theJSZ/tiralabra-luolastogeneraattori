"""Erilaisia luolaston toimintaan liittyviä yksikkötestejä"""
import unittest
import random
from algoritmit.bsp import validi_huone
from luokat.luolasto import Luolasto
from luokat.huone import Huone

class TestLuolasto(unittest.TestCase):
    """Testaa Luolasto-luokkaa"""
    def setUp(self):
        """Kaikissa testeissä käytetään Nethack-standardin kokoista luolastoa"""
        self.luolasto = Luolasto(19, 77)

    def test_kaiva(self):
        """Testataan että yhden ruudun kaivaminen toimii oikein"""
        ruutu_x = random.randint(1, self.luolasto.leveys-2)
        ruutu_y = random.randint(1, self.luolasto.korkeus-2)

        self.assertEqual(self.luolasto.kartta[ruutu_y][ruutu_x].tyyppi, 'kallio')
        self.luolasto.kaiva(ruutu_x, ruutu_y)
        self.assertEqual(self.luolasto.kartta[ruutu_y][ruutu_x].tyyppi, 'lattia')

    def test_kaiva_huone(self):
        """Testataan että huoneen kaivaminen toimii oikein"""
        huone_x = random.randint(1, self.luolasto.leveys-2)
        huone_y = random.randint(1, self.luolasto.korkeus-2)
        huone_leveys = random.randint(1, self.luolasto.leveys-huone_x)
        huone_korkeus = random.randint(1, self.luolasto.korkeus-huone_y)
        huone = Huone(huone_y, huone_x, huone_korkeus, huone_leveys)

        # aluksi huoneen paikalla on kalliota
        for ruutu_y in range(huone_y, huone_y+huone_korkeus):
            for ruutu_x in range(huone_x, huone_x+huone_leveys):
                self.assertEqual(self.luolasto.kartta[ruutu_y][ruutu_x].tyyppi, 'kallio')

        self.luolasto.kaiva_huone(huone)

        # kaivamisen jälkeen huone on lattiaa
        for ruutu_y in range(huone_y, huone_y+huone_korkeus):
            for ruutu_x in range(huone_x, huone_x+huone_leveys):
                self.assertEqual(self.luolasto.kartta[ruutu_y][ruutu_x].tyyppi, 'lattia')

    def test_kaiva_seinallinen_huone(self):
        """Testataan että seinällinen huone kaivetaan oikein"""
        # arvotaan huoneen sijainti ja koko
        huone_x = random.randint(1, self.luolasto.leveys-2)
        huone_y = random.randint(1, self.luolasto.korkeus-2)
        huone_leveys = random.randint(1, self.luolasto.leveys-huone_x)
        huone_korkeus = random.randint(1, self.luolasto.korkeus-huone_y)
        huone = Huone(huone_y, huone_x, huone_korkeus, huone_leveys)

        self.luolasto.kaiva_seinallinen_huone(huone)

        # pitäisi nyt olla seinää ja lattiaa
        for ruutu_y in range(huone_y, huone_y+huone_korkeus):
            for ruutu_x in range(huone_x, huone_x+huone_leveys):
                if ruutu_y in [huone_y,huone_y+huone_korkeus-1]:
                    self.assertEqual(self.luolasto.kartta[ruutu_y][ruutu_x].tyyppi, 'seinä')
                elif ruutu_x in [huone_x,huone_x+huone_leveys-1]:
                    self.assertEqual(self.luolasto.kartta[ruutu_y][ruutu_x].tyyppi, 'seinä')

                else:
                    self.assertEqual(self.luolasto.kartta[ruutu_y][ruutu_x].tyyppi, 'lattia')

    def test_etsi_seinat(self):
        """Testataan että seinien paikat löytyvät oikein"""
        # valitaan kaivettava ruutu sallituista paikoista eli ei kiinni reunassa
        kaivettava_x = random.randint(1, self.luolasto.leveys-2)
        kaivettava_y = random.randint(1, self.luolasto.korkeus-2)

        self.luolasto.kaiva(kaivettava_x, kaivettava_y)
        self.luolasto.maarita_naapurit()
        self.luolasto.etsi_seinat()

        # käydään läpi kaivetun ruudun ympäröivät ruudut
        for ruutu_y in range(kaivettava_y-1, kaivettava_y+2):
            for ruutu_x in range(kaivettava_x-1, kaivettava_x+2):
                if ruutu_y == kaivettava_y and ruutu_x == kaivettava_x:
                    continue
                self.assertEqual(self.luolasto.kartta[ruutu_y][ruutu_x].tyyppi, 'seinä')

    def test_huone_kartan_ulkopuolella_ei_validi(self):
        huone = Huone(50, 50, 10, 10)  # kartan ulkopuolella
        self.assertEqual(validi_huone(huone, self.luolasto), False)

    def test_huone_kiinni_reunassa_ei_validi(self):
        huone = Huone(0, 0, 10, 10)  # kiinni reunassa, ei ok
        self.assertEqual(validi_huone(huone, self.luolasto), False)

    def test_huone_kiinni_toisessa_huoneessa_ei_ok(self):
        huone_1 = Huone(1, 1, 3, 3)
        self.luolasto.kaiva_huone(huone_1)

        huone_2 = Huone(4, 1, 3, 3)  # tämä huone kiinni edellisessä, ei ok
        huone_3 = Huone(5, 1, 3, 3)  # tämä irrallaan, ok

        self.assertEqual(validi_huone(huone_2, self.luolasto), False)
        self.assertEqual(validi_huone(huone_3, self.luolasto), True)

    def test_validi_huone(self):
        huone = Huone(1, 1, 10, 10)  # ei kiinni reunassa tai toisessa huoneessa, ok
        self.assertEqual(validi_huone(huone, self.luolasto), True)
