# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 12:59:37 2016

@author: coursera
"""

"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import alg_cluster
import time
import matplotlib.pyplot as plt

# conditional imports
if DESKTOP:
    import ClosestPairClustering as alg_project3_solution    # desktop project solution
    import alg_clusters_matplotlib
    #import ApplicationAnalysisA3
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results

def compute_distortion(cluster_list):

    #data_table =  load_data_table(DATA_111_URL)
    #data_table = load_data_table(DATA_290_URL)
    data_table = load_data_table(DATA_896_URL)
    
    total_distortions = 0    
    for cluster_obj in cluster_list:
        total_distortions += cluster_obj.cluster_error(data_table)
    return total_distortions

def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    #data_table = load_data_table(DATA_3108_URL)
    #data_table = load_data_table(DATA_111_URL)
    #data_table = load_data_table(DATA_290_URL)
    data_table = load_data_table(DATA_896_URL)
    
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    #cluster_list = sequential_clustering(singleton_list, 9)	
    #print "Displaying", len(cluster_list), "sequential clusters"

   
    #start_time = time.clock()
    cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 9)
    #print "hierarchical:",compute_distortion(cluster_list)
    #print "time taken for plot:"+ str(time.clock() - start_time) 
    print "Displaying", len(cluster_list), "hierarchical clusters"

    #start_time = time.clock()
    #cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)
    #print "kmeans: ",compute_distortion(cluster_list)
    #print "time taken for plot:"+ str(time.clock() - start_time) 
    #print "Displaying", len(cluster_list), "k-means clusters"

            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
        
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
        #print ""
        
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers
        #print ""
 
 #run_example()
 
def compare_distortions():
    
     #data_table = load_data_table(DATA_111_URL)
     #data_table = load_data_table(DATA_290_URL)
     data_table = load_data_table(DATA_896_URL)
     dist_hierarchical = []
     dist_kmeans = []
     
     out_cluster_k = [k for k in range(6,21)]
     
     print  out_cluster_k
     
     for k in out_cluster_k:
        
        singleton_list = []
        for line in data_table:
            singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

        cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, k)
        dist_hierarchical.append(compute_distortion(cluster_list))
        
        singleton_list = []
        for line in data_table:
            singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))


        cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, k, 5)
        dist_kmeans.append(compute_distortion(cluster_list))

     return dist_hierarchical,dist_kmeans,out_cluster_k

def plot_2_lines(yvals1 ,yvals2, xvals, leg_label1, leg_label2, x_axis_l, y_axis_l, title):
    
    plt.title('Desktop python 2.7 : ' + title)
    plt.plot(xvals, yvals1, '-b', label=leg_label1)
    plt.plot(xvals, yvals2, '-r', label=leg_label2)
    plt.xlabel(x_axis_l)
    plt.ylabel(y_axis_l)
    plt.legend(loc='upper right')
    plt.show()

hierarchical_dist,kmeans_dist,xvals =  compare_distortions() 
print hierarchical_dist,kmeans_dist,xvals        
title = "Comparison of running times of clustering algos as a function of o/p clusters: Dataset 896"
blue_plot = "hierarchical"
red_plot = "kmeans"
y_axis_l = 'computed_distortion'
x_axis_l = 'Output Clusters'
plot_2_lines(hierarchical_dist, kmeans_dist, xvals, blue_plot, red_plot, x_axis_l, y_axis_l, title)





        




