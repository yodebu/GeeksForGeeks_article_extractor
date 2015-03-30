#!/usr/bin/env python

""" 
this is the file containing functions for selecting the individuals for next pass of the genetic algorithm
individuals with most fitness values are propagated to the next phase

Author: Sourya Bhattacharyya
Dept of CSE, IIT Kharagpur
V1.0 - 06.02.2014 - basic implementation
"""


import Header
from Header import *

import TreeUtilFunc
from TreeUtilFunc import *

import Tree_Generate
from Tree_Generate import *

#-----------------------------------------
""" 
this function implementats the tournament selection procedure 
from the given input set, a subset of population is experimented to find the best (max fitness)
this process continues until the next population size is found 

parameters: 
1) orig_inp_dist_mat is the original (input) distance matrix 
2) no_of_taxa is total no of taxa
3) inp_gen_pop_treelist is the input (current) generation population (trees) in string form (newick)
4) inp_pop_size is the input population size
5) subset_size is the size of tournament pool from which the winner is to be chosen
6) next_gen_pop_size is the size of population that need to be constructed from this function
(corresponding no of trees will be included in the next_gen_pop_treelist)
next_gen_pop_size may be less than the inp_pop_size, since we do not yet account for the crossover and mutation parts
"""
def Tournament_Select(inp_gen_pop_treelist, next_gen_pop_treelist, orig_inp_dist_mat, no_of_taxa, LS_score_list, \
		      inp_pop_size, next_gen_pop_size_to_be_used):    
  count = 0
  while (count < next_gen_pop_size_to_be_used):
    # select a subset from the inp_gen_pop_treelist 
    # select first the random indices whose corresponding elements will be part of this subset
    rand_index_subset_list = random.sample(xrange(inp_pop_size), tournament_select_subset_size)  
    # check these indices and find the maximum fitness entry 
    for i in range(tournament_select_subset_size):
      if (i == 0):
	max_fitness_tree_entry = rand_index_subset_list[i]
	max_fitness_LS_val = LS_score_list[max_fitness_tree_entry][1]
      else:
	curr_tree_LS_val = LS_score_list[rand_index_subset_list[i]][1]
	if (curr_tree_LS_val < max_fitness_LS_val):
	  max_fitness_LS_val = curr_tree_LS_val
	  max_fitness_tree_entry = rand_index_subset_list[i]
    
    if (DEBUG_LEVEL > 1):
      print 'previous generation propagation - tree index: ', max_fitness_tree_entry, ' added in the position: ', count
    
    # append corresponding tree in the next generation population
    # first derive the arguments
    inp_tree = inp_gen_pop_treelist[max_fitness_tree_entry]._GetTree()
    mut_rate = inp_gen_pop_treelist[max_fitness_tree_entry]._GetMutationRate()
    cros_rate = inp_gen_pop_treelist[max_fitness_tree_entry]._GetCrossOverRate()
    # now append the tree in the next generation population
    AddPopulationEntry(next_gen_pop_treelist, inp_tree, mut_rate, cros_rate)
        
    # increment the output tree production counter for loop termination condition check
    count = count + 1
    
  return next_gen_pop_treelist
  
