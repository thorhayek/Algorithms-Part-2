"""
Created on Sun Oct 30 13:18:16 2016

@author: vishayv
"""
"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import random
import alg_cluster
import time
#from alg_cluster import Cluster



######################################################
# Code for closest pairs of clusters

def min_tuple(tup_1, tup_2):
    """
    Helper function that computes the tup with the minimum dist
    
    Input: 2 three element tup of the form (d, idx1, idx2), where d is dist
    between cluster idx1 and idx2.
    
    Output: tup with the smaller "d" ( distance) element.
    
    """
   
    if(tup_1 == None and tup_2==None or (len(tup_1) == 0 and len(tup_2)==0)):
        return None
    elif(tup_2 == None or (len(tup_2) == 0)):
        return tup_1
    elif(tup_1 == None or (len(tup_1) == 0)):
        return tup_2
        
    
    if(tup_1[0] < tup_2[0]):
        return tup_1
    else:
        return tup_2

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    min_dist = float("inf")
    ans_tup = None
    for idx1 in range(len(cluster_list)):
        for idx2 in range(len(cluster_list)):
            if(idx1 != idx2 and idx1 < idx2 ):
                dist_tup = pair_distance(cluster_list,idx1,idx2)
                #print dist_tup
                dist = dist_tup[0]
                if(dist < min_dist):
                    min_dist = dist
                    ans_tup = dist_tup
                    #print "min ",ans_tup
    return ans_tup


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    
    total_points = len(cluster_list)
    
    #base case recursion
    if(total_points <= 3):
        return slow_closest_pair(cluster_list)
    
    middle_x_coord = total_points/2
    
    # create P_L and P_R
    cluster_left = cluster_list[0:middle_x_coord+1]
    left_len = len(cluster_left)
    cluster_right = cluster_list[middle_x_coord+1:]
    left_min_tup = fast_closest_pair(cluster_left)
    right_min_tup_raw = fast_closest_pair(cluster_right) 
    if(right_min_tup_raw):
        right_min_tup = (right_min_tup_raw[0], right_min_tup_raw[1] + left_len, right_min_tup_raw[2] + left_len)
    else:
        right_min_tup = tuple()
    # find min of left and right
    fast_min_tup = min_tuple(left_min_tup, right_min_tup) 
    mid = (cluster_left[-1].horiz_center() + cluster_right[0].horiz_center())/2
    closest_strip_min = closest_pair_strip(cluster_list, mid, fast_min_tup[0])
    
    # return min of closest_strip_min and fast_min
    return  min_tuple(fast_min_tup, closest_strip_min)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    # sort cluster list according to the y coordinate
    #cc_list = list(cluster_list)
    #cc_list.sort(key = lambda cluster: cluster.vert_center())
    #ll = [x for x in l if abs(x-5)<= 1]
    strip_points = [idx for idx in range(len(cluster_list)) if abs(cluster_list[idx].horiz_center()- horiz_center) < half_width]
    
    #sort strip points according to the y coordinate
    strip_points.sort(key = lambda idx: cluster_list[idx].vert_center())
    
    strip_points_len = len(strip_points)
    res_tup = (float("inf"),-1, -1)
    for point1_idx in range(strip_points_len-1):
        for point2_idx in range(point1_idx+1,min(point1_idx+4,strip_points_len)):
            dist_tup = pair_distance(cluster_list,strip_points[point1_idx], strip_points[point2_idx])
            #print dist_tup
            res_tup = min_tuple(res_tup,dist_tup)
    return res_tup
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    #num_clusters_inp = len(cluster_list)
    while(len(cluster_list) > num_clusters):
        dist_tup = fast_closest_pair(cluster_list)
        #print dist_tup
        #merge
        cluster_list[dist_tup[1]].merge_clusters(cluster_list[dist_tup[2]])
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        #remove
        del cluster_list[dist_tup[2]]
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    
    # position initial clusters at the location of clusters with largest populations
    # mu_list does not have to be a cluster , it can be list with x, y coord
    mu_list = list(cluster_list) 
    mu_list.sort(key = lambda cluster:cluster.total_population(), reverse=True)
    mu_list = mu_list[:num_clusters]
    #iterative algorithm 
    for _ in range(num_iterations):
        new_cc_lst = [alg_cluster.Cluster(set([]), 0.0, 0.0, 0, 0) for _ in range(num_clusters)]
        # for all points find idx of mu its closest to
        for idx in range(len(cluster_list)):
            cluster_idx = min_dist_idx(mu_list, cluster_list[idx])
            new_cc_lst[cluster_idx].merge_clusters(cluster_list[idx])
        # update mus 
        for idx in range(num_clusters):
            mu_list = new_cc_lst 
            
    return new_cc_lst

def min_dist_idx(cluster_list, point_cluster):
    
    """
    given a list of clusters finds and a cluster/point 
    output : the cluster idx (0 <= cluster_idx < k(num_clusters in k means) ) in the cluster list that is closest to the point
    """
    min_dist = float("inf")
    cluster_idx = -1
    for inp_cluster_idx in range(len(cluster_list)):
        dist = cluster_list[inp_cluster_idx].distance(point_cluster)
        #print dist
        if(dist < min_dist):
            min_dist = dist 
            cluster_idx = inp_cluster_idx
    #print min_dist
    return cluster_idx


#cluster0 = alg_cluster.Cluster(set([]), 0.11, 0.75, 1, 0)

#cluster1 = alg_cluster.Cluster(set([]), 0.62, 0.86, 1, 0)

#cluster2 = alg_cluster.Cluster(set([]), 0.65, 0.68, 1, 0)

#cluster3 = alg_cluster.Cluster(set([]), 0.68, 0.48, 1, 0)

#cluster4 = alg_cluster.Cluster(set([]), 0.7, 0.9, 1, 0)

#cluster5 = alg_cluster.Cluster(set([]), 0.79, 0.18, 1, 0)




#print(fast_closest_pair([cluster_1, cluster_2, cluster_3, cluster_4, cluster_5, cluster_6]))
#print(fast_closest_pair([cluster0, cluster1, cluster2, cluster3, cluster4, cluster5]))
#print(slow_closest_pair([cluster0, cluster1, cluster2, cluster3, cluster4, cluster5]))

#print "test"
#print cluster_1.distance(cluster_4)
#print cluster_4.distance(cluster_5)