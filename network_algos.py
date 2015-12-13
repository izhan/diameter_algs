import networkx as nx
import numpy as numpy
import time as time

def timing(f):
  def wrap(*args):
    print "---------------------"
    print 'TIMING: %s' % (f.func_name)
    time1 = time.time()
    ret = f(*args)
    time2 = time.time()
    print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
    print 'return: %s' % (ret)
    print "---------------------\n"
    return ret
  return wrap

# based off of networkx single_source_shortest_path_length implementation
# returns array of vertices: 
# [vertices 0 dist away from source, vertices 1 dist away from source, ...]
def get_fringe_list(graph, source, cutoff=None):
  seen = {}                  # level (number of hops) when seen in BFS
  level = 0                  # the current level
  nextlevel = {source:1}  # dict of nodes to check at next level
  fringes = []
  while nextlevel:
      thislevel = nextlevel  # advance to next level
      nextlevel = {}         # and start a new list (fringe)
      for v in thislevel:
          if v not in seen:
              seen[v] = level # set the level of vertex v
              nextlevel.update(graph[v]) # add neighbors of v
              if len(fringes) == level:
                fringes.append([v])
              else:
                fringes[level].append(v)
      if (cutoff is not None and cutoff <= level):  break
      level=level+1
  del seen
  return fringes

# generate apsp 2d array
def floyd_warshall(graph):
  n = graph.order()
  
  # init n x n array of min dist w/ inf distance
  dist = numpy.empty((n,n,))
  dist[:] = float("inf")

  # dist to self is 0, dist to adj is 1
  for i in range(0, n):
    dist[i][i] = 0
    for j in graph.adj[i].keys():
      dist[i][j] = 1

  for k in range(0, n):
    for i in range(0, n):
      for j in range(0, n):
        if dist[i][j] > dist[i][k] + dist[k][j]:
          dist[i][j] = dist[i][k] + dist[k][j] 

  return dist

def calculate_max_ecc(graph, nodes):
  max_ecc = 0
  for node in nodes:
    ecc = nx.eccentricity(graph, node)
    if ecc > max_ecc:
      max_ecc = ecc
  return max_ecc

# from http://www.sciencedirect.com/science/article/pii/S0304397512008687
# calculates fringe list from one BFS. gets height of tree
# lower bound = height of tree
# upper bound = twice height of tree
# every iteration, calculate eccentricities of all leaves of tree
@timing
def ifub(graph, u, l=0, k=0):
  fringes = get_fringe_list(graph, u)

  i = len(fringes) - 1
  lb = max(i, l)
  ub = 2 * i

  while ub - lb > k:
    b = calculate_max_ecc(graph, fringes[i])
    if max(lb, b) > 2 * (i - 1):
      return max(lb, b)
    else:
      lb = max(lb, b)
      ub = 2 * (i - 1)
    i -= 1

  return lb

# same as calling nx.diamter directly with a timer
@timing
def normal_diameter(graph):
  return nx.diameter(graph)

