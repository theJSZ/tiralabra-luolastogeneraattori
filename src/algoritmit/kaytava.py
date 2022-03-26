from heapq import heapify, heappush, heappop
import random

def kaytava(lahto_y, lahto_x, kohde_y, kohde_x, luolasto):
    painot = {'lattia': 1,
              'käytävä': 2,
              'kallio': 5,
              'seinä': 1000}
    
    reitti = []
    jono = []
    heapify(jono)



if __name__ == "__main__":
    keko = []
    heapify(keko)
    for _ in range(100):
        heappush(keko, random.randint(0, 1000))

    for _ in range(10):
        print(heappop(keko))