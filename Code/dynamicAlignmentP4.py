"""
Created on Sun Oct 30 13:18:16 2016

@author: vishayv
python 2.7
"""

from collections import deque

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores
    diag_score, off_diag_score, and dash_score. The function 
    returns a dictionary of dictionaries whose entries are 
    indexed by pairs of characters in alphabet plus '-'. 
    The score for any entry indexed by one or more dashes is 
    dash_score. The score for the remaining diagonal entries
    is diag_score. Finally, the score for the remaining 
    off-diagonal entries is off_diag_score.
    """
    scoring_matrix = dict()
    dash_str = '-'
    all_alpha = alphabet.union(set([dash_str]))
    for let in all_alpha:
        for let2 in all_alpha:
            if let not in scoring_matrix.keys():
                scoring_matrix[let] = dict()
            if (let == dash_str or let2 == dash_str):
                scoring_matrix[let][let2] = dash_score
            elif( let == let2):
                scoring_matrix[let][let2] = diag_score
            else:
                scoring_matrix[let][let2] = off_diag_score
    
    return scoring_matrix


#score_matrix = build_scoring_matrix(set(['a','b','c']), 5, -2, -6)
#print score_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements
     share a common alphabet with the scoring matrix scoring_matrix. 
     The function computes and returns the alignment matrix for 
     seq_x and seq_y as described by the pairwise alignment algo. 
     If global_flag is True, then compute global alignment otherwise
     compute local alignment 
    """
    dash_str = '-'
    x_len = len(seq_x)
    y_len = len(seq_y)
    align_matrix = [ [0 for _ in range(y_len+1)] for _ in range(x_len+1)]
    
    for idx in range(1, x_len+1):
         val1 = align_matrix[idx-1][0] + scoring_matrix[seq_x[idx-1]][dash_str]
         align_matrix[idx][0] = 0 if (val1 < 0 and not global_flag) else val1
    for idy in range(1, y_len+1):
         val1 = align_matrix[0][idy-1] + scoring_matrix[dash_str][seq_y[idy-1]]
         align_matrix[0][idy] = 0 if (val1 < 0 and not global_flag) else val1   
         
    for idx in range(1, x_len+1):
        for idy in range(1, y_len+1):
             val1 = align_matrix[idx-1][idy-1] + scoring_matrix[seq_x[idx-1]][seq_y[idy-1]] 
             val2 = align_matrix[idx-1][idy] + scoring_matrix[seq_x[idx-1]][dash_str]
             val3 = align_matrix[idx][idy-1] + scoring_matrix[dash_str][seq_y[idy-1]]
             max_val = max(val1, val2, val3)
             align_matrix[idx][idy] = 0 if (max_val < 0 and not global_flag) else max_val
    
    return align_matrix 
 
#expected [[0, -4], [-4, 6]] but received [[0, 0], [0, 0]]    
#print compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True)   
#print compute_alignment_matrix(['a','b','c'], [1,2,3], [] , True)
 
def  compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix): 
    """
    Takes as input two sequences seq_x and seq_y whose elements share a
    common alphabet with the scoring matrix scoring_matrix. 
    This function computes a global alignment of seq_x and seq_y 
    using the global alignment matrix alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y)
    where score is the score of the global alignment align_x and align_y.
    Note that align_x and align_y should have the same length and may
    include the padding character '-'.
    """
    dash_str = '-'
    x_len = len(seq_x)
    y_len = len(seq_y)
    align_x = deque()
    align_y = deque()
    idx = x_len
    idy = y_len
    
    while idx > 0 and idy > 0:
        val1 = alignment_matrix[idx-1][idy-1] + scoring_matrix[seq_x[idx-1]][seq_y[idy-1]] 
        val2 = alignment_matrix[idx-1][idy] + scoring_matrix[seq_x[idx-1]][dash_str]
        if alignment_matrix[idx][idy] == val1:
            align_x.appendleft(seq_x[idx-1])
            align_y.appendleft(seq_y[idy-1])
            idx -= 1
            idy -= 1
        elif alignment_matrix[idx][idy] == val2:
            align_x.appendleft(seq_x[idx-1])
            align_y.appendleft(dash_str)
            idx -= 1
        else:
            align_x.appendleft(dash_str)
            align_y.appendleft(seq_y[idy-1])
            idy -= 1
            
    while idx > 0:
            align_x.appendleft(seq_x[idx-1])
            align_y.appendleft(dash_str)
            idx -= 1
    while idy > 0:
            align_x.appendleft(dash_str)
            align_y.appendleft(seq_y[idy-1])
            idy -= 1
       
    alignx = "".join(align_x)
    aligny = "".join(align_y)
    assert len(alignx) == len(aligny)
    return (alignment_matrix[x_len][y_len], alignx, aligny)
    
    
def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix.
    This function computes a local alignment of seq_x and seq_y
    using the local alignment matrix alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y)
    where score is the score of the optimal local alignment align_x
    and align_y. Note that align_x and align_y should have 
    the same length and may include the padding character '-'.
    """
    dash_str = '-'
    #x_len = len(seq_x)
    #y_len = len(seq_y)
    align_x = deque()
    align_y = deque()
    max_score, idx, idy = get_max_score_index(alignment_matrix)
    
    while idx > 0 and idy > 0 and alignment_matrix[idx][idy] != 0:
        val1 = alignment_matrix[idx-1][idy-1] + scoring_matrix[seq_x[idx-1]][seq_y[idy-1]] 
        val2 = alignment_matrix[idx-1][idy] + scoring_matrix[seq_x[idx-1]][dash_str]
        if alignment_matrix[idx][idy] == val1:
            align_x.appendleft(seq_x[idx-1])
            align_y.appendleft(seq_y[idy-1])
            idx -= 1
            idy -= 1
        elif alignment_matrix[idx][idy] == val2:
            align_x.appendleft(seq_x[idx-1])
            align_y.appendleft(dash_str)
            idx -= 1
        else:
            align_x.appendleft(dash_str)
            align_y.appendleft(seq_y[idy-1])
            idy -= 1
            
    while idx > 0 and alignment_matrix[idx][idy] != 0:
            align_x.appendleft(seq_x[idx-1])
            align_y.appendleft(dash_str)
            idx -= 1
    while idy > 0 and alignment_matrix[idx][idy] != 0:
            align_x.appendleft(dash_str)
            align_y.appendleft(seq_y[idy-1])
            idy -= 1
            
    alignx = "".join(align_x)
    aligny = "".join(align_y)
    assert len(alignx) == len(aligny)
    return (max_score, alignx, aligny)
    
def get_max_score_index(matrix):
    """
    get max score and argmax from matrix list of lists
    """
    max_num = 0    
    idx = None 
    idy = None
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if(matrix[row][col] > max_num):
                max_num = matrix[row][col]
                idx = row
                idy = col
    return (max_num, idx, idy)
    
#print get_max_score_index([[0, -4], [-4, 6]])