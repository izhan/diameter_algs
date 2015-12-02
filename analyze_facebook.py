import networkx as nx

GRAPH_FILENAME = "facebook_data/facebook_combined.txt"

def fetch_graph():
  print "fetching graph"
  edgelist = []

  f = open(GRAPH_FILENAME, "r")

  for line in f:
    edge = tuple(line.split())
    edgelist.append(edge)

  f.close()
  print "finished fetching graph"
  return nx.from_edgelist(edgelist)

def main():
  graph = fetch_graph()
  print "calculating diameter"
  print nx.diameter(graph)

main()
