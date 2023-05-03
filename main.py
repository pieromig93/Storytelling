# per creare una rete in python si può utilizzare una libreria chiamata networkx

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from IPython.display import HTML
test_graph = nx.Graph()

G = nx.petersen_graph()
nx.draw(G, with_labels=True, font_weight='bold')
net=Network(filter_menu=True)
net.from_nx(G)
net.save_graph("./test.html")
HTML(filename="./test.html")
