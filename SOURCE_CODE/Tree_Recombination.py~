#!/usr/bin/env python

""" 
this is the file containing functions for recombination of the input tree
that is, the crossover operation between 2 parents are performed

Author: Sourya Bhattacharyya
Dept of CSE, IIT Kharagpur
V1.0 - 06.02.2014 - basic implementation
"""


import Header
from Header import *

import TreeUtilFunc
from TreeUtilFunc import *

#-------------------------------------------------
""" this is a function to recombine two parent trees
this operation is termed as prune delete graph recombination """
def Prune_Del_Graph_Recomb(parent_tree1, parent_tree2):
  if (DEBUG_LEVEL > 2):
    print 'PDG operation - input parent tree 1 : '
    TreePrint(parent_tree1)
    print 'PDG operation - input parent tree 2 : '
    TreePrint(parent_tree2)
  
  # at first create one copy of the parent_tree1
  offspring_tree = Tree(parent_tree1)
  
  if (DEBUG_LEVEL > 1):
    print 'recombination: length of offspring tree edge set: ', len(offspring_tree.get_edge_set())  
  
  # form the subtree consisting of taxa set of the second parent tree, starting from the target_node_parent_tree2 as its root
  new_subtree_parent_tree2 = Tree(parent_tree2)   
  
  if (DEBUG_LEVEL > 1):
    print 'recombination - length of taxa set of parent tree1: ', len(parent_tree1.infer_taxa())
    print 'recombination - length of taxa set of parent tree2: ', len(parent_tree2.infer_taxa())
  
  # pick one node (leaf / taxa or an internal node) from the second parent tree
  # which will be the root of subtree of the second parent tree (to be used in the offspring)
  # one condition is that the root of the subtree cannot be the root of the second parent tree
  # so we have to check for only those nodes (internal or leaf) which have a valid parent node
  filter_fn = lambda n: (n.parent_node is not None)  
  new_subtree_parent_tree2_all_node_set = new_subtree_parent_tree2.get_node_set(filter_fn=filter_fn)
  
  # now select one random node from the given node set of the second parent tree
  target_node_new_subtree_parent_tree2 = DeriveTargetNode(new_subtree_parent_tree2_all_node_set)
  target_node_new_subtree_parent_tree2_branch_len = target_node_new_subtree_parent_tree2.edge_length  
  if (DEBUG_LEVEL > 1):
    print 'target node: ', target_node_new_subtree_parent_tree2
    print 'description; ', target_node_new_subtree_parent_tree2.description()
    #print 'its branch length: ', target_node_new_subtree_parent_tree2_branch_len
    
  # set root ("seed_node") to above node
  new_subtree_parent_tree2.seed_node = target_node_new_subtree_parent_tree2
  # set parent of root node to None
  new_subtree_parent_tree2.seed_node.parent_node = None
  if (DEBUG_LEVEL > 2):
    print 'new subtree from the second parent tree: '
    TreePrint(new_subtree_parent_tree2)
    
  # infer the taxa set of this subtree (labels)
  new_subtree_parent_tree2_taxa_set_labels = new_subtree_parent_tree2.infer_taxa().labels()
  
  if (DEBUG_LEVEL > 1):
    print 'length of subtree (for pruning): ', len(new_subtree_parent_tree2_taxa_set_labels)
    print 'corresponding labels: ', new_subtree_parent_tree2_taxa_set_labels
  
  # all the taxa of the subtree of the second parent tree should be removed from the offspring tree first  
  # comment - sourya
  # offspring_tree.prune_taxa_with_labels(new_subtree_parent_tree2_taxa_set_labels)
  # add - sourya
  offspring_tree_taxa_labels = offspring_tree.infer_taxa().labels()
  for label in new_subtree_parent_tree2_taxa_set_labels:
    if label in offspring_tree_taxa_labels:
      offspring_tree.prune_taxa_with_labels(label)  
  # end add - sourya
  
  if (DEBUG_LEVEL > 2):
    print 'offspring tree (copy of parent tree 1) after pruning tha taxa set of the derived subtree (of parent tree 2): '
    TreePrint(offspring_tree)
    
  if (DEBUG_LEVEL > 1):
    print 'after pruning: len of offspring tree taxa set: ', len(offspring_tree.infer_taxa())
  
  # now we have to select one random edge from the remaining offspring tree
  # comment - sourya
  # offspring_tree_edge_set = offspring_tree.get_edge_set()  

  # add - sourya
  filter_fn = lambda n: (n.tail_node is not None)
  offspring_tree_edge_set = offspring_tree.get_edge_set(filter_fn=filter_fn)
  # end add - sourya
  
  if (DEBUG_LEVEL > 1):
    print 'within recombination: after pruning --- length of offspring tree edge set: ', len(offspring_tree_edge_set)  
  
  if (DEBUG_LEVEL > 2):
    print 'selection of target edge from the edge set of the offspring tree'
  
  # after pruning the subtree from the input tree, now we have to select one random edge from the remaining input tree
  target_edge = DeriveTargetEdge(offspring_tree_edge_set)
  
  if (DEBUG_LEVEL > 1):
    print 'target edge: ', target_edge.description()  
  
  # find the head and tail nodes of the current edge  
  node_list = FindNodesOfTargetEdge(offspring_tree, target_edge)
  
  """ check the head and tail nodes of the current edge
  if the tail node is None then it is the root edge
  insert accordingly """
  curr_edge_parent_node, curr_edge_child_node = FindParentChildNodeReln(node_list)

  if (curr_edge_parent_node is None) and (curr_edge_child_node is None):
    return
    
  if (DEBUG_LEVEL > 2):
    print 'parent node of the edge (where the subtree will be inserted) : ', curr_edge_parent_node
    print 'child node of the edge (where the subtree will be inserted) : ', curr_edge_child_node
    
  # now insert the subtree on to the input tree
  InsertSubtreeOnTree(curr_edge_parent_node, curr_edge_child_node, new_subtree_parent_tree2, target_node_new_subtree_parent_tree2_branch_len, target_edge.length)
  
  # update split hashes of the input tree, after this parent change operation
  #offspring_tree.update_splits() 	# add - sourya
  
  if (DEBUG_LEVEL > 2):
    print 'offspring tree (after PDG operation) : '
    TreePrint(offspring_tree)
  
  return offspring_tree
  
