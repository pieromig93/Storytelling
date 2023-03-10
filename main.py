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

STATE_A, STATE_B, STATE_C = 0, 1, 2

class Conversation:
    actual_state = STATE_A

    def get_state(self):
        return self.actual_state

