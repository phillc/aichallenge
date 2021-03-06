#!/usr/bin/env python
import math
import random

#game parameters
possibleNoPlayers = [4, 6, 8, 9, 10, 12, 14, 15, 16]


maxDim = 100

visionRadius = 5

minWallProportion = 0.1
maxWallProportion = 0.3

minFoodProportion = 0.05
maxFoodProportion = 0.1

directions = {
    'N': (-1,0),
    'S': (1,0), 
    'E': (0,1), 
    'W': (0,-1),
}

#
#	Functions
#

#picks out region dimensions
def get_region_dimensions(noPlayers):
	s = []
	i = 2
	while i*i <= noPlayers:
		if noPlayers%i == 0:
			s.append(i)
		i = i+1
	
	m = s[random.randint(0,len(s)-1)]
	n = noPlayers/m
	return [m, n]	

#prints the map
def print_map(pMap):
	print "D", Dim[0], Dim[1], P
	for row in pMap:
		print "M " + ''.join(row)

#randomly picks a location inside the map
def pick_square():
	return [random.randint(0, sDim[0]-1), random.randint(0, sDim[1]-1)]
	
def fill_squares(loc, type):
	v = type
	for r in range(rDim[0]):
		for c in range(rDim[1]):
			map[loc[0] + r*sDim[0] ][loc[1] + c*sDim[1] ] = v
			if type == 'a':
				v = chr(ord(v)+1)

#returns the distance between two squares
def distance(loc1, loc2):
	d1 = abs(loc1[0] - loc2[0])
	d2 = abs(loc1[1] - loc2[1])
	return min(d1, Dim[0]-d1) + min(d2, Dim[1]-d2)
	
#returns the new location after moving in a particular direction
def get_loc(loc, direction):                                    
    dy, dx = directions[direction]                              
    return [(loc[0]+dy)%Dim[0], (loc[1]+dx)%Dim[1] ]


#checks whether the players can reach every non-wall square
def is_valid(startLoc):
	nMap = [ [0 for c in range(Dim[1])] for r in range(Dim[0])]
	nMap[startLoc[0] ][startLoc[1] ] = 1
	squaresVisited = 1
	
	stack = [startLoc]
	while stack != []:
		cLoc = stack.pop()
		for d in directions:
			nLoc = get_loc(cLoc, d)
			if nMap[nLoc[0] ][nLoc[1] ] == 0:
				squaresVisited += 1
				nMap[nLoc[0] ][nLoc[1] ] = 1
				if map[nLoc[0] ][nLoc[1] ] != "X":
					stack.append(nLoc)
					
	if squaresVisited == Dim[0]*Dim[1]:
		return True
	return False
	
#
#	Builds the map
#

#picks the dimensions and creates the empty map
P = possibleNoPlayers[random.randint(0, len(possibleNoPlayers)-1)]
rDim = get_region_dimensions(P)

sDim = [random.randint(10, int(maxDim/rDim[0])), random.randint(10, int(maxDim/rDim[1]))]
sDim[0] = sDim[1] = min(sDim[0], sDim[1])

Dim = [rDim[0]*sDim[0], rDim[1]*sDim[1]]
map = [ ['.' for c in range(Dim[1])] for r in range(Dim[0]) ]

#print "region dimensions: ", rDim[0], rDim[1]
#print "individual region dimensions: ", sDim[0], sDim[1]
#print "dimensions: ", Dim[0], Dim[1]

#picks out ants starting squares
p1Loc = pick_square()
fill_squares(p1Loc, 'a')

#picks out wall squares
minWallSquares = int(minWallProportion*sDim[0]*sDim[1])
maxWallSquares = int(maxWallProportion*sDim[0]*sDim[1])
noWallSquares = random.randint(minWallSquares, maxWallSquares)

nMap = [ [0 for c in range(Dim[1])] for r in range(Dim[0])]
w = 0
while w < noWallSquares:
	wSquare = pick_square()
	while map[wSquare[0] ][wSquare[1] ] != '.' or nMap[wSquare[0] ][wSquare[1] ] == 1:
		nMap[wSquare[0] ][wSquare[1] ] = 1
		wSquare = pick_square()
		
	nMap[wSquare[0] ][wSquare[1] ] = 1
		
	fill_squares(wSquare, 'X')
	if is_valid(p1Loc):
		w += 1
	else:
		fill_squares(wSquare, '.')
	
#picks out resource squares
minFoodSquares = int(minFoodProportion*sDim[0]*sDim[1])
maxFoodSquares = int(maxFoodProportion*sDim[0]*sDim[1])
noFoodSquares = random.randint(minFoodSquares, maxFoodSquares)

for f in range(noFoodSquares):
	gSquare = pick_square()
	while map[gSquare[0] ][gSquare[1] ] != '.' or distance(p1Loc, gSquare) < 4:
		gSquare = pick_square()
		
	fill_squares(gSquare, '*')
	
#prints the map
print_map(map)
