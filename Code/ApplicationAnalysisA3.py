# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 19:35:52 2016

@author: vishay
python 2.7
"""

# general python lib imports
import urllib2
import random
import time
import math
from collections import deque
import matplotlib.pyplot as plt

# source imports 
import alg_cluster
import ClosestPairClustering
#import alg_project3_viz


# Efficiency Analysis 1 

def gen_random_clusters(num_clusters):

    n_fips = set([])
    n_total_pop = 1
    n_avg_risk = 0
    rand_list = [-1, 1]
    cluster_list = []

    for _ in range(num_clusters):

        rand_x = random.random() * random.choice(rand_list)
        rand_y = random.random() * random.choice(rand_list)
        cluster_list.append(alg_cluster.Cluster(n_fips, round(rand_x,2), round(rand_y,2), n_total_pop, n_avg_risk))

    return cluster_list

def compare_closest_pair_algos():

    slow_times = []
    fast_times = []
    c_size_list = []
    avg_run = 10
    
    
    for c_size in range(2,201):
        
        c_size_list.append(c_size)
        rand_clusters = gen_random_clusters(c_size)
        #slow_time_avg = [] 
        #fast_time_avg = []
        
        start_time = time.clock()
        # avg the running time of 10 runs 
        for _ in range(avg_run):
            ClosestPairClustering.slow_closest_pair(rand_clusters)
        total_time = time.clock() - start_time
        slow_times.append(total_time/float(avg_run))
        
        #calc fast closest pair execution time
        start_time = time.clock()
        # avg the running time of 10 runs 
        for _ in range(avg_run):
            ClosestPairClustering.fast_closest_pair(rand_clusters)
        total_time = time.clock() - start_time
        fast_times.append(total_time/float(avg_run))
        
    assert len(fast_times) == len(slow_times) == 199 == len(c_size_list)
    return slow_times,fast_times,c_size_list
    


def plot_2_lines(yvals1 ,yvals2, xvals, leg_label1, leg_label2, x_axis_l, y_axis_l, title):
    
    plt.title('Desktop python 2.7 : ' + title)
    plt.plot(xvals, yvals1, '-b', label=leg_label1)
    plt.plot(xvals, yvals2, '-r', label=leg_label2)
    plt.xlabel(x_axis_l)
    plt.ylabel(y_axis_l)
    plt.legend(loc='upper left')
    plt.show()


#print gen_random_clusters(10)
slow_cp,fast_cp,xvals = compare_closest_pair_algos()
title = "Comparison of running times closest pair algos as a function of clusters"
blue_plot = "slow_cp"
red_plot = "fast_cp"
y_axis_l = 'Execution time in seconds'
x_axis_l = 'Clusters'
plot_2_lines(slow_cp, fast_cp, xvals, blue_plot, red_plot, x_axis_l, y_axis_l, title)
