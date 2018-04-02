import networkx as nx
import matplotlib.pyplot as plt
graph=nx.Graph()
nodes_list  = [1, 2, 3, 4, 5, 6]
edges_list  = [(1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (3, 6), (4, 6)]
edge_length = [1 + 0.1*i for i in range(len(edges_list))]
for n in nodes_list:
    graph.add_node(n)
for i,e in enumerate(edges_list):
    graph.add_edge(*e, weight=edge_length[i])
nx.draw_networkx(graph)

path_iter=nx.all_simple_paths(graph,4,5) #计算4,5间的所有路径

def get_path_length(graph,p):
    length = 0.0
    for i in range(len(p)-1):
        length += graph[p[i]][p[i+1]]['weight']
    return length

if __name__ == "__main__":
    plt.show(nx)
    print('type of path_iter:',type(path_iter))
    pathes=[]

    for p in path_iter:
        pathes.append(p)
    print(pathes)

    for p in pathes:
        print(get_path_length(graph, p), '\t', p)



