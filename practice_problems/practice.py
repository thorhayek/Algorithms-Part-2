# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 19:33:19 2016

@author: vishay
contains code for practice excercises.
python 2.7
"""
import urllib2
import matplotlib.pyplot as plt

#Exercise 1 - Node Count
def node_count(graph):
    """
    Returns the number of nodes in a graph.

    Arguments:
    graph -- The given graph.

    Returns:
    The number of nodes in the given graph.
    """
    return len(graph.keys())

#Exercise 2 - Edge Count

def edge_count(graph):
    """
    Returns the number of edges in a graph.

    Arguments:
    graph -- The given graph.

    Returns:
    The number of edges in the given graph.
    """
    edge_double_count = 0
    for nodeKey in graph.keys():
        edge_double_count = edge_double_count + len(graph[nodeKey])

    return edge_double_count / 2


def create_digraph():
    digraph  = {}
    for node in xrange(5):
        digraph[node] = set([node+1])
    digraph[5] = set([0])
    #digraph[4] = set([0])
    return digraph
    
test_digraph = create_digraph()
print test_digraph

def in_degree(digraph,node):

    in_degree = 0    
    for item_node in digraph:
        if(node in digraph[item_node]):
            in_degree += 1
    return in_degree
    
print in_degree(test_digraph, 0)

"""
tests
"""

digraph = {  1 : set([2]),
                 2 : set([3,4]),
                 3 : set([]),
                 4 : set([3,2]),
                 5 : set() }
                
assert in_degree(digraph, 3) == 2
assert in_degree(digraph, 4) == 1
assert in_degree(digraph, 1) == 0


def is_undirected_graph_valid(graph):
    """
    Tests whether the given graph is logically valid.

    Asserts for every unordered pair of distinct nodes {n1, n2} that
    if n2 appears in n1's adjacency set then n1 also appears in
    n2's adjacency set.  Also asserts that no node appears in 
    its own adjacency set and that every value that appears in
    an adjacency set is a node in the graph.

    Arguments:
    graph -- The graph in dictionary form to test.

    Returns:
    True if the graph is logically valid.  False otherwise.
    """
    
    # 1) every value that appears is a node in graph
    # 2) no node appears in its own adjacency list
    # 3) edge nodes in both adjacency list
    
    nodes = graph.keys()
    for node in nodes:
        edges = graph[node]
        assert node not in edges # 2
        for edge_node in edges:
            assert edge_node in nodes # 1
            assert node in graph[edge_node] #3


" tests "

graph1 = { "0" : set(["1","2"]),"1" : set(["0","2"]),"2" : set(["1","0"])}
is_undirected_graph_valid(graph1)

graph2 = { "0" : set(["1","2"]),
               "1" : set(["0","2"]),
               "2" : set(["1"]) }
#is_undirected_graph_valid(graph2) false
               
graph4 = { "0" : set(["1","2"]),
               "1" : set(["0","2"]),
               "2" : set(["1","3"]) }

#is_undirected_graph_valid(graph4)

graph5 = { "0" : set(["1"]) }
#is_undirected_graph_valid(graph5)
graph6 = { "0" : set(["0"]) }
#is_undirected_graph_valid(graph6)



"""
Popular nodes 
"""

def popular_nodes(graph):
    node_list = []
    count = edge_count(graph) *2
    avg_edge = count/len(graph)
    print "edges",avg_edge
    for node in graph.keys():
        print len(graph[node])
        if len(graph[node]) > avg_edge :
            node_list.append(node)
    return node_list

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
cite_10 = "http://storage.googleapis.com/codeskulptor-alg/random10.txt"
cite_100 = "http://storage.googleapis.com/codeskulptor-alg/random100.txt"
cite_1000 = "http://storage.googleapis.com/codeskulptor-alg/random1000.txt"
cite_10000 = "http://storage.googleapis.com/codeskulptor-alg/random10000.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(cite_100)
pop_nodes =  popular_nodes(citation_graph)
print pop_nodes
print len(pop_nodes)

import random

def plot_dice_rolls(nrolls):
    """
    Plot the distribution of the sum of two dice when they are rolled
    nrolls times.

    Arguments:
    nrolls - the number of times to roll the pair of dice

    Returns:
    Nothing
    """
    sum_val_dict = {}
    for _ in range(nrolls):
        value1 = random.randrange(1, 7)
        value2 = random.randrange(1, 7)
        sum_val = value1 + value2
        if sum_val in sum_val_dict:
            sum_val_dict[sum_val] += 1.0/nrolls
        else:
            sum_val_dict[sum_val] = 1.0/nrolls
    
    #print sum_val_dict 
    return sum_val_dict
    
vals_dict =  plot_dice_rolls(100)
#print "ans",vals_dict
xvals , yvals1 = vals_dict.keys() , vals_dict.values()
print xvals
print yvals1
def plot_2_lines(yvals1, xvals, leg_label1, x_axis_l, y_axis_l, title):
    
    #print "test"
    plt.title('Desktop python 2.7 : ' + title)
    plt.plot(xvals, yvals1, '-b', label=leg_label1)
    #plt.plot(xvals, yvals2, '-r', label=leg_label2)
    plt.xlabel(x_axis_l)
    plt.ylabel(y_axis_l)
    plt.legend(loc='upper left')
    plt.show()
    
plot_2_lines(yvals1,xvals," prob distribution 2 die sum", "coin toss sum", "probability","distribution of the sum of two die")


"""

