# -*- coding: utf-8 -*-
"""
Created on Sat Dec 07 13:49:50 2013

@author: Frank
"""

GRIDSIZE = 3
WORDFILE = 'words.txt'

def neighbors(GRIDSIZE):
    """Return a dictionary of neighboring points
    where the key is the point in question and the value
    is a list of neightboring points
    """
    
    points = range(1, GRIDSIZE**2 + 1)
    neighbors = []
    neighbordict = {point : 0 for point in points}
    for point in points:
        if point % GRIDSIZE not in [0, 1]:  # middle points
            neighbors = [point + 1, 
                         point - 1, 
                         point - GRIDSIZE, 
                         point - GRIDSIZE + 1,
                         point - GRIDSIZE - 1,
                         point + GRIDSIZE,
                         point + GRIDSIZE + 1,
                         point + GRIDSIZE - 1]
        if point % GRIDSIZE == 1:  # left edge points
            neighbors = [point + 1, 
                        point - GRIDSIZE, 
                        point - GRIDSIZE + 1,
                        point + GRIDSIZE,
                        point + GRIDSIZE + 1]
        if point % GRIDSIZE == 0:  # right edge points
            neighbors = [point - 1, 
                        point - GRIDSIZE, 
                        point - GRIDSIZE - 1,
                        point + GRIDSIZE,
                        point + GRIDSIZE - 1]          
        neighbors = [n for n in neighbors
                     if n > 0 and n <= len(points)]
        neighbordict[point] = neighbors
    return neighbordict
    
def readwords(WORDFILE):
    with open(WORDFILE) as wordfile:
        wordset = set([s.strip() for s in wordfile.readlines()])
    return wordset
    
def makestartdict(wordset, GRIDSIZE):
    startdict = {length : None for length in range(1, GRIDSIZE**2)}
    for length in startdict.keys():
        starters = [w[0:length] for w in wordset if len(w) > length]
        startdict[length] = set(starters)
    return startdict

def checkpath(path, grid, neighbordict, wordset, startdict, answords):
    pathlist = [grid[i - 1] for i in path]
    pathword = ''.join(pathlist)
    if pathword in wordset:
        answords.append(pathword)
    if pathword in startdict[len(pathword)]:
        for point in neighbordict[path[-1]]:
            if point not in path:
                newpath = path + [point]
                checkpath(newpath, grid, neighbordict, 
                          wordset, startdict, answords)
    return None

def main():
    GRIDSIZE = raw_input("What is the lenght of one size of the grid?\n")
    GRIDSIZE = int(GRIDSIZE)
    grid = ''
    for i in range(GRIDSIZE):
        line = raw_input("Enter line %s:\n" % (i + 1))
        if i == 0:
            GRIDSIZE = len(line)
        if len(line) != GRIDSIZE:
            print "Invalid line. You must enter %s letters per line" % GRIDSIZE        
        grid = grid + line
    grid = grid.lower()
    neighbordict = neighbors(GRIDSIZE)
    wordset = readwords(WORDFILE)
    startdict = makestartdict(wordset, GRIDSIZE)
    answords = []
    for i in range(1, GRIDSIZE**2 + 1):
        checkpath([i], grid, neighbordict, wordset, startdict, answords)
    uniqwords = list(set(answords))
    uniqwords = sorted(uniqwords, key=len)
    print '\n'.join(uniqwords)   
       
if __name__ == "__main__":
    main()