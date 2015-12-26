import networkx as nx
import network_algos as algs
import graph_importer as graph_importer

FACEBOOK_FILENAME = "facebook_data/facebook_combined.txt"
ENRON_FILENAME = "other_data/email-Enron.txt"
ASTROPH_FILENAME = "other_data/ca-AstroPh.txt"
GNUTELLA_FILENAME = "other_data/p2p-Gnutella08.txt"

# given apsp, gimme diameter
def diameter_from_apsp(dist):
  return numpy.max(dist)

def test_big_graph():
  graph = graph_importer.graph_from_file(FACEBOOK_FILENAME)
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
  graph = graph_importer.graph_from_file(file)
  arbitrary_vertex = next(iter(graph))
  
  print "ifub"
  print algs.ifub(graph, arbitrary_vertex)

  print "bounding_diameters"
  print algs.bounding_diameters(graph)

  # # around 132.322 seconds
  # print "normal library"
  # print algs.normal_diameter(graph) 

def main():
  print "calculating diameter"
  test_timer(FACEBOOK_FILENAME)
  test_timer(ENRON_FILENAME)
  # annoying b/c nodes dont start from 0
  test_timer(ASTROPH_FILENAME)
  test_timer(GNUTELLA_FILENAME)

import pdb, traceback, sys

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
