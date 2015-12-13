import networkx as nx
import network_algos as algs

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

# given apsp, gimme diameter
def diameter_from_apsp(dist):
  return numpy.max(dist)

def test_big_graph():
  graph = fetch_fb_graph()
  print "ifub"
  print algs.ifub(graph, 0)
  print "normal library"
  print nx.diameter(graph)

def test_small_graph():
  graph = create_dummy()
  dist = algs.floyd_warshall(graph)
  print diameter_from_apsp(dist)

def test_timer():
  graph = fetch_fb_graph()

  # around 6.247 seconds
  print "ifub"
  print algs.ifub(graph, 0)

  # around 132.322 seconds
  print "normal library"
  print algs.normal_diameter(graph) 

def main():
  print "calculating diameter"
  test_timer()

main()
