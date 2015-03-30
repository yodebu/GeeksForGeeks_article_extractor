#!/usr/bin/env python

''' 
this is the file containing basic class definitions and importing the libraries
required for the implementation of the source code 

Author: Sourya Bhattacharyya
Dept of CSE, IIT Kharagpur
V1.0 - 06.02.2014 - basic implementation
''' 

import dendropy
from dendropy import *
#from dendropy import treesim 
#from dendropy import Tree, Taxon, TaxonSet, TreeList, Node
#from dendropy import treecalc
import itertools
import numpy
from numpy import *
import os
import re
import math
from math import *
#import matplotlib.pyplot as plt
#from pylab import *
import operator
from operator import itemgetter
import time
from optparse import OptionParser
import random
from random import gauss
from cStringIO import StringIO

# variable for debugging option set
DEBUG_LEVEL = 2

# executable path of neighbor joining code
# integrated in the PHYLIP package
location_neighbor_exec = '/home/sourya/SOURYA_ALL/PhD_Codes/GSP/REFERENCE_CODES/PHYLIP/phylip-3.695/exe/neighbor'

neighbor_batch_filename = 'NJ_exec_command_seq.txt'
out_NJ_exec_filename = 'out_NJ_file.phy'
out_NJ_exec_treename = 'out_NJ_tree.phy'

""" this is the list of taxon names used for the current execution
it is filled by manual reading of the input distance matrix file
the list is useful to find out the index of individual taxa labels in the distance matrix
since the NJ tree and original distance matrix may use different taxa ordering during creation of respective distance matrices """
LIST_OF_TAXON_NAMES = []

#------------------------------------
# parameters used for genetic algorithm
#------------------------------------
# mutation rate is 0.5 for measure based parameter control
# we can also tune this rate between 0 and 1 with a step size of 0.1 
# for measure based parameter control, following adaptation is made -----
# 1) results are not so good for 10 generations then this rate is increased by 0.05
# 2) results are good for 2 generations then this rate is decreased by 0.05
# if the rate goes below 0.06 or above 0.95 then it is reset to 0.5
#mutation_rate = 0.5

# recombination rate is 0.5 for measure based parameter control
# we can also tune this rate between 0 and 1 with a step size of 0.1
# for measure based parameter control, following adaptation is made -----
# 1) results are not so good for 10 generations then this rate is increased by 0.05
# 2) results are good for 2 generations then this rate is decreased by 0.05
# if the rate goes below 0.06 or above 0.95 then it is reset to 0.5
#recombination_rate = 0.5 

no_of_repeated_experiments = 5

# this variable signifies the different mutation operators currently implemented
# so far SWAP TAXA, NNI, and SPR are implemented
num_diff_mutation_operators = 3

# this is the subset size employed for tournament selection
tournament_select_subset_size = 2

#-------------------------------------------------------
""" this class represents one entry of a population
it constitutes one tree (in string newick format), crossover rate, and a mutation rate """
class Entity_Population(object):
  def __init__(self, inp_tree=None, inp_mut_rate=0, inp_cros_rate=0):
    self._SetTree(inp_tree)
    self._SetMutationRate(inp_mut_rate)
    self._SetCrossOverRate(inp_cros_rate)
    
  def _GetMutationRate(self):
    return self.Mutation_Rate
  
  def _GetCrossOverRate(self):
    return self.CrossOver_Rate
    
  def _SetMutationRate(self, inp_val):
    self.Mutation_Rate = inp_val
  
  def _SetCrossOverRate(self, inp_val):
    self.CrossOver_Rate = inp_val
    
  def _GetTree(self):
    return self.Inp_Tree
    
  def _SetTree(self, inp_tree):
    if (inp_tree is None):
      self.Inp_Tree = Tree()
    else:
      self.Inp_Tree = Tree(inp_tree)
  
  
  
