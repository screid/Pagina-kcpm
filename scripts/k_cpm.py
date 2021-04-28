from datetime import datetime
import networkx as nx
from networkx.algorithms.community import k_clique_communities

inicio = datetime.now()

G=nx.Graph()
G.add_node(1)
L = nx.read_weighted_edgelist("weight_file.txt")

k_cpm = list(range(5,31))
k_cpm.reverse()

for k in k_cpm:
    print ("Calculando con K: %s" % k)
    c = list(k_clique_communities(L, k))
    with open("k_cpm/cpm_cluster_K" + str(k) + ".txt","w") as archivo:
        for i in map(list, c):
            for j in i:
                archivo.write(str(j) + ' ')
            archivo.write('\n')
    print("Termine K: {}".format(k))

print ("Tiempo:", datetime.now() - inicio)