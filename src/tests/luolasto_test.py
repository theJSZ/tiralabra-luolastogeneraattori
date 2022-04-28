import unittest
from luokat.luolasto import Luolasto
from luokat.huone import Huone

class TestLuolasto(unittest.TestCase):
    def setUp(self):
        self.L = Luolasto(19, 77)

    def test_luolaston_koko(self):
        self.assertEqual(self.L.korkeus, 19)
        self.assertEqual(self.L.leveys, 77)

    def test_kaiva(self):
        self.L.kaiva(1, 1)
        self.assertEqual(self.L.kartta[1][1].tyyppi, 'lattia')

    def test_kaiva_huone(self):
        H = Huone(1, 1, 3, 2)
        
        self.L.kaiva_huone(H)
        for y in range(1, 4):
            for x in range(1, 3):
                self.assertEqual(self.L.kartta[y][x].tyyppi, 'lattia')

    def test_kaiva_seinallinen_huone(self):
        H = Huone(1, 1, 4, 4)
        
        self.L.kaiva_seinallinen_huone(H)
        seinaruudut = [(1,1),(1,2),(1,3),(1,4),
                       (2,1),(2,4),
                       (3,1),(3,4),
                       (4,1),(4,2),(4,3),(4,4)]

        lattiaruudut = [(2,2),(2,3),
                        (3,2),(3,3)]

        for ruutu in seinaruudut:
            self.assertEqual(self.L.kartta[ruutu[0]][ruutu[1]].tyyppi, 'seinä')
        for ruutu in lattiaruudut:
            self.assertEqual(self.L.kartta[ruutu[0]][ruutu[1]].tyyppi, 'lattia')

    def test_etsi_seinat(self):
        self.L.kaiva(9, 9)
        self.L.maarita_naapurit()
        self.L.etsi_seinat()

        naapurit = []

        # käydään läpi ruudun (9,9) ympäröivät ruudut
        for y in range(8, 11):
            for x in range(8, 11):
                if y == 9 and x == 9:
                    continue
                naapurit.append(self.L.kartta[y][x].tyyppi)

        self.assertEqual(naapurit, ['seinä' for _ in range(8)])