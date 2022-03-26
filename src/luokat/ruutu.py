class Ruutu:
    def __init__(self, tyyppi: str = None):
        self._tyyppi = tyyppi
        self._sisalto = None
        self._naapurit = [None for _ in range(8)]
        # naapurit:
        #
        # 035
        # 1.6
        # 247


    @property
    def tyyppi(self):
        return self._tyyppi

    @tyyppi.setter
    def tyyppi(self, tyyppi: str):
        self._tyyppi = tyyppi

    @property
    def sisalto(self):
        return self._sisalto

    @sisalto.setter
    def sisalto(self, sisalto):
        self._sisalto = sisalto

    def __str__(self):
        if self._sisalto:
            return str(self._sisalto)

        if not self._tyyppi:
            return ' '

        if self._tyyppi == 'seinä':
            return seinan_esitys(self)
        
        tyyppien_esitykset = {'kallio': '#',
                              'lattia': '.',
                              'käytävä': '▒'}
        
        return tyyppien_esitykset[self._tyyppi]

if __name__ == "__main__":
    r = Ruutu('lattia')
    print(r.tyyppi)
    r.tyyppi = 'kallio'
    print(r.tyyppi)
    print(r)
    r.sisalto = 'o'
    print(r)

