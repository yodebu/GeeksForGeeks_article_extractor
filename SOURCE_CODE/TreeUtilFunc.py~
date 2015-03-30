#!/usr/bin/env python

import Header
from Header import *

#-----------------------------------------
# this function prints input tree
def TreePrint(inp_tree):  
  print 'inp tree : ', inp_tree.as_string("newick")
  # at least two taxa are reqd
  if (len(inp_tree.infer_taxa()) > 1):
    inp_tree.print_plot()
  
#-----------------------------------------
""" this custom function searches one node in a tree
the node can be internal or a leaf node """
def Search_Tree_Node(inp_tree, target_node):
  for temp_node in inp_tree.postorder_node_iter():
    if (DEBUG_LEVEL > 2):
      print 'postoder iteration - temp_node : ', temp_node
    if (target_node == temp_node):
      if (DEBUG_LEVEL > 2):
	print 'found the target node: ', temp_node
      return temp_node
  return None
    
#-----------------------------------------
#""" this function obtains one edge set which consists of the internal edges
#plus having valid tail and head nodes """
#def GetValidInternalEdgeSet(inp_tree):
  #inp_tree_internal_edge_set = set()	# empty set
  #for e in inp_tree.get_edge_set():
    #e1 = e	# store the copy
    #if (e1.is_internal() == True) and (e1.is_terminal() == False):
      #""" this function switches the tail and head node
      #if previously tail node pointer was None then now head node pointer will be None 
      #in such case, current edge will be both non terminal and non internal edge """      
      #if ((e1.invert()).is_terminal() == False):
	#inp_tree_internal_edge_set.add(e)
  #return inp_tree_internal_edge_set
  
#-----------------------------------------
# this function obtains one target edge (by random selection) from the input edge set (having certain property) 
def DeriveTargetEdge(inp_edge_set):
  """ the random index will be between 1 to n where n is the set cardinality
  set does not support indexing
  so we have to pop the edges one by one until we obtain the desired edge """
  # comment - sourya
  """
  rand_index = random.randint(1, len(inp_edge_set)) 
  if (DEBUG_LEVEL > 2):
    print 'length of edge set: ', len(inp_edge_set)
    print 'generated random index: ', rand_index
  no_of_pop = 0
  while (no_of_pop < rand_index):
    # this is the shallow copy of the target edge maintained in the set data type
    target_edge = inp_edge_set.pop()
    no_of_pop = no_of_pop + 1
  """
  # add - sourya
  # one random edge from the input set
  #target_edge = random.sample(inp_edge_set, 1)
  
  rand_index = random.randint(1, len(inp_edge_set)) 
  no_of_pop = 0
  for edge in inp_edge_set:
    no_of_pop = no_of_pop + 1
    if (no_of_pop == rand_index):
      target_edge = edge
      break
  # end add - sourya
  return target_edge
  
#-----------------------------------------
# this function finds two nodes on either side of an edge (in a tree)
def FindNodesOfTargetEdge(inp_tree, target_edge):
  node_list = []
  for temp_node in inp_tree.postorder_node_iter():
    if target_edge in temp_node.incident_edges():
      node_list.append(temp_node)
  return node_list
  
#-----------------------------------------
# this function obtains one target node (by random selection) from the input node set (having certain property) 
def DeriveTargetNode(inp_node_set):
  # comment - sourya
  """
  # now select the random node
  rand_index = random.randint(1, len(inp_node_set))
  if (DEBUG_LEVEL > 2):
    print 'length of node set: ', len(inp_node_set)
    print 'generated random index: ', rand_index
  no_of_pop = 0
  while (no_of_pop < rand_index):
    # this is the shallow copy of the target edge maintained in the set data type
    target_node = inp_node_set.pop()
    no_of_pop = no_of_pop + 1
  """
  # add - sourya
  # one random node from the input set
  #target_node = random.sample(inp_node_set, 1)
  
  rand_index = random.randint(1, len(inp_node_set))
  no_of_pop = 0
  for node in inp_node_set:
    no_of_pop = no_of_pop + 1
    if (no_of_pop == rand_index):
      target_node = node
      break
  # end add - sourya
  return target_node
  
#-----------------------------------------
# by inspecting the input node list, this function finds the parent and child nodes of a particular edge 
def FindParentChildNodeReln(node_list):
  """ depending on the selected random edge, find the head and tail nodes of the edge
  case 1 - if the node list has length 0 then the edge selected is surely a false one
  case 2 - if the node list has length 1 then it has no tail node 
  case 3 - one internal edge selected """
  if (len(node_list) == 0):
    if (DEBUG_LEVEL > 1):
      print 'there is no single node associated with this edge - this edge is not a valid edge - return'
    return None, None
  elif (len(node_list) == 1):
    curr_edge_parent_node = None
    curr_edge_child_node = node_list[0]
  else:      
    if (node_list[0].parent_node == node_list[1]):
      curr_edge_parent_node = node_list[1]
      curr_edge_child_node = node_list[0]
    elif (node_list[1].parent_node == node_list[0]):
      curr_edge_parent_node = node_list[0]
      curr_edge_child_node = node_list[1]
    else:
      if (DEBUG_LEVEL > 1):
	print 'there is no parent or child node of the edge where the subtree will be inserted -- return'
      return None, None
  
  return curr_edge_parent_node, curr_edge_child_node
  
#-----------------------------------------
""" this function places a new node between input parent and child nodes
and inserts the input subtree between them """ 
def InsertSubtreeOnTree(curr_edge_parent_node, curr_edge_child_node, new_subtree, target_node_branch_len, prev_edge_len):
  """ create a new internal node within its edge
  it will be placed at the middle of current parent and child nodes
  the length of edge will be half """
  #prev_edge_len = curr_edge_child_node.edge_length
  newnode = Node()	# create one node
  
  """ if there exists a parent node then it will have this new node as its child
  else this new node will act as the root of the tree 
  the previous child node will now be child of this new node
  along with the modified branch length information """
  if (curr_edge_parent_node is not None):
    #newnode.parent_node = curr_edge_parent_node
    #curr_edge_child_node.parent_node = newnode
    curr_edge_parent_node.add_child(newnode)
    newnode.add_child(curr_edge_child_node)
    curr_edge_parent_node.remove_child(curr_edge_child_node)
  else:
    newnode.parent_node = None
    curr_edge_child_node.parent_node = None
    newnode.add_child(curr_edge_child_node)
    #curr_edge_child_node.parent_node = newnode
  
  # comment - sourya
  """
  curr_edge_child_node.edge_length = (prev_edge_len / 2.0)
  newnode.edge_length = (prev_edge_len / 2.0)
  """
  
  # modified - sourya
  if (prev_edge_len is not None):
    curr_edge_child_node.edge_length = (prev_edge_len / 2.0)
    newnode.edge_length = (prev_edge_len / 2.0)
  else:
    newnode.edge_length = prev_edge_len
    curr_edge_child_node.edge_length = (target_node_branch_len / 2.0)
  # end modify - sourya
  
  # now place the previous pruned subtree as the child of this new node
  newnode.add_child(new_subtree.seed_node)
  new_subtree.seed_node.edge_length = target_node_branch_len
  
  #inp_tree.update_splits()   
  