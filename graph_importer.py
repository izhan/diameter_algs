import networkx as nx

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
  g = graph.subgraph(nodes)
  return nx.convert_node_labels_to_integers(g)

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