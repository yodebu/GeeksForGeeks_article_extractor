#!/usr/bin/env python

''' 
this is the file containing function to implement the various Trees
from an input of distance matrix

Author: Sourya Bhattacharyya
Dept of CSE, IIT Kharagpur
V1.0 - 06.02.2014 - basic implementation
''' 


import Header
from Header import *

import UtilFunc
from UtilFunc import *

#------------------------------------------
# this function generates the neighbor joining tree from a given distance matrix 
def NJ_Tree_Gen(neighbor_batch_filename, out_NJ_exec_file, out_NJ_exec_tree):
          
  ''' now there is a phylip file generated
  use the NEIGHBOR executable to process this file and generate the distance matrix 
  the distance matrix is provided as input
  the tree files are produed as output
  the file named screenout1 contains the detail output description 
  input: out_dnadist_filename_distmat_simul_tree_orig
  imp ------ make sure the process runs on foreground so that the system waits until completion of execution '''      
  phylip_neighbor_exec_command = location_neighbor_exec + ' < ' + neighbor_batch_filename + ' > screenout'
  os.system(phylip_neighbor_exec_command)
  
  # now copy the generated files in a separate name for future use and comparison
  # out_NJ_exec_file contains output results and descriptions of the NJ method
  # out_NJ_exec_tree contains output tree generated from NJ 
  file_rename_command = 'mv -f outfile ' + str(out_NJ_exec_file)
  os.system(file_rename_command)
  file_rename_command = 'mv -f outtree ' + str(out_NJ_exec_tree)
  os.system(file_rename_command)
  
  # delete the instance of screenout
  Prev_File_Instance_Del()
  
  # now read the tree generated from NJ execution, from the file out_NJ_exec_tree 
  out_tree_NJ_algo = dendropy.Tree.get_from_path(out_NJ_exec_tree, "newick")
  
  return out_tree_NJ_algo
  
##-----------------------------------------------------
''' this function generates a random tree with the same taxa set as the input tree '''
def Generate_Random_Tree(inp_taxa_set, input_dist_mat):
  # generate the random tree using random birth death process
  #random_tree = treesim.birth_death(birth_rate=1.0, death_rate=0.9, taxon_set=inp_taxa_set, repeat_until_success=True)  
  
  random_tree = treesim.birth_death(birth_rate=1.0, death_rate=0, taxon_set=inp_taxa_set, repeat_until_success=True)  

  # now modify the random tree branch lengths so that the average branch length
  # of the random tree equals of the NJ tree
  if 0:
    ModifyBranch(random_tree, input_dist_mat, inp_taxa_set)
  
  return random_tree
  
##-----------------------------------------------------
''' this function modifies the tree branch length
basically weighted adjustment '''
def ModifyBranch(random_tree, input_dist_mat, inp_taxa_set):
  # compute the average value of the original distance matrix
  avg_inp_dist_mat_val = Compute_Avg_Dist_Mat(input_dist_mat)
  ntaxa = (numpy.shape(input_dist_mat))[0]
  if (DEBUG_LEVEL > 1):
    print 'average input distance matrix value: ', avg_inp_dist_mat_val
  # generate distance matrix of the random tree
  pdm_randtree = treecalc.PatristicDistanceMatrix(random_tree)
  # compute the average entry of the distance matrix of the random tree
  avg_rand_tree_dist_mat_val = 0
  for i in range(ntaxa - 1):
    t1 = inp_taxa_set[i]
    for j in range(i+1, ntaxa):
      t2 = inp_taxa_set[j]
      avg_rand_tree_dist_mat_val = avg_rand_tree_dist_mat_val + pdm_randtree(t1, t2)
  # compute the average value
  avg_rand_tree_dist_mat_val = (avg_rand_tree_dist_mat_val * 1.0) / ((ntaxa * (ntaxa - 1)) / 2)  
  if (DEBUG_LEVEL > 1):
    print 'average random tree distance matrix value: ', avg_rand_tree_dist_mat_val
  # now scale each edge of the random tree to the ratio of the average values
  ratio_avg_values = (avg_inp_dist_mat_val / avg_rand_tree_dist_mat_val)
  random_tree.scale_edges(ratio_avg_values)  
  
##-----------------------------------------------------
""" this function enters individual entries for constructing the initial population """
def AddPopulationEntry(Population_Treelist, inp_tree, mut_rate, cros_rate):
  # append new instance of Entity_Population class in the tree list
  Population_Treelist.append(Entity_Population(inp_tree, mut_rate, cros_rate))  
  ## input tree append
  #Population_Treelist[pop_idx]._SetTree(inp_tree)
  #""" mutation and crossover rates are varying from 0.1 to 1, with a step of 0.1
  #depending on the current index, rates are selected """
  #Population_Treelist[pop_idx]._SetMutationRate(mut_rate)
  #Population_Treelist[pop_idx]._SetCrossOverRate(cros_rate)
  