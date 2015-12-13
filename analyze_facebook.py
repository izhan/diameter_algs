import networkx as nx
import network_algos as algs

FACEBOOK_FILENAME = "facebook_data/facebook_combined.txt"
ENRON_FILENAME = "other_data/email-Enron.txt"
ASTROPH_FILENAME = "other_data/ca-AstroPh.txt"
GNUTELLA_FILENAME = "other_data/p2p-Gnutella08.txt"

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

def graph_from_file(file):
  graph = fetch_graph(file)

  nodes = max(nx.connected_components(graph), key=len)
  return graph.subgraph(nodes)

def fetch_graph(file):
  print "fetching graph"
  edgelist = []

  f = open(file, "r")

  for line in f:
    edge = tuple([int(i) for i in line.split()])
    edgelist.append(edge)

  f.close()
  print "finished fetching graph " + file + "\n"
  return nx.from_edgelist(edgelist)

# given apsp, gimme diameter
def diameter_from_apsp(dist):
  return numpy.max(dist)

def test_big_graph():
  graph = graph_from_file(FACEBOOK_FILENAME)
  print "ifub"
  print algs.ifub(graph, 0)
  print "normal library"
  print nx.diameter(graph)

def test_small_graph():
  graph = create_dummy()
  dist = algs.floyd_warshall(graph)
  print diameter_from_apsp(dist)

def test_timer(file):
  print "Running for file: " + file
  graph = graph_from_file(file)
  arbitrary_vertex = next(iter(graph))

  # around 6.247 seconds
  print "ifub"
  print algs.ifub(graph, arbitrary_vertex)

  # # around 132.322 seconds
  # print "normal library"
  # print algs.normal_diameter(graph) 

def main():
  print "calculating diameter"
  test_timer(FACEBOOK_FILENAME)
  test_timer(ENRON_FILENAME)
  test_timer(ASTROPH_FILENAME)
  test_timer(GNUTELLA_FILENAME)

main()
