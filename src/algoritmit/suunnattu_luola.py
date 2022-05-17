import random
from time import sleep
import os
from luokat.luolasto import Luolasto

def cls():
    """Tyhjentää terminaalin
    """
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def korjattu_leveys(leveys, luolasto):
    """Pakotetaan väylän leveys olemaan järkevissä rajoissa"""
    if leveys < 3:
        return 3
    if leveys > luolasto.korkeus - 2:
        return luolasto.korkeus - 2
    return leveys

def korjattu_y(kaivaja_y, luolasto, leveys):
    """Pakotetaan väylän sijainti järkeviin rajoihin"""
    max_y = luolasto.korkeus - 2 - leveys // 2
    min_y = (leveys-1) // 2 + 1
    if kaivaja_y > max_y:
        return max_y
    if kaivaja_y < min_y:
        return min_y
    return kaivaja_y

def suunnattu_luola(luolasto: Luolasto,
                    leveys = 3,
                    mutkaisuus = 25,
                    vaihtelu = 25,
                    suunta = 1,
                    visualisointi: bool = False):
    """Hyvin yksinkertainen algoritmi. Luo vahvasti yhtenäisen luolaston
    joka etenee sivusuunnassa, mutkitellen ja käytävän leveyttä vaihdellen
    annettujen parametrien mukaan satunnaisesti. Useamman kerran ajettuna
    voi luoda hienoja, kaivosmaisia karttoja:

    #############################################################################
    #..........#############.#..############.#..............#..##........#....###
    #..........#############....###########..#..................#...............#
    #...........##########........########......................................#
    #.........#....#######.....#..########..#.#########.#........#.........#....#
    #.........#................#....##..#...#.#####.....#....###....##########..#
    ######..#..#...........###..##............#####.......######...##############
    ##########.##..........####........................#.########.###############
    ##########....#......######.......#...##.......#####.#######.########.##.####
    ###########..######..#######......#...####.....#############.########.....###
    ###########..#################.......#####...##############......###........#
    ##################################....#.#.....#########.###.#....###.#......#
    ##################.##############.....#.#.....#########..............###....#
    #..###......#......##############.........###....#####......................#
    #..###...............#########....#....#.##.#....#####.#....................#
    #...........................................................#########.......#
    #.........................................................#################.#
    ##.........#.....####..............###.....#.#...........##################.#
    #############################################################################

    Lähde: http://www.roguebasin.com/index.php/Basic_directional_dungeon_generation


    Args:
        luolasto (Luolasto): Muokattava kartta
        leveys (int, optional): Käytävän leveys alussa, oletusarvo 3
        mutkaisuus (int, optional): Käytävän mutkaisuus välillä 0-100, oletus 25
        vaihtelu (int, optional): Leveyden vaihtelu välillä 0-100, oletus 25
        suunta (int, optional): 1: vasemmalta oikealle, -1: oikealta vasemmalle
    """
    kaivaja_x = 1
    kaivaja_y = random.randint(1, luolasto.korkeus)

    for x_2 in range(kaivaja_x, luolasto.leveys-1):
        leveys = korjattu_leveys(leveys, luolasto)
        kaivaja_y = korjattu_y(kaivaja_y, luolasto, leveys)

        for kaivettava_y in range(kaivaja_y - (leveys-1)//2, kaivaja_y + 1 + (leveys-1)//2):
            if suunta == 0:  # aloitus oikealta
                kaivettava_x = luolasto.leveys-1-x_2
            else:
                kaivettava_x = x_2

            if visualisointi:
                luolasto.kartta[kaivettava_y][kaivettava_x].sisalto = 'o'

            luolasto.kaiva(kaivettava_x, kaivettava_y)

        if visualisointi:
            luolasto.nayta()
            sleep(0.05)
            for y_2 in range(kaivaja_y - (leveys-1)//2, kaivaja_y + 1 + (leveys-1)//2):
                luolasto.kartta[y_2][kaivettava_x].sisalto = None

        leveyden_muutos = (random.randint(1, 100) <= vaihtelu)
        if leveyden_muutos:
            leveys += random.choice([-2, -1, 1, 2])

        mutka = (random.randint(1, 100) <= mutkaisuus)
        if mutka:
            kaivaja_y += random.choice([-2, -1, 1, 2])
