'''
Rappresentare efficientemente una rete sottoforma di grafo. 

La rete è composta da due strutture: 
    - nodi
    - archi orientati

La rete, a sua volta, può rappresentare uno steriotipo di conversazione oppure una "storia". Quindi è presente una gerarchia di reti: 
    - la prima è una rete conversazionale che rappresenta la tipologia di conversazione dovrà fare. Ad esempio parlando di Console romano 
        (VITA)--->(STUDI)--->(OPERE)
    
    - la seconda è di tipo culturale/fisico. Ad esempio, se consideriamo l'area degli scavi di Pompei potremmo dire che sulla via X sono situate adiacentemente
        domus (DOMUS 1)--->(DOMUS 2)--->(DOMUS 3)
                       |--->(DOMUS 9)--->(DOMUS 10)

Lo scopo di questo programma sarà quello di individuare quale percorso sul grafo risulta essere di maggior interesse per un utente che visita gli scavi ad esempio
prendendo delle scelte in funzione di ciò che significativamente piace all'utente. Quindi considerandone un profilo con degli interessi pesati

'''

# per creare una rete in python si può utilizzare una libreria chiamata networkx
import networkx as nx
import matplotlib.pyplot as plt
test_graph = nx.Graph()

G = nx.petersen_graph()
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

# STATE_A, STATE_B, STATE_C = 0, 1, 2

# class Conversation:
#     states = [STATE_A, STATE_B, STATE_C]
#     actual_state = -1

#     def __init__(self):
#         self.actual_state = STATE_A

#     def get_state(self):
#         return self.actual_state

#     def set_state(self, state):
#         self.actual_state = state

# # class Perl:
# #     next_perl
# #     previuos_perl
# #     topic =

# class User:
    
#     id = 0
#     # lista pesata
#     preferences = []
    
#     def __init__(self):
#         self.id = id+1


