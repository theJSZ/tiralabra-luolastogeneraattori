import random
from luokat.luolasto import Luolasto

def korjattu_leveys(leveys, luolasto):
    if leveys < 3:
       return 3
    if leveys > luolasto.korkeus - 2:
       return luolasto.korkeus - 2
    return leveys

def korjattu_y(y, luolasto, leveys):        
    max_y = luolasto.korkeus - 2 - leveys // 2
    min_y = (leveys-1) // 2 + 1
    if y > max_y:
        return max_y
    if y < min_y:
        return min_y
    return y

def suunnattu_luola(luolasto: Luolasto, leveys = 3, mutkaisuus = 25, vaihtelu = 25, suunta = 1):
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
    x = 1
    # y = luolasto.korkeus // 2
    y = random.randint(1, luolasto.korkeus)    

    for x2 in range(x, luolasto.leveys-1):
        leveys = korjattu_leveys(leveys, luolasto)
        y = korjattu_y(y, luolasto, leveys)
            
        for y2 in range(y - (leveys-1)//2, y + 1 + (leveys-1)//2):
            if suunta == -1:
                luolasto.kaiva(luolasto.leveys-1-x2, y2)
            else:
                luolasto.kaiva(x2, y2)

        leveyden_muutos = (random.randint(1, 100) <= vaihtelu)
        if leveyden_muutos:
            leveys += random.choice([-2, -1, 1, 2])

        mutka = (random.randint(1, 100) <= mutkaisuus)
        if mutka:
            y += random.choice([-2, -1, 1, 2])