Leap Lists using Recursion

For the leap list problem we are given a list where the last element is 0 (the goal element) and every other element is a positive integer. For example:

[1, 2, 3, 3, 3, 1, 0]
Given a starting index n for a player and a leap budget k we are asked to determine whether a player may "leap" from the starting index to the goal index in k or less leaps. By the rules of leap list however, if the player is currently at index i the player may only next leap to index i+list[i] (a right leap) or i-list[i] (a left leap) assuming that the leap would land on a valid index of the list. For example, if the player started at index 4 (which contains the value 3) their next leap could be to "leap left" to index 1 (since 4-3=1) but not to "leap right" to 7 (since 4+3=7) because this would be leaping beyond the boundary of the list. Likewise, after moving to index 1 (with value 2) the player then could then "leap right" to index 3 but not "leap left" to index -1. If the player found themselves on index 5 they could leap right to index 6 (to the goal!) or left to index 4.

Exercise 1 - Max Leaps Pseudocode

Write the pseudocode for a recursive algorithm IsGoalReachableMax that determines whether it is possible to leap from the starting position to the goal in a given number of leaps (or fewer). Once you are satisfied with your pseudo-code, you are welcome to examine our pseudo-code.
"""

def is_goal_reachable_max(leap_list, start_index, max_leaps):
    """ 
    Determines whether goal can be reached in at most max_leaps leaps.
    goal elem == 0 last elem
    Arguments:
    leap_list - the leap list game board.
    start_index - the starting index of the player.
    max_leaps - the most number of leaps allowed before the player loses.

    Returns:
    True if goal is reachable in max_leap or less leaps.  False if goal is not reachable in max_leap or fewer leaps.
    """
    num_elem = len(leap_list)
    curr_val = leap_list[start_index]
   
    if(curr_val == 0):
        return True
    if(max_leaps == 0):
        return False
        
    right_leap = start_index + curr_val
    left_leap =  start_index - curr_val
    
    
    if(right_leap < num_elem):
        if is_goal_reachable_max(leap_list, right_leap, max_leaps-1):
            return True
    elif(left_leap >= 0):
        if is_goal_reachable_max(leap_list, left_leap, max_leaps-1):
            return True
    # case when elem value is so large that both right and left leaps not possible
    return False
   

assert is_goal_reachable_max([1, 2, 3, 3, 3, 1, 0], 0, 3)
#True
assert is_goal_reachable_max([1, 2, 3, 3, 3, 1, 0], 0, 2) == False
#False
assert is_goal_reachable_max([1, 2, 3, 3, 3, 1, 0], 4, 3)
#True
assert is_goal_reachable_max([1, 2, 3, 3, 3, 1, 0], 4, 2) == False 
#False
assert is_goal_reachable_max([2, 1, 2, 2, 2, 0], 1, 5) == False
#False
assert is_goal_reachable_max([2, 1, 2, 2, 2, 0], 3, 1)
#True

visited_set = set([])
def is_goal_reachable(leap_list, start_index):
    """ 
    Determines whether goal can be reached in any number of leaps.
    goal elem == 0 last elem
    
    Arguments:
    leap_list - the leap list game board.
    start_index - the starting index of the player.

    Returns:
    True if goal is reachable.  False if goal is not reachable.
    """
    global visited_set
    visited_set.add(start_index)  
    print visited_set
    num_elem = len(leap_list)
    if(len(visited_set) == len(leap_list)):
        return False
    
    curr_val = leap_list[start_index]
    if(curr_val == 0):
        return True
    
    right_leap = start_index + curr_val
    left_leap =  start_index - curr_val
    
    if(right_leap < num_elem and right_leap not in visited_set):
         if (is_goal_reachable(leap_list, right_leap)):
             return True
    if(left_leap >= 0 and left_leap not in visited_set):
         if (is_goal_reachable(leap_list, left_leap)):
             return True
    return False

    

assert is_goal_reachable([1, 2, 3, 3, 3, 1, 0], 0)
#True

visited_set = set([])
print "new"
assert is_goal_reachable([1, 2, 3, 3, 3, 1, 0], 4)
#True

visited_set = set([])
print "new"
assert is_goal_reachable([2, 1, 2, 2, 2, 0], 1) == False
#False

visited_set = set([])
print "new"
assert is_goal_reachable([2, 1, 2, 2, 2, 0], 1) == False
#False

visited_set = set([])
print "new"
assert is_goal_reachable([2, 1, 2, 2, 2, 0], 3)
#True

visited_set = set([])
print "new"
assert is_goal_reachable([3, 6, 4, 1, 3, 4, 2, 5, 3, 0], 0)
#True
