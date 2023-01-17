#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-only

"""
--- Day 17: Trick Shot ---

You finally decode the Elves' message. HI, the message says. You continue searching for the sleigh keys.

Ahead of you is what appears to be a large ocean trench. Could the keys have fallen into it? You'd better send a probe to investigate.

The probe launcher on your submarine can fire the probe with any integer velocity in the x (forward) and y (upward, or downward if negative) directions. For example, an initial x,y velocity like 0,10 would fire the probe straight up, while an initial velocity like 10,-1 would fire the probe forward at a slight downward angle.

The probe's x,y position starts at 0,0. Then, it will follow some trajectory by moving in steps. On each step, these changes occur in the following order:

    The probe's x position increases by its x velocity.
    The probe's y position increases by its y velocity.
    Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
    Due to gravity, the probe's y velocity decreases by 1.

For the probe to successfully make it into the trench, the probe must be on some trajectory that causes it to be within a target area after any step. The submarine computer has already calculated this target area (your puzzle input). For example:

target area: x=20..30, y=-10..-5

This target area means that you need to find initial x,y velocity values such that after any step, the probe's x position is at least 20 and at most 30, and the probe's y position is at least -10 and at most -5.

Given this target area, one initial velocity that causes the probe to be within the target area after any step is 7,2:

.............#....#............
.......#..............#........
...............................
S........................#.....
...............................
...............................
...........................#...
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTT#TT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

In this diagram, S is the probe's initial position, 0,0. The x coordinate increases to the right, and the y coordinate increases upward. In the bottom right, positions that are within the target area are shown as T. After each step (until the target area is reached), the position of the probe is marked with #. (The bottom-right # is both a position the probe reaches and a position in the target area.)

Another initial velocity that causes the probe to be within the target area after any step is 6,3:

...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT

Another one is 9,0:

S........#.....................
.................#.............
...............................
........................#......
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTT#
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT

One initial velocity that doesn't cause the probe to be within the target area after any step is 17,-4:

S..............................................................
...............................................................
...............................................................
...............................................................
.................#.............................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT..#.............................
....................TTTTTTTTTTT................................
...............................................................
...............................................................
...............................................................
...............................................................
................................................#..............
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
..............................................................#

The probe appears to pass through the target area, but is never within it after any step. Instead, it continues down and to the right - only the first few steps are shown.

If you're going to fire a highly scientific probe out of a super cool probe launcher, you might as well do it with style. How high can you make the probe go while still reaching the target area?

In the above example, using an initial velocity of 6,9 is the best you can do, causing the probe to reach a maximum y position of 45. (Any higher initial y velocity causes the probe to overshoot the target area entirely.)

Find the initial velocity that causes the probe to reach the highest y position and still eventually be within the target area after any step. What is the highest y position it reaches on this trajectory?

Your puzzle answer was 9870.


--- Part Two ---

Maybe a fancy trick shot isn't the best idea; after all, you only have one probe, so you had better not miss.

To get the best idea of what your options are for launching the probe, you need to find every initial velocity that causes the probe to eventually be within the target area after any step.

In the above example, there are 112 different initial velocity values that meet these criteria:

23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7

How many distinct initial velocity values cause the probe to be within the target area after any step?
"""

"""
So find:
    The x velocities zeroing out on target area 
    (reverse Hase und Igel movement cost)
    and the y range (y0 - 1 .. y1 - 1)
    as first set of combinations.

    Then the x/y velocities going there in i step (grid).
    
    Then the halve x velocities (+1) and their y velocities.

    And so on. Min(x) and max(y) are known from first computation.
"""
with open('Day17-Input--Debug', 'r') as file:
#with open('Day17-Input', 'r') as file:
    line = file.read()
d0, d1, xrange, yrange = line.split()
x0, d0, x1 = xrange[2:].strip(',').split('.')
y0, d0, y1 = yrange[2:].split('.')
x0 = int(x0)    # lower bound
x1 = int(x1)    # upper bound
y0 = int(y0)    # lower bound (neg!)
y1 = int(y1)    # upper bound (neg!)
print(x0, x1)
print(y0, y1)

x_highY = []
y_highY = []
possible_x = [] # twin list with all permutations,
possible_y = [] # get value pairs by walking both at once
# ugh, actually, handle this as one set.

## the longest solutions. x*2+2 steps, the last from y=0 to target.
h = 0
for i in range(1, 1000):
    h += i
    if h >= x0:
        if h > x1:
            break
        x_highY.append(i)
for i in range(abs(y1)-1, abs(y0)):
        y_highY.append(i)
        for val in x_highY:
            possible_x.append(val)
            possible_y.append(i)

print(x_highY)
print(y_highY)

# one-step solutions
for x in range(x0, x1+1):
    for y in range(y0, y1+1):
        print('1 step', x, y)
        possible_x.append(x)
        possible_y.append(y)
print(len(possible_x))

# two-step solutions
for x in range(x0//2+1, (x1+1)//2+1):
    for y in range(y0//2+1, (y1+1)//2+1):
        print('2 steps', x, y)
        possible_x.append(x)
        possible_y.append(y)
print(len(possible_x))

# three-step solutions
for x in range(x0//3+2, x1//3+2):
    for y in range(y0//3+2, (y1+1)//3+2):
        print('3 steps', x, y)
        possible_x.append(x)
        possible_y.append(y)
print(len(possible_x))

# four-step solutions
for x in range(x0//4+2, x1//4+3):   # wrong
    for y in range(y0//4+2, y1//4+3): # wrong again
        print('4 steps', x, y)
        possible_x.append(x)
        possible_y.append(y)
print(len(possible_x))

# five-step solutions
for x in range(x0//5+2, x1//5+3):   #wrong
    for y in range(y0//5+2, y1//5+3): # allwrong
        print('5 steps', x, y)
        possible_x.append(x)
        possible_y.append(y)
print(len(possible_x))

## in the example, all that's left is numbers for which any y
## between 'high enough' and 'falling too fast' will do.

## Fix the range definitions by computing all edge cases,
## and try and find the generic formula...

checkx = []
checky = []
with open('Day17-Input--Debug_Control', 'r') as file:
    for line in file:
        x, y = line.split(',')
        checkx.append(int(x))
        checky.append(int(y))

for i in range(len(possible_x)):
    isin = False
    for j in range(len(checkx)):
        if possible_x[i] == checkx[j] and possible_y[i] == checky[j]:
            isin = True
    if not isin:
        print('Wrong value:', possible_x[i], possible_y[i])

for j in range(len(checkx)):
    isin = False
    for i in range(len(possible_x)):
        if possible_x[i] == checkx[j] and possible_y[i] == checky[j]:
            isin = True
    if not isin:
        print('Not yet covered:', checkx[j], checky[j])
       
quit()
print()
# 17.1, keep/integrate.
d0, yraw, d1 = line.split('-')
y = int(yraw[:-2])
h =  int((y-1) * y / 2)
print(h)

# 9870
