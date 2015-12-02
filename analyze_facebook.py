import networkx as nx
import numpy as numpy

GRAPH_FILENAME = "facebook_data/facebook_combined.txt"

def create_dummy():
  edgelist = [
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (3, 6),
    (2, 4),
    (4, 5)
  ]

  return nx.from_edgelist(edgelist)

# based off of networkx single_source_shortest_path_length implementation
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

def fetch_fb_graph():
  print "fetching graph"
  edgelist = []

  f = open(GRAPH_FILENAME, "r")

  for line in f:
    edge = tuple([int(i) for i in line.split()])
    edgelist.append(edge)

  f.close()
  print "finished fetching graph"
  return nx.from_edgelist(edgelist)

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

# given apsp, gimme diameter
def diameter_from_apsp(dist):
  return numpy.max(dist)

def main():
  # graph = fetch_fb_graph()
  graph = create_dummy()
  print "calculating diameter"

  dist = floyd_warshall(graph)
  print diameter_from_apsp(dist)
  import pdb; pdb.set_trace()
  print nx.diameter(graph)

main()
