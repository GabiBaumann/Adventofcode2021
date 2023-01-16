#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-only

"""
--- Day 15: Chiton ---

You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can barely still fit, though; the main problem is that the walls of the cave are covered in chitons, and it would be best not to bump any of them.

The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input). For example:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).

What is the lowest total risk of any path from the top left to the bottom right?
"""

from copy import copy as cp
from sys import setrecursionlimit
setrecursionlimit(100000)

def step(posy, posx, ar):
    global minrisk
    ar += grid[posy][posx]
    #print('Now', posy, posx, ar)
    if ar >= rm[posy][posx]:
        return minrisk
    elif ar > minrisk:
        rm[posy][posx] = minrisk
        return ar
    elif posx == maxx and posy == maxy:
        print('At end', minrisk, ar)
        return ar
    rm[posy][posx] = ar
    if posy < maxy:
        rv = step(posy+1, posx, ar)
        if rv < minrisk:
            minrisk = rv
    if posx < maxx:
        rv = step(posy, posx+1, ar)
        if rv < minrisk:
            minrisk = rv
    if posy > 0:
        rv = step(posy-1, posx, ar)
        if rv < minrisk:
            minrisk = rv
    if posx > 0:
        rv = step(posy, posx-1, ar)
        if rv < minrisk:
            minrisk = rv
    return minrisk


grid = []
rm = []
minrisk = 100000000000

#with open('Day15-Input--Debug', 'r') as file:
with open('Day15-Input', 'r') as file:
    for line in file:
        row = []
        for char in line.strip():
            row.append(int(char))
        grid.append(row)

maxy = len(grid) - 1
maxx = len(row) - 1

row = []
for i in range(maxx+1):
    row.append(minrisk)
for i in range(maxy+1):
    rm.append(cp(row))

posx = 0
posy = 0
step(posy, posx, 0)
minrisk -= grid[0][0]
print(minrisk)

# 613
