import random
from heapq import heappop, heappush

class Node:
    def __init__(self, y, x):
        self.y = y
        self.x = x
    
    def __repr__(self):
        return f'({self.y}, {self.x})'

def build_map(map_h, map_w):
    map = ['#'*(map_w+2)]
    for _ in range(map_h):
        map_row = '#'
        for _ in range(map_w):
            map_row += random.choice(['.', '#'])
        map.append(map_row + '#')
    map.append('#'*(map_w+2))
    return map

def print_map(map):
    for row in map:
        print(row)

def get_h_values(map):
    map_h = len(map)
    map_w = len(map[0])
    return [[abs(x-(map_w-2))+abs(y-(map_h-2)) for x in range(map_w)] for y in range(map_h)]

if __name__ == "__main__":
    map_w = 4
    map_h = 4
    map = build_map(map_h, map_w)
    goal = (map_h, map_w)
    print_map(map)

    graph = []
    distance = [[float('inf') for _ in range(map_w+1)] for _ in range(map_h+1)]
    visited = [[False for _ in range(map_w+1)] for _ in range(map_h+1)]
    

    for y in range(1, map_h+1):
        for x in range(1, map_w+1):
            distance[y][x] = float('inf')
            node = Node(y, x)
            n1 = Node(y-1, x)
            n2 = Node(y+1, x)
            n3 = Node(y, x-1)
            n4 = Node(y, x+1)

            for n in [n1, n2, n3, n4]:
                if map[n.y][n.x] == '#':
                    weight = 100
                if map[n.y][n.x] == '.':
                    weight = 1

                graph.append(((node.y, node.x), n, weight))

    h_values = get_h_values(map)

    heap = []
    heappush(heap, (0, (1, 1)))

    came_from = {}
    distance[1][1] = 0
    f_values = [[float('inf') for _ in range(len(h_values[0]))] for _ in range(len(h_values))]
    f_values[1][1] = h_values[1][1]

    while len(heap) > 0:
        curr = heappop(heap)
        y, x = curr[1][0], curr[1][1]
        if h_values[y][x] == 0:
            print('found route')
            # do stuff to extract path
        n1 = (y-1, x)
        n2 = (y+1, x)
        n3 = (y, x-1)
        n4 = (y, x+1)

        for next in [n1, n2, n3, n4]:
            n_y, n_x = next[0], next[1]
            # new_cost = distance[y][x] + 
        for x in graph:
            print(x[0])