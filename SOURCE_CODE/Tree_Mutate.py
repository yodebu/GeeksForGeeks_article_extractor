#!/usr/bin/env python

""" 
this is the file containing functions for mutation of the input tree

Author: Sourya Bhattacharyya
Dept of CSE, IIT Kharagpur
V1.0 - 06.02.2014 - basic implementation
"""


import Header
from Header import *

import TreeUtilFunc
from TreeUtilFunc import *

#-----------------------------------------
""" this function selects among different mutation operators
and finally applies the selected mutation operation on the input tree """
def SelectAmongDiffMutation(inp_tree):
  
  if (DEBUG_LEVEL > 1):
    print 'Mutation --- length inp_tree_taxa_set: ', len(inp_tree.infer_taxa())
  
  # copy the inp_tree first
  mutated_tree = Tree(inp_tree)
  num = random.randint(1, num_diff_mutation_operators)	# number of mutation operation currently defined
  if (DEBUG_LEVEL > 2):
    print 'selected num: ', num
  if (num == 1):
    if (DEBUG_LEVEL > 1):
      print 'swapping taxa is selected'
    # mutation 1 - swapping the leaves
    SwapTaxa(mutated_tree)
  elif (num == 2):
    if (DEBUG_LEVEL > 1):
      print 'NNI is selected'
    # mutation 2 - NNI
    NNI(mutated_tree)
  else:
    if (DEBUG_LEVEL > 1):
      print 'SPR is selected'
    # mutation 3 - SPR
    SPR(mutated_tree)
  
  return mutated_tree

#-------------------------------------------------
""" this is a function to mutate the input tree using the swap operation
a pair of leaf nodes are interchanged """
def SwapTaxa(inp_tree):
  
  if (DEBUG_LEVEL > 2):
    print 'inp tree before SWAP : '
    TreePrint(inp_tree)
      
  # infer the taxa set of input tree
  inp_tree_taxa_set = inp_tree.infer_taxa()
  
  if (DEBUG_LEVEL > 2):
    print 'inp_tree_taxa_set: ', inp_tree_taxa_set
      
  # pick 2 distinct random indices from the set of indices of inp_tree_taxa_set
  rand_index_list = random.sample(xrange(len(inp_tree_taxa_set)), 2)
  
  # find the nodes in the tree corresponding to the pair of taxa pointed by these indices
  node1 = inp_tree.find_node_with_taxon_label(inp_tree_taxa_set[rand_index_list[0]].label)
  node2 = inp_tree.find_node_with_taxon_label(inp_tree_taxa_set[rand_index_list[1]].label)
  
  if (DEBUG_LEVEL > 1):
    print 'random selected indices: ', rand_index_list[0], rand_index_list[1]
    print 'nodes selected for swapping: ', node1.taxon.label, node2.taxon.label
  
  # now interchange the node labels
  temp_label = node1.taxon.label
  node1.taxon.label = node2.taxon.label
  node2.taxon.label = temp_label
  
  # update split hashes of the input tree, after this parent change operation
  #inp_tree.update_splits() 	# add - sourya
  
  if (DEBUG_LEVEL > 2):
    print 'inp tree after SWAP : '
    TreePrint(inp_tree)
    
#-------------------------------------------------
""" this is a function to mutate the input tree using the NNI operation
at first we search for an internal edge
then out of its 4 subtrees, two non sibling subtrees are swapped """
def NNI(inp_tree):
  
  if (DEBUG_LEVEL > 2):
    print 'inp tree before NNI : '
    TreePrint(inp_tree)

  # infer the internal edge set of input tree
  # obtain the internal edges with valid tail and head nodes as well
  # comment - sourya
  #inp_tree_internal_edge_set = GetValidInternalEdgeSet(inp_tree)
  # add - sourya
  filter_fn = lambda n: ((n.is_internal() == True) and (n.tail_node is not None))  
  inp_tree_internal_edge_set = inp_tree.get_edge_set(filter_fn=filter_fn)
  # end add - sourya
  
  if (DEBUG_LEVEL > 2):
    print 'selection of target edge from the internal edge set'
  
  # derive the target edge of the current tree which will be selected as random for NNI operation
  target_edge = DeriveTargetEdge(inp_tree_internal_edge_set)
    
  # now swap two non-sibling subtrees of this internal edge
  # at first find the head and tail nodes of the current edge
  # both the nodes will be internal nodes
  node_list = FindNodesOfTargetEdge(inp_tree, target_edge)
    
  # node_list contains the head and tail nodes of the current edge
  if (len(node_list) != 2):
    if (DEBUG_LEVEL > 1):
      print 'edge description: ', target_edge.description()
      print 'internal edge: ', target_edge.is_internal()
      print 'terminal edge: ', target_edge.is_terminal()
      print 'len(node_list): ', len(node_list)
      if (len(node_list) > 0):
	for temp_node in node_list:
	  print 'nodes --- ', temp_node
    print 'determination of parent and child node of the current edge has errors --- returning'
    return
    
  # two nodes (parent) 
  node1 = node_list[0]
  node2 = node_list[1]
  
  if (node1 is None) or (node2 is None):
    if (DEBUG_LEVEL > 1):
      print 'NNI - two internal root nodes (of target subtrees) are not present - at least one of them is None - return'
    return
  
  # obtain their children
  node1_child_nodes = node1.child_nodes()
  node2_child_nodes = node2.child_nodes()
  
  # comment - sourya
  """
  if node2 in node1_child_nodes:
    node1_child_nodes.remove(node2)
  if node1 in node2_child_nodes:
    node2_child_nodes.remove(node1)
  """
  # add - sourya
  node1_child_nodes_idx_list = []
  for i in range(len(node1_child_nodes)):
    node1_child_nodes_idx_list.append(i)
  node2_child_nodes_idx_list = []
  for i in range(len(node2_child_nodes)):
    node2_child_nodes_idx_list.append(i)
  if node2 in node1_child_nodes:
    node1_child_nodes_idx_list.remove(node1_child_nodes.index(node2))
  if node1 in node2_child_nodes:
    node2_child_nodes_idx_list.remove(node2_child_nodes.index(node1))    
  # end add - sourya
  
  if (DEBUG_LEVEL > 2):
    # comment - sourya
    """
    print 'node 1 no of children: ', len(node1_child_nodes)
    print 'node 2 no of children: ', len(node2_child_nodes)
    """
    # add - sourya
    print 'node 1 no of children: ', len(node1_child_nodes_idx_list)
    print 'node 2 no of children: ', len(node2_child_nodes_idx_list)
    # end add - sourya
    
  # select randomly one child from each node
  # comment - sourya
  """
  rand_index_node1_child_nodes = random.randint(0, (len(node1_child_nodes) - 1))
  rand_index_node2_child_nodes = random.randint(0, (len(node2_child_nodes) - 1))
  """
  # add - sourya
  # last [0] is used since the random.sample function returns a 1 element list
  rand_index_node1_child_nodes = random.sample(node1_child_nodes_idx_list, 1)[0]
  rand_index_node2_child_nodes = random.sample(node2_child_nodes_idx_list, 1)[0]  
  # end add - sourya
  
  if (DEBUG_LEVEL > 1):
    print 'random index of node1 child list: ', rand_index_node1_child_nodes
    if (node1_child_nodes[rand_index_node1_child_nodes].is_leaf() == True):
      print 'node1 child -- leaf -- label: ', node1_child_nodes[rand_index_node1_child_nodes].taxon.label
    print 'random index of node2 child list: ', rand_index_node2_child_nodes
    if (node2_child_nodes[rand_index_node2_child_nodes].is_leaf() == True):
      print 'node2 child -- leaf -- label: ', node2_child_nodes[rand_index_node2_child_nodes].taxon.label
  
  # perform the swapping
  node1_child_to_be_swapped = Search_Tree_Node(inp_tree, node1_child_nodes[rand_index_node1_child_nodes])
  node2_child_to_be_swapped = Search_Tree_Node(inp_tree, node2_child_nodes[rand_index_node2_child_nodes])
  
  if (DEBUG_LEVEL > 1):
    if (node1_child_to_be_swapped is None) or (node2_child_to_be_swapped is None):
      print 'during NNI - subtrees for swapping are None - exit'
      return
    else:
      print 'node1_child_to_be_swapped: ', node1_child_to_be_swapped
      print 'node2_child_to_be_swapped; ', node2_child_to_be_swapped

  #node1.remove_child(node1_child_to_be_swapped)
  #node2.remove_child(node2_child_to_be_swapped)
  #node1_child_to_be_swapped.parent_node = None
  #node2_child_to_be_swapped.parent_node = None
  #node1.add_child(node2_child_to_be_swapped)
  #node2.add_child(node1_child_to_be_swapped)
  node2_child_to_be_swapped.parent_node = node1	# add - sourya
  node1_child_to_be_swapped.parent_node = node2	# add - sourya
          
  # update split hashes of the input tree, after this parent change operation
  #inp_tree.update_splits() 	# add - sourya
  
  if (DEBUG_LEVEL > 2):
    print 'inp tree after NNI: '
    TreePrint(inp_tree)
    
#-------------------------------------------------
""" this is a function to mutate the input tree using the SPR operation
at first we delete one subtree from the tree
then we insert that subtree onto one random edge of the remaining tree """
def SPR(inp_tree):
  if (DEBUG_LEVEL > 2):
    print 'inp tree before SPR : '
    TreePrint(inp_tree)
    
  if (DEBUG_LEVEL > 1):
    print 'before SPR: length of input tree edge set: ', len(inp_tree.get_edge_set())
    
  # pick one node (leaf / taxa or an internal node) which will be the root of subtree to be deleted
  # one condition is that the root of the subtree cannot be the root of the original tree
  # so we have to check for only those nodes (internal or leaf) which have a valid parent node
  filter_fn = lambda n: (n.parent_node is not None)  
  inp_tree_all_node_set = inp_tree.get_node_set(filter_fn=filter_fn)
  
  # now select one random node from the given node set
  target_node = DeriveTargetNode(inp_tree_all_node_set)
  target_node_branch_len = target_node.edge_length  
  if (DEBUG_LEVEL > 1):
    print 'target node: ', target_node
    print 'description; ', target_node.description()
    print 'its branch length: ', target_node_branch_len
  
  # now create one new tree which will contain the desired subtree
  new_subtree = Tree(inp_tree) 
  # set root ("seed_node") to above node
  new_subtree.seed_node = target_node
  # now prune the subtree from the input tree
  inp_tree.prune_subtree(target_node)
  #inp_tree.update_splits()  
  # set parent of root node to None
  new_subtree.seed_node.parent_node = None
  
  if (DEBUG_LEVEL > 2):
    print 'inp tree (after pruning the subtree) : '
    TreePrint(inp_tree)        
    print 'new subtree generated : '
    TreePrint(new_subtree)
    
  if (DEBUG_LEVEL > 1):
    print 'after pruning: len of inp tree taxa set: ', len(inp_tree.infer_taxa())
    print 'len of new subtree taxa set: ', len(new_subtree.infer_taxa())

  # comment - sourya
  #inp_tree_edge_set = inp_tree.get_edge_set()

  # add - sourya
  # after pruning the subtree from the input tree, now we have to select one random edge from the remaining input tree
  filter_fn = lambda n: (n.tail_node is not None)
  inp_tree_edge_set = inp_tree.get_edge_set(filter_fn=filter_fn)
  # end add - sourya
  
  if (DEBUG_LEVEL > 1):
    print 'within SPR: after pruning --- length of input tree edge set: ', len(inp_tree_edge_set)  
  
  if (DEBUG_LEVEL > 2):
    print 'selection of target edge from the input tree edge set'
  
  # after pruning the subtree from the input tree, now we have to select one random edge from the remaining input tree
  target_edge = DeriveTargetEdge(inp_tree_edge_set)
  
  if (DEBUG_LEVEL > 1):
    print 'target edge: ', target_edge.description()
  
  # find the head and tail nodes of the current edge  
  node_list = FindNodesOfTargetEdge(inp_tree, target_edge)
  
  """ check the head and tail nodes of the current edge
  if the tail node is None then it is the root edge
  insert accordingly """
  curr_edge_parent_node, curr_edge_child_node = FindParentChildNodeReln(node_list)

  if (curr_edge_parent_node is None) and (curr_edge_child_node is None):
    return
    
  if (DEBUG_LEVEL > 1):
    print 'parent node of the edge (where the subtree will be inserted) : ', curr_edge_parent_node
    print 'child node of the edge (where the subtree will be inserted) : ', curr_edge_child_node
    #print 'target edge length: ', target_edge.length
    
  # now insert the subtree on to the input tree
  InsertSubtreeOnTree(curr_edge_parent_node, curr_edge_child_node, new_subtree, target_node_branch_len, target_edge.length)
        
  # update split hashes of the input tree, after this parent change operation
  #inp_tree.update_splits() 	# add - sourya
        
  if (DEBUG_LEVEL > 2):
    print 'inp tree (after SPR operation) : '
    TreePrint(inp_tree)
    
  