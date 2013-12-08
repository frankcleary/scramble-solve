# -*- coding: utf-8 -*-
"""
Created on Sat Dec 07 13:49:50 2013

Find words in an n by n grid of letters where a word can be made by joining
letters adjacent or diagonal to one another, without reuse. Prompts user for
the n, size of the grid, and for each row of letters.

@author: Frank Cleary
"""

WORDFILE = 'words.txt'

def neighbors(GRIDSIZE):
    """Return a dictionary of neighboring points where the key is the point in
    question and the value is a list of neightboring points.
    
    GRIDSIZE: an integer defining the size of one size of the grid.
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
    """Return a set object made of the words in WORDFILE, a file with one
    word per line.
    
    WORDFILE: A string of the the file's location
    """
    with open(WORDFILE) as wordfile:
        wordset = set([s.strip() for s in wordfile.readlines()])
    return wordset
    
def makestartdict(wordset, GRIDSIZE):
    """Return a dictionary where each key is a integer, n, and each value
    is a set containing all the length n permutations of letters appear at the
    start of the words in wordset.
    
    wordset: A set object of words
    GRIDSIZE: n will range from 1 to GRIDSIZE**2 - 1
    """
    startdict = {length : None for length in range(1, GRIDSIZE**2)}
    for length in startdict.keys():
        starters = [w[0:length] for w in wordset if len(w) > length]
        startdict[length] = set(starters)
    return startdict

def checkpath(path, grid, neighbordict, wordset, startdict, answords):
    """If the letters at the positions defined by path are a word, add to
    answords, if the letters form the start of a word, call checkpath
    (this function) on the possible extensions of the path, if no words start
    with the letters, return None.
    
    Example: If path = [1, 5, 6] and grid = 'ratsadtscatstags' pathword will be
    'rad', 'rad' will be added to answords if it's a legal word, and all the 
    letters next to point 6 on the grid that are not already in the path will 
    be appended to the path and checkpath will be called on this new path. If
    no legal words begin with 'rad', None will be returned.
    
    path: a list of ints defining the path through the grid
    grid: a string defining the letters on the grid (grid = row1 + row2 + ...)
    neighbordict: a dictionary whose values are lists of all the neighboring 
        points the point n, where n is the key. Made by the neighbors function
    wordset: a set of all legal words
    startdict: a dictionary with keys n whose values are sets of all the length
        n permutations of letters that form the start of words. Made by the
        makestartdict function.
    """
    pathlist = [grid[i - 1] for i in path]
    pathword = ''.join(pathlist)
    pathword = pathword.replace('q', 'qu')
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
    """Get input from user defining the letters of an nxn grid, and find words
    made up of neighboring letters within that grid wihtout reuse, outputting 
    a list sorted by word length.
    """
    wordset = readwords(WORDFILE)
    GRIDSIZE = raw_input("What is the lenght of one size of the grid?\n")
    GRIDSIZE = int(GRIDSIZE)
    neighbordict = neighbors(GRIDSIZE)
    startdict = makestartdict(wordset, GRIDSIZE)
    grid = ''
    for i in range(GRIDSIZE):
        line = raw_input("Enter line %s:\n" % (i + 1))
        if len(line) != GRIDSIZE:
            print "Invalid line. You must enter %s letters per line" % GRIDSIZE
            return None
        grid = grid + line
    grid = grid.lower()
    answords = []
    for i in range(1, GRIDSIZE**2 + 1):
        checkpath([i], grid, neighbordict, wordset, startdict, answords)
    uniqwords = list(set(answords))
    sortedwords = sorted(uniqwords, key=len)
    print '\n'.join(sortedwords)   
       
if __name__ == "__main__":
    main()