# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 21:44:26 2017

@author: vishay
"""

def create_ht(ht_size):
   """ 
   Returns an empty hash table of size ht_size.

   Arguments:
   ht_size - the length of the hash table
   

   Returns:
   A hash table containing ht_size empty chains (lists).
   """
   hash_table = []
   for idx in xrange(ht_size):
       hash_table.append([])
   return hash_table

def add_ht(ht,key,value):
   """
   Adds to key/value pair to the hash table ht.
   If the key is already in the hash table, replace its old value with the new.

   Arguments:
   ht - the hash table
   key - the key of the key value pair to store
   value - the value of the key value pair to store
   """
   index = hash(key) % len(ht)
   # chain is a list of tuples
  
   chain = ht[index]
   for kvp in chain:
       if(kvp[0] == key):
           chain.remove(kvp)
           break
   # either length of chain is 0 or key val not present in ht(hash_table)[index] chain
   # chain is a list that has a reference in ht[index] so any change to chain
   # will change update ht[index]
   chain.append((key,value))
   
def remove_ht(ht, key):
    """
    Removes a key's value from the hash table.
    If no key is found in the table, no action is taken.
    
    Arguments:
    key - the key to search for in the hash table
    """  
    index = hash(key) % len(ht)
    chain = ht[index]
    for kvp in chain:
        if(kvp[0] == key):
            chain.remove(kvp)
            return

def lookup_ht(ht,key):
   """ 
   Returns the value associated with the key in the hash table ht.
   If the key is not present, raise an error.

   Returns:
   The value associated with the given key.
   """
   index = hash(key) % len(ht)
   chain = ht[index]
   for kvp in chain:
       if(kvp[0] == key):
           return kvp[1]
   raise Exception("Key not Found in the Hash Table.")

def contains_key_ht(ht, key):
    """
    Tests whether a given key is contained in a hash table.

    Arguments:
    ht - the hash table
    key - the key to search for within the hash table

    Returns:
    True if the key is found, false otherwise.
    """
    index = hash(key) % len(ht)
    chain = ht[index]
    for kvp in chain:
        if(kvp[0] == key):
            return True
    return False
    
    
import time

def ht_test(n,size):
    """
    Computes search time for the nth element of hash table.

    Arguments:
    n - the number of elemements in the table.
    size - the size of the table

    Returns:
    The lookup time in seconds.
    """

    ht = create_ht(size)

    for i in xrange(n):
        add_ht(ht, i, i)

    start = time.clock()
    lookup_ht(ht, n-1)
    stop = time.clock()
    return stop - start

def list_test(n):
    """
    Computes search time for the nth element of a list.

    Arguments:
    n - the number of elemements in the list.

    Returns:
    The lookup time in seconds.
    """

    lst = []

    for i in xrange(n):
        lst.append(i)

    start = time.clock()
    lst.index(n-1)
    stop = time.clock()
    return stop - start
    
def run_timing():
    """
    Compare speed of list search to hash table lookup
    """
    print "Time for hash table lookup is", ht_test(1000000, 100000)
    print "Time for list search is", list_test(1000000)
    
run_timing()

def rehash_ht(ht, size):
    """
    Rehashes the given hash table in place to a new table size.

    Arguments:
    ht - the hash table to modify
    size - the new hash table size
    """
    
    # copy kvp into a set
    kvps = set()
    
    while len(ht)>0:
        chain = ht.pop()
        while(len(chain)>0):
            kvps.add(chain.pop())
        
    
    #inc_ht = size - len(ht)
    for _ in xrange(size):
        ht.append([])
    
    # start in place rehashing 
    for kvp in kvps:
        add_ht(ht, kvp[0], kvp[1])
           


def rehash_ht2(ht, size):
    """
    Rehashes the given hash table in place to a new chain size.

    Arguments:
    ht - the hash table to modify
    size - the new hash table size
    """

    kvps = set()

    while len(ht) > 0:
        chain = ht.pop()
        while len(chain) > 0:
            kvps.add(chain.pop())

    for i in xrange(size):
        ht.append([])

    for kvp in kvps:
        add_ht(ht, kvp[0], kvp[1])
        

ht = create_ht(10)

for i in xrange(6):
    add_ht(ht, str(i), i)
    

#print "before rehash 1"
#print ht
rehash_ht(ht,20)

print "after rehash 1"
print ht


ht2 = create_ht(10)

for i in xrange(6):
    add_ht(ht2, str(i), i)
#print "before rehash 2"
#print ht2
rehash_ht2(ht2,20)

print "after rehash 2"
print ht2

print "contains ht 5"
print contains_key_ht(ht2,"5")

print "lookup ht"
print lookup_ht(ht2,'5')

print "clear ht"
for i in xrange(6):
    remove_ht(ht2, str(i))
print ht2
print "contains ht 5"
print contains_key_ht(ht2,"5")
print "lookup ht"
print lookup_ht(ht2,'5')