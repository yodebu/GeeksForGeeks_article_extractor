#!/usr/bin/env python

import Header
from Header import *

import Tree_Generate
from Tree_Generate import *

import Tree_Recombination
from Tree_Recombination import *

import Tree_Mutate
from Tree_Mutate import *

import Selection
from Selection import *

##-----------------------------------------------------
""" this function first constructs the initial population
it will have the NJ tree
mutation of NJ tree for every 10th population
or a random tree """
def Create_Initial_Population(Population_Treelist, NJ_tree, Orig_Dist_Mat, total_population_size):
  # taxa set of the NJ tree
  nj_tree_taxa_set = NJ_tree.infer_taxa()
  # now generate the population
  for pop_idx in range(total_population_size):
    if (DEBUG_LEVEL > 2):
      print 'generating population index: ', pop_idx
    mut_rate = 0.1 * ((pop_idx % 10) + 1)
    cros_rate = 0.1 * ((pop_idx % 10) + 1)
    if (pop_idx == 0):
      if (DEBUG_LEVEL > 1):
	print 'NJ tree in pop idx: ', pop_idx
      AddPopulationEntry(Population_Treelist, NJ_tree, mut_rate, cros_rate)
    elif (((pop_idx + 1) % 10) == 0):	# every 10th population
      if (DEBUG_LEVEL > 1):
	print 'Mutation of NJ tree in pop idx: ', pop_idx    
      # apply mutation of the NJ tree to generate candidates for genetic population
      mutated_tree = SelectAmongDiffMutation(NJ_tree)
      # now add this mutated tree
      AddPopulationEntry(Population_Treelist, mutated_tree, mut_rate, cros_rate)
    else:  
      # obtain a random tree which will have same taxa set as the NJ_tree 
      # and its average branch length will correspond to the average of input distance matrix
      random_tree = Generate_Random_Tree(nj_tree_taxa_set, Orig_Dist_Mat)
      # now add this random tree
      AddPopulationEntry(Population_Treelist, random_tree, mut_rate, cros_rate)
      
##-----------------------------------------------------
""" this function adds one element to the next generation population
by recombination of two parent elements """
def AddElem_Recombination(NextGenPop, propagate_pop_size, pop_idx):
  # this loop selects two indices from the already propagated enxt generation elements, for recombination
  while(1):
    recomb_parent_idx_list = random.sample(xrange(propagate_pop_size), 2)  
    parent1_prob_rand = random.random()
    parent2_prob_rand = random.random()
    if (parent1_prob_rand <= NextGenPop[recomb_parent_idx_list[0]]._GetCrossOverRate()) and \
	(parent2_prob_rand <= NextGenPop[recomb_parent_idx_list[1]]._GetCrossOverRate()):
      break
  
  if (DEBUG_LEVEL > 1):
    print '===>> recombination using trees (of previous population) indices: ', recomb_parent_idx_list[0], recomb_parent_idx_list[1], ' placed at idx: ', pop_idx
  
  # now form the recombined tree
  parent_tree1 = NextGenPop[recomb_parent_idx_list[0]]._GetTree()
  parent_tree2 = NextGenPop[recomb_parent_idx_list[1]]._GetTree()
  offspring_tree = Prune_Del_Graph_Recomb(parent_tree1, parent_tree2)
    
  # change the mutation and recombination probabilities of this new offspring_tree
  val = random.random()	# generate a number between 0 and 1
  mut_rate = val * NextGenPop[recomb_parent_idx_list[0]]._GetMutationRate() \
	      + (1 - val) * NextGenPop[recomb_parent_idx_list[1]]._GetMutationRate()
  mut_rate = ValidateRate(mut_rate)
  cros_rate = val * NextGenPop[recomb_parent_idx_list[0]]._GetCrossOverRate() \
	      + (1 - val) * NextGenPop[recomb_parent_idx_list[1]]._GetCrossOverRate()
  cros_rate = ValidateRate(cros_rate)
  
  if (DEBUG_LEVEL > 1):
    print 'offspring: mutation rate: ', mut_rate, ' crossover rate: ', cros_rate
  
  AddPopulationEntry(NextGenPop, offspring_tree, mut_rate, cros_rate)
  
  
##-----------------------------------------------------
""" this function adds one element to the next generation population
by mutation of one parent element """
def AddElem_Mutation(NextGenPop, propagate_pop_size, pop_idx):
  # this loop selects one element from the already propagated enxt generation elements, for mutation
  while(1):
    mut_idx = random.randint(0, (propagate_pop_size - 1))
    mut_prob = random.random()
    if (mut_prob <= NextGenPop[mut_idx]._GetMutationRate()):
      break

  if (DEBUG_LEVEL > 1):
    print '==>>> mutation of tree (of previous population) index: ', mut_idx, ' placed at idx: ', pop_idx
  
  # now form the mutated tree
  parent_tree = NextGenPop[mut_idx]._GetTree()
  offspring_tree = SelectAmongDiffMutation(parent_tree)
  
  # change the mutation and recombination probabilities of this new offspring_tree
  mut_rate = gauss(0, 1) * 0.05 * NextGenPop[mut_idx]._GetMutationRate()
  mut_rate = ValidateRate(mut_rate)
  cros_rate = gauss(0, 1) * 0.05 * NextGenPop[mut_idx]._GetCrossOverRate()
  cros_rate = ValidateRate(cros_rate)
  
  if (DEBUG_LEVEL > 1):
    print 'offspring: mutation rate: ', mut_rate, ' crossover rate: ', cros_rate
  
  AddPopulationEntry(NextGenPop, offspring_tree, mut_rate, cros_rate)
  
##-----------------------------------------------------
""" this function constructs the remaining part of next generation population
by mutation and recombination operations of the elements (of previous generation) 
which are already placed in this generation (by selection operation)
parameters: NextGenPop: total next generation population
propagate_pop_size: no of elements that have been propagated from the previous generation 
pop_idx: the position where this new element is inserted """
def NextGenEvolve(NextGenPop, propagate_pop_size, pop_idx):
  # select operator of either recombination or mutation
  GA_operator_type = random.randint(1, 2)
  if (GA_operator_type == 1):
    if (DEBUG_LEVEL > 1):
      print 'selection of candidate for idx: ', pop_idx, 'via recombination ---'
    # perform recombination
    AddElem_Recombination(NextGenPop, propagate_pop_size, pop_idx)
  else:
    if (DEBUG_LEVEL > 1):
      print 'selection of candidate for idx: ', pop_idx, 'via mutation ---'
    # perform mutation
    AddElem_Mutation(NextGenPop, propagate_pop_size, pop_idx)
  
##-----------------------------------------------------
""" this function has input of current population
it forms the next generation population """
def FormNextGenPopulation(Population_Treelist, Next_Gen_Pop_Treelist, inp_dist_mat, Number_of_taxa, LS_score_list, \
			  population_size,  selection_scheme, fraction_prev_generation_retain, elitism_count):
    
  """ this is the population size that will be filled by elements of previous generation
  basically, all the best candidates upto this number will be propagated
  requires some rounding operator as the target value is an integer """ 
  Next_Gen_Popsize_from_Prev_Gen = math.trunc(population_size * fraction_prev_generation_retain)
  
  if (DEBUG_LEVEL > 2):
    print 'Next_Gen_Popsize_from_Prev_Gen: ', Next_Gen_Popsize_from_Prev_Gen
  
  # at first form the next generation population containing the best candidates of previous generation 
  if (selection_scheme == 2):
    Ranking_Select(Population_Treelist, Next_Gen_Pop_Treelist, inp_dist_mat, Number_of_taxa, LS_score_list, \
		  population_size, Next_Gen_Popsize_from_Prev_Gen, True, elitism_count)
  elif (selection_scheme == 1):
    Ranking_Select(Population_Treelist, Next_Gen_Pop_Treelist, inp_dist_mat, Number_of_taxa, LS_score_list, \
		  population_size, Next_Gen_Popsize_from_Prev_Gen, False, 0)
  else:
    Tournament_Select(Population_Treelist, Next_Gen_Pop_Treelist, inp_dist_mat, Number_of_taxa, LS_score_list, \
		      population_size, Next_Gen_Popsize_from_Prev_Gen)    
    
  
  """ now fill the remaining elements with the mutation and crossover scheme
  number of such remaining elements: (population_size - Next_Gen_Popsize_from_Prev_Gen) """
  for pop_idx in range(Next_Gen_Popsize_from_Prev_Gen, population_size):
    # append individual element to the next generation population
    NextGenEvolve(Next_Gen_Pop_Treelist, Next_Gen_Popsize_from_Prev_Gen, pop_idx)
    
##-----------------------------------------------------
""" this function generates the LS scores for all the trees in the input tree list """
def Generate_LS_scores_Treelist(inp_gen_pop_treelist, orig_inp_dist_mat, no_of_taxa, inp_pop_size):
  # at first compute the fitness of individual solutions and store them in a list
  LS_score_list = []
  for i in range(inp_pop_size):
    curr_tree = inp_gen_pop_treelist[i]._GetTree()
    if (DEBUG_LEVEL > 1):
      print 'LS score check -- curr tree idx: ', i, 'len taxa set: ', len(curr_tree.infer_taxa())
      #print 'taxa set: ', curr_tree.infer_taxa().labels()
    if (DEBUG_LEVEL > 2):
      TreePrint(curr_tree)
    curr_tree_LS_score = EvaluateLS(orig_inp_dist_mat, no_of_taxa, curr_tree)
    sublist = [i, curr_tree_LS_score]
    LS_score_list.append(sublist)
  
  return LS_score_list
  
  
  
  
  
  
  
  