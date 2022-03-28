from audioop import reverse
from heapq import heappush, heappop

#          v goal
map = ['..#.',
       '..#.',
       '###.',
       '.#..']
#       ^ start
start = (0, 1)
goal = (2, 3)

# very expensive to go through wall
weight = {'.': 1,
          '#': 100}

height = len(map)
width = len(map[0])

# heuristic
h = [[0 for _ in range(width)] for _ in range(height)]

# to store best path
via = [[None for _ in range(width)] for _ in range(height)]

# to store actual cost of travel
cost = [[10**9 for _ in range(width)] for _ in range(height)]
# which is 0 to begin with
cost[start[0]][start[1]] = 0

# build h table
for y in range(height):
    for x in range(width):
        h[y][x] = abs(goal[0] - y) + abs(goal[1] - x)

# initialize queue
queue = []
heappush(queue, (0, start))

# start the loop
while len(queue) > 0:
    at = heappop(queue)[1]
    if at == goal:
        print('found route:')
        route = [goal]

        while True:
            prev = via[at[0]][at[1]]
            route.append(prev)
            if prev == start:
                break
            at = prev

        route = route[::-1]
        print(route)
        break

    # look at neighbors
    neighs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for n in neighs:
        new_y = at[0] + n[0]
        new_x = at[1] + n[1]
        # check not out of bounds
        if new_y < 0 or new_y >= height:
            continue
        if new_x < 0 or new_x >= width:
            continue

        # not out of bounds, check prospective new cost
        prospective_cost = cost[at[0]][at[1]] + weight[map[new_y][new_x]]
        if prospective_cost < cost[new_y][new_x]:
            cost[new_y][new_x] = prospective_cost
            via[new_y][new_x] = at
            print(f'cost {prospective_cost} to {new_y, new_x} via {at}')
            heappush(queue, (cost[at[0]][at[1]] + weight[map[new_y][new_x]] + h[new_y][new_x], (new_y, new_x)))