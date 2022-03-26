from luokat.luolasto import LATTIA, SEINA, RUUTUTYYPIT, Luolasto

def merkkaa(y, x, luolasto: Luolasto):
    ruutu = luolasto.kartta[y][x]

    if ruutu == LATTIA:
        return '.'

    if ruutu == 'o':
        return 'o'

    naapurit = [(-1,-1), (0,-1), (1, -1),
                (-1, 0), (1, 0),
                (-1, 1), (0, 1), (1, 1)]

    if ruutu == SEINA:
        # onko kiveä?
        naapurit_yht = 0
        naapurit_seinaa = 0
        naapurit_lattiaa = []
        naapurit_seinaa_lista = []
        for indeksi, naapuri in enumerate(naapurit):
            if y + naapuri[0] >= 0 and y + naapuri[0] < luolasto.korkeus:
                if x + naapuri[1] >= 0 and x + naapuri[1] < luolasto.leveys:
                    naapurit_yht += 1
                    if not luolasto.kartta[y+naapuri[0]][x+naapuri[1]] == LATTIA:
                        naapurit_seinaa += 1
                        naapurit_seinaa_lista.append(indeksi)
                    else:
                        naapurit_lattiaa.append(indeksi)

        if naapurit_yht == naapurit_seinaa:
            return ' '

# naapurit:
# 035
# 1.6
# 247

# jos ylävasemmalla ei seinää mutta kaikki muut seinää:
#   ┘
# sama kaikille diagonaaleille

        if naapurit_lattiaa == [0]:
            return '┘'
        if naapurit_lattiaa == [2]:
            return '┐'
        if naapurit_lattiaa == [5]:
            return '└'
        if naapurit_lattiaa == [7]:
            return '┌'

# Jos ei seinää ylävasemmalla eikä yläoikealla mutta kyllä
# vasemmalla oikealla ja ylhäällä:
#   ┴
# sama * neljä suuntaa
        if 0 in naapurit_lattiaa and 5 in naapurit_lattiaa:
            if 1 in naapurit_seinaa_lista and 3 in naapurit_seinaa_lista and 6 in naapurit_seinaa_lista:
                return '┴'

        if 2 in naapurit_lattiaa and 7 in naapurit_lattiaa:
            if 1 in naapurit_seinaa_lista and 4 in naapurit_seinaa_lista and 6 in naapurit_seinaa_lista:
                return '┬'
        
        if 5 in naapurit_lattiaa and 7 in naapurit_lattiaa:
            if 3 in naapurit_seinaa_lista and 4 in naapurit_seinaa_lista and 6 in naapurit_seinaa_lista:
                return '├'

        if 0 in naapurit_lattiaa and 2 in naapurit_lattiaa:
            if 3 in naapurit_seinaa_lista and 4 in naapurit_seinaa_lista and 1 in naapurit_seinaa_lista:
                return '┤'


# Jos ei seinää alhaalla eikä vasemmalla mutta kyllä ylhäällä ja oikealla:
#   └
        if 4 in naapurit_lattiaa and 1 in naapurit_lattiaa:
            if 3 not in naapurit_lattiaa and 6 not in naapurit_lattiaa:
                return '└'

# Jos ei seinää ylhäällä eikä vasemmalla mutta kyllä alhaalla ja oikealla:
#   ┌
        if 3 in naapurit_lattiaa and 1 in naapurit_lattiaa:
            if 4 not in naapurit_lattiaa and 6 not in naapurit_lattiaa:
                return '┌'

# Jos ei seinää ylhäällä eikä oikealla mutta kyllä alhaalla ja vasemmalla:
#   ┐
        if 3 in naapurit_lattiaa and 6 in naapurit_lattiaa:
            if 4 not in naapurit_lattiaa and 1 not in naapurit_lattiaa:
                return '┐'

# Jos ei seinää alhaalla eikä oikealla mutta kyllä ylhäällä ja vasemmalla:
#   ┘
        if 4 in naapurit_lattiaa and 6 in naapurit_lattiaa:
            if 3 not in naapurit_lattiaa and 1 not in naapurit_lattiaa:
                return '┘'


# Jos seinää kaikissa pääsuunnissa paitsi yhdessä:
#   ┴ * neljä suuntaa
# naapurit:
# 035
# 1.6
# 247
        if 1 in naapurit_seinaa_lista and 4 in naapurit_seinaa_lista and 6 in naapurit_seinaa_lista:
            if 3 not in naapurit_seinaa_lista:
                return '┬'
# naapurit:
# 035
# 1.6
# 247
        if 1 in naapurit_seinaa_lista and 4 in naapurit_seinaa_lista and 3 in naapurit_seinaa_lista:
            if 6 not in naapurit_seinaa_lista:
                return '┤'
# naapurit:
# 035
# 1.6
# 247
        if 4 in naapurit_seinaa_lista and 6 in naapurit_seinaa_lista and 3 in naapurit_seinaa_lista:
            if 1 not in naapurit_seinaa_lista:
                return '├'
# naapurit:
# 035
# 1.6
# 247
        if 1 in naapurit_seinaa_lista and 6 in naapurit_seinaa_lista and 3 in naapurit_seinaa_lista:
            if 4 not in naapurit_seinaa_lista:
                return '┴'

# nyt pitäisi olla jäljellä enää suorien seinien paikat
# eli jos seinää vasemmalla tai oikealla:
#   ─
# ja jos seinää ylä-tai alapuolella:
#   │
        if 1 in naapurit_seinaa_lista or 6 in naapurit_seinaa_lista:
            return '─'

        if 3 not in naapurit_lattiaa or 4 not in naapurit_lattiaa:
            return '│'

    # print('ei osaa päättää, ruutu', x, y)
    # print(f'naapurit seinää: {naapurit_seinaa_lista}')
    # print(f'naapurit lattiaa: {naapurit_lattiaa}')
    # quit()
    return '│'

def stilisoi(luolasto: Luolasto):
    merkatut = 0
    tuloste = [[' ' for _ in range(luolasto.leveys)] for _ in range(luolasto.korkeus)]
    merkattu = [[False for _ in range(luolasto.leveys)] for _ in range(luolasto.korkeus)]
    for y in range(luolasto.korkeus):
        for x in range(luolasto.leveys):
            if not merkattu[y][x]:
                tuloste[y][x] = merkkaa(y, x, luolasto)
                if tuloste[y][x] in [' ', '┐', '└', '┘', '┌', '┬', '┴', '├', '┤', '│', '─', '.']:
                    merkattu[y][x] = True
                    merkatut += 1
                elif tuloste[y][x] == 'o':
                    continue
                else:
                    print('error')
                    tuloste[y][x] = ' '
    # for y in range(luolasto.korkeus):
    #     for x in range(luolasto.leveys):
    #         if not merkattu[y][x]:
    #             tuloste[y][x] = merkkaa(y, x, luolasto)
    #             if tuloste[y][x] in ['#', '┐', '└', '┘', '┌', '┬', '┴', '├', '┤', '│', '─', '.']:
    #                 merkattu[y][x] = True
    #                 merkatut += 1
    #             else:
    #                 # print('error')
    #                 tuloste[y][x] = ' '
    

    for rivi in tuloste:
        print(''.join(rivi))

    # print('merkattuja:', merkatut)
    # print(f'koko: {luolasto.leveys * luolasto.korkeus}')
##########
#......#.#
#........#
#........#
#######.##
#..#....##
#........#
#........#
###.####.#
##########

# esim. tämä 10*10 luola tulisi näyttää tältä:

# ASCII-koodit seinille:
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

# ┌──────┬─┐
# │......│.│
# │........│
# │........│
# ├──┬───.┌┘
# │..│....└┐
# │........│
# │........│
# └─┐.┌──┐.│
# ##└─┘##└─┘