#-----------------------------------------
""" 
this function implements the ranking selection procedure
individual candidates are sorted based on fitness and assigned corresponding no of shares
based on a random integer value, one particular individual is selected 

parameter: 1) elitism_enabled
it is a boolean flag which makes sure that the best candidate solution of the last generation is always used in the next generation
2) fraction_prev_generation_retain: fraction of population that will be propagated to the next generation
remaining elements will be obtained by mutation and recombination of those samples
"""
def Ranking_Select(inp_gen_pop_treelist, next_gen_pop_treelist, orig_inp_dist_mat, no_of_taxa, LS_score_list, \
		  inp_pop_size, next_gen_pop_size_to_be_used, elitism_enabled, elitism_count):
        
  # total no of shares (required for ranking based selection) from the input population size
  total_share = (inp_pop_size * (inp_pop_size - 1)) / 2  
      
  if (DEBUG_LEVEL > 2):
    print 'constructed list before sorting: ', LS_score_list
    
  """ now sort the list according to the increasing value of LS 
  so elements in the list is sorted by decreasing order of priority
  i.e. 1st element of the list is the best candidate, 
  2nd element is the 2nd best candidate 
  for the elitism scheme, we have to select the first elements from this list """
  LS_score_list.sort(key=lambda x: x[1])
  #sorted(LS_score_list, key=operator.itemgetter(1))
  
  if (DEBUG_LEVEL > 2):
    print 'constructed list after sorting: ', LS_score_list
    
  # this variable checks the number of elements inserted in the next generation population
  count = 0
    
  """ now we check if elitism is enabled
  if so then we first insert the best candidates in the next generation population
  total number of such candidates is given by the parameter elitism_count """
  if (elitism_enabled == True):
    for i in range(elitism_count):
      """ index of the best candidate for elitism :
      LS_score_list[len(LS_score_list) - (i + 1)][0] 
      that element is inserted in the next_gen_pop_treelist """
      # index of the original population
      tree_idx_prev_gen_population = LS_score_list[i][0]
      if (DEBUG_LEVEL > 1):
	print 'elitism - previous generation propagation - tree index: ', tree_idx_prev_gen_population, ' added in the position: ', count
      # append corresponding tree in the next generation population
      # first derive the arguments
      inp_tree = inp_gen_pop_treelist[tree_idx_prev_gen_population]._GetTree()
      mut_rate = inp_gen_pop_treelist[tree_idx_prev_gen_population]._GetMutationRate()
      cros_rate = inp_gen_pop_treelist[tree_idx_prev_gen_population]._GetCrossOverRate()
      # now append the tree in the next generation population
      AddPopulationEntry(next_gen_pop_treelist, inp_tree, mut_rate, cros_rate)
      # increment the element counter
      count = count + 1
    
  """ now we construct the selected list of candidate solutions
  here we pick one random share and select corresponding solution assigned that particular share
  by this process we fill the candidate solutions for next generation """  
  N = len(LS_score_list)  
  while (count < next_gen_pop_size_to_be_used):
    # select one random share number
    # find that share belonging to one list element
    random_share_val = random.randint(1, total_share)
    # this variable signifies accumulated share which needs to be computed to find the location of current share value
    acc_share = 0
    """ list 0'th index contains N shares, where N = len(LS_score_list)
    1st index contains (N-1) shares
    in general, j'th index contains (N-j) shares """
    for j in range(N):
      if (acc_share <= random_share_val) and ((acc_share + N - j) >= random_share_val):
	# LS_score_list[j][0] contains the index of the target tree string (with respect to inp_gen_pop_treelist)
	# this tree will be included in the population
	# index of the original population
	tree_idx_prev_gen_population = LS_score_list[j][0]
	
	if (DEBUG_LEVEL > 1):
	  print 'share : ', random_share_val, 'acc share: ', acc_share, 'within sorted idx: ', j, \
		'previous population idx: ', tree_idx_prev_gen_population, ' added in the position: ', count
	
	# append corresponding tree in the next generation population
	# first derive the arguments
	inp_tree = inp_gen_pop_treelist[tree_idx_prev_gen_population]._GetTree()
	mut_rate = inp_gen_pop_treelist[tree_idx_prev_gen_population]._GetMutationRate()
	cros_rate = inp_gen_pop_treelist[tree_idx_prev_gen_population]._GetCrossOverRate()
	# now append the tree in the next generation population
	AddPopulationEntry(next_gen_pop_treelist, inp_tree, mut_rate, cros_rate)
	# increment the element counter
	count = count + 1	
	break
      # otherwise update the accumulated share
      acc_share = acc_share + (N - j)
      
  """ now return the next generation population
  it just contains good solutions from the last generation """
  return next_gen_pop_treelist
  
  
  