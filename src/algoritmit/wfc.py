import random
from time import sleep

class Positio:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.vaihtoehdot = []
        self.valmis = False

    def __lt__(self, toinen):
        return self.vaihtoehdot < toinen.vaihtoehdot

    def __str__(self):
        return f'{self.y}, {self.x}: vaihtoehtoja {len(self.vaihtoehdot)}'

def lukitse(kuvio, positio: Positio, output):
    y = positio.y
    x = positio.x
    for kuvio_y, rivi in enumerate(kuvio):
        for kuvio_x, merkki in enumerate(rivi):
            output[y+kuvio_y][x+kuvio_x] = merkki

def valmis(output):
    for rivi in output:
        for merkki in rivi:
            if merkki == '?':
                return False
    return True

def sopii(positio: Positio, kuvio, output):
    y = positio.y
    x = positio.x

    for kuvio_y, rivi in enumerate(kuvio):
        for kuvio_x, merkki in enumerate(rivi):
            # print(f'merkki: "{merkki}", ehdolla paikkaan "{output[y+kuvio_y][x+kuvio_x]}"')
            if output[y+kuvio_y][x+kuvio_x] not in ['?', merkki]:
                # print('ei sovi')
                return False
    # print('sopii')
    return True

def peilaa(kuvio):
    uusi_kuvio = []
    for rivi in kuvio:
        uusi_rivi = rivi[::-1]
        uusi_kuvio.append(uusi_rivi)
    return uusi_kuvio
    
def kaanna(kuvio):
    uusi_kuvio = ['' for _ in range(len(kuvio))]
    for kuvio_y, rivi in enumerate(kuvio):
        for kuvio_x, merkki in enumerate(rivi):
            uusi_kuvio[len(rivi)-1-kuvio_x] += merkki

    return uusi_kuvio

# input = ['┌─┬┐    ',
#          '└┐└┼─┐  ',
#          ' └─┴┐│  ',
#          '    └┘  ',
#          '        ',
#          '    *   ',
#          '        ',
#          '        ']

input = ['           ',
         '           ',
         '           ',
         '           ',
         '           ',
         '   #####   ',
         '   #####   ',
         '   ## ##   ',
         '   #####   ',
         '   #####   ',
         '           ']


# input = ['           ',
#          '          #',
#          '         # ',
#          '#       #  ',
#          ' #     #   ',
#          '  #   #    ',
#          '   # #     ',
#          '    #      ',
#          '   #       ',
#          '  #        ',
#          ' #         ']

# input = ['     ',
#          '     ',
#          ' ### ',
#          '     ',
#          '     ']
N = 5
kuviot = []

for _ in range(4):
    input = kaanna(input)
    for _ in range(2):
        input = peilaa(input)
        for y in range(-2, len(input)-(N-1)):
            for x in range(-2, len(input[y])-(N-1)):
                kuvio = []
                for y2 in range(N):
                    rivi = ''
                    for x2 in range(N):
                        rivi += input[y+y2][x+x2]
                    kuvio.append(rivi)
                kuviot.append(kuvio)

# for indeksi, kuvio in enumerate(kuviot):
#     print(f'kuvio {indeksi+1}:')
#     for rivi in kuvio:
#         print(f"'{rivi}'")
# quit()
# 77*19, 'Nethack-standardi'
output = [['?' for _ in range(35)] for _ in range(10)]

# luo positiot
positiot = []
for y in range(len(output)-(N-1)):
    for x in range(len(output[y])-(N-1)):
        positio = Positio(y, x)
        # positio.vaihtoehdot = len(kuviot)
        positiot.append(positio)

# tarkista kuinka monta vaihtoehtoa on jäljellä kullekin
# positiolle tulosteessa, arvo käsiteltäväksi yksi niistä
# joilla vähiten
i = 1
while not valmis(output):
    # print(f'iteraatio {i}')
    i += 1
    
    for positio in positiot:
        if not positio.valmis:
            positio.vaihtoehdot = []
            for kuvio in kuviot:
                if sopii(positio, kuvio, output):
                    positio.vaihtoehdot.append(kuvio)
        if positio.valmis:
            positiot.remove(positio)
    
    random.shuffle(positiot)
    positiot2 = []
    for positio in positiot:
        if len(positio.vaihtoehdot) > 0:
            positiot2.append(positio)
    positiot2.sort()

    kohdepositio = positiot2[0]            

# arvo käsiteltävälle positiolle yksi
# mahdollisista vaihtoehdoista
    print(f'kohdepositio: {kohdepositio}')
    kohdekuvio = random.choice(kohdepositio.vaihtoehdot)
    lukitse(kohdekuvio, kohdepositio, output)
    kohdepositio.valmis = True

    for rivi in output:
        print(''.join(rivi))
    print()
    # sleep(2)


# ─ 2500
# │ 2502
# ┌ 250C
# ┐ 2510
# └ 2514
# ┘ 2518
# ├ 251C
# ┤ 2524
# ┬ 252C
# ┴ 2534
# ┼ 253C