#!/usr/bin/env python3
from paint import paint
import sys
from time import sleep
import numpy as np
"""
# Sample format to answer pattern questions 
# assuming the pattern would be frag0:
..*
**.
.**
#############################################
# Reread the instructions for assignment 1: make sure
# that you have the version with due date SUNDAY.
# Every student submits their own assignment.
* Delete the names and ccids below, and put
# the names and ccids of all members of your group, including you. 
# name                         ccid

Farish Punjani                 fpunjani
Yash Patel                     ypatel2
Payas Singh                    payas
Akhilesh Patel                 ak2

#############################################
# Your answer to question 1-a:
Glider Pattern
. * .
. . *
* * *
#############################################
# Your answer to question 1-b:
Glider Gun pattern
#############################################
# Your answer to question 2:
A)
With num_numbrs, you could calculate the number of live neighbours the selected cell would have. Using this, you could determine if a cell was eligible for one of the 3 categories - survival, death, giving birth. But in life-np.py, it was replaced with having the num_nbrs function implemented inside the next_state function.

B)
life.py implements the pad() function to get an infinite grid. It avoids the possibility of any boundary collisions. It checks if the first and last row are filled up; if yes, it will add an extra row or column to avoid any collisions.

C)

The guards help us in skipping the step to check if the index is trying to go out of bounds while we check for live neighbours.


#############################################
# Follow the assignment 1 instructions and
# make the changes requested in question 3.
# Then come back and fill in the answer to
# question 3-c:
Final pattern - Sum of secret numbers(09+92+44+39) = Number of iterations 184

..............
.....*........
......*.......
....***.......
..............

#############################################
"""
"""
based on life-np.py from course repo
"""


PTS = '.*#'
DEAD, ALIVE, WALL = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[WALL]


def point(r, c, cols): return c + r*cols

"""
board functions
  * represent board as 2-dimensional array
"""


def get_board():
    B = []
    print(sys.argv[1])
    with open(sys.argv[1]) as f:
        for line in f:
            B.append(line.rstrip().replace(' ', ''))
        rows, cols = len(B), len(B[0])
        for j in range(1, rows):
            assert(len(B[j]) == cols)
        return B, rows, cols


def convert_board(B, r, c):  # from string to numpy array
    A = np.zeros((r, c), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if B[j][k] == ACH:
                A[j, k] = ALIVE
    return A


def expand_grid(A, r, c, t):  # add t empty rows and columns on each side
    N = np.zeros((r+2*t, c+2*t), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if A[j][k] == ALIVE:
                N[j+t, k+t] = ALIVE
    return N, r+2*t, c+2*t


def print_array(A, r, c):
    print('')
    for j in range(r):
        out = ''
        for k in range(c):
            out += ACH if A[j, k] == ALIVE else DCH
        print(out)


def show_array(A, r, c):
    for j in range(r):
        line = ''
        for k in range(c):
            line += str(A[j, k])
        print(line)
    print('')


""" 
Conway's next-state formula
"""


def next_state(A, r, c):
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = 0
            if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
                num += 1
            if j > 0 and A[j-1, k] == ALIVE:
                num += 1
            if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
                num += 1
            if k > 0 and A[j, k-1] == ALIVE:
                num += 1
            if k < c-1 and A[j, k+1] == ALIVE:
                num += 1
            if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
                num += 1
            if j < r-1 and A[j+1, k] == ALIVE:
                num += 1
            if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
                num += 1
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed


#############################################
""" 
Provide your code for the function 
next_state2 that (for the usual bounded
rectangular grid) calls the function num_nbrs2,
and delete the raise error statement:
"""


def next_state2(s, cols):
    new = ''
    for j in range(len(s)):
        ch = s[j]
        if ch == GCH:
            new += GCH
        else:
            m = num_nbrs(s, j, cols, ACH)
            if ch == ACH:
                new += ACH if m > 1 and m < 4 else DCH
            else:
                new += ACH if m == 3 else DCH
    return new
    #raise NotImplementedError()
#############################################


#############################################
""" 
Provide your code for the function 
num_nbrs2 here and delete the raise error
statement:
"""


def num_nbrs2(s, j, cols, ch):
    num = 0
    if s[j-(cols+1)] == ch:
        num += 1
    if s[j - cols] == ch:
        num += 1
    if s[j-(cols-1)] == ch:
        num += 1
    if s[j-1] == ch:
        num += 1
    if s[j+1] == ch:
        num += 1
    if s[j+(cols-1)] == ch:
        num += 1
    if s[j + cols] == ch:
        num += 1
    if s[j + cols+1] == ch:
        num += 1
    return num
    #raise NotImplementedError()
#############################################


#############################################
""" 
Provide your code for the function 
next_state_torus here and delete the raise 
error statement:
"""


def next_state_torus(A,r,c):

    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = num_nbrs_torus(A,r,c,j,k)
	    
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed
#############################################


#############################################
""" 
Provide your code for the function 
num_nbrs_torus here and delete the raise 
error statement:
"""


def num_nbrs_torus(A,r,c,j,k):
    
    num=0

    rowout=j+1
    colout=k+1
 
    
    #To tackle the boundary-wrapped nature of a torus, we change any out-of-index bound situations
    if k == c-1:
        colout=0
    if j==r-1:
        rowout=0

    if  A[j-1,k-1] == ALIVE:
        num += 1
    if  A[j-1, k] == ALIVE :
        num += 1
    if  A[j-1, colout]==ALIVE:
        num += 1
    if  A[j, k-1] == ALIVE:
        num += 1
    if  A[j, colout] == ALIVE :
        num += 1
    if  A[rowout, k-1] == ALIVE:
        num += 1
    if  A[rowout, k] == ALIVE:
        num += 1
    if  A[rowout, colout] == ALIVE:
        num += 1

    return num
#############################################


"""
input, output
"""

pause = 0.2

#############################################
""" 
Modify interact as necessary to run the code:
"""
#############################################


def interact(max_itn):
    itn = 0
    B, r, c = get_board()
    print(B)
    X = convert_board(B, r, c)
    A, r, c = expand_grid(X, r, c, 0)
    print_array(A, r, c)
    while itn <= max_itn:
        sleep(pause)
        newA, delta = next_state_torus(A,r,c)
        if not delta:
            break
        itn += 1
        A = newA
        print_array(A, r, c)
    print('\niterations', itn)


def main():
    interact(183)


if __name__ == '__main__':
    main()
