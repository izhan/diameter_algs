import networkx as nx
import numpy as numpy
import time as time
import operator

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

# same as calling nx.diamter directly with a timer
@timing
def normal_diameter(graph):
  return nx.diameter(graph)


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

# https://dl.acm.org/citation.cfm?id=2063748
# observation 1: given e(v), k = dist(v, w), e(v)-k <= e(w) <= e(v)+k
# observation 2: 
#   lower bound of diameter: maximum lower bound of eccentricity over all nodes
#   upper bound of diamter: maximum upper bound of eccentricity over all nodes 
#                           OR twice the smallest lower bound of eccentricity over all nodes
@timing
def bounding_diameters(graph):
  w_set = dict(graph.degree())
  n = len(w_set)

  e_lower = numpy.empty((n,))
  e_upper = numpy.empty((n,))
  e_lower[:] = -float("inf")
  e_upper[:] = float("inf")

  lower_bound = -float("inf")
  upper_bound = float("inf")

  while (lower_bound != upper_bound) and (len(w_set) != 0):
    v = max(w_set.iteritems(), key=operator.itemgetter(1))[0]
    path_lengths = nx.single_source_dijkstra_path_length(graph, v)
    ecc = max(path_lengths.iteritems(), key=operator.itemgetter(1))[1] # plucking highest value in dict

    lower_bound = max(lower_bound, ecc)
    upper_bound = min(upper_bound, 2 * ecc)
    temp = w_set.copy()
    for w in w_set:
      e_lower[w] = max(e_lower[w], max(ecc - path_lengths[w], path_lengths[w]))
      e_upper[w] = min(e_upper[w], ecc + path_lengths[w])
      if (e_upper[w] <= lower_bound and e_lower[w] >= upper_bound / 2) or e_lower[w] == e_upper[w]:
        del temp[w]
    w_set = temp

  return lower_bound

