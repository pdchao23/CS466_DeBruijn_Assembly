# de Bruijn assembly option
import argparse
import sys
import networkx as nx


def readFile():
    # print('Argument List:', str(sys.argv))

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    with open(args.filename) as file_param:
        file_param = file_param.read().splitlines()

    # print(file_param)
    return file_param


def createGraph(sequences):
    d = {}
    last_right = ''
    counter = 0
    for s in sequences:
        l, r = s[:-1], s[1:]
        # print("Left: " + l)
        # print("Right: " + r)
        if l not in d:
            d[l] = list()
        if r not in d:
            d[r] = list()
        if last_right != l and counter != 0:
            d[last_right].append(l)

        d[l].append(r)
        last_right = r
        counter += 1

    # print(d)

    graph = nx.MultiDiGraph()
    for key in d:
        graph.add_node(key)
        for e in d[key]:
            graph.add_edge(key, e)

    # nx.draw(graph, with_labels=True)
    # plt.savefig("graph.png")
    return graph, d


def eulerianPath(graph, d):
    # Check if eulerian assumptions are met!

    # Check if the graph has an Euler circuit: All vertices have even degrees
    # check connected
    # in degree and out degree are the same
    # 0 or 2 semibalanced nodes

    temp = graph.to_undirected()
    if not nx.is_connected(temp):
        # print("not connected")
        return "-1"

    num_semi_nodes = 0
    nodes = list(graph.nodes)

    for n in nodes:
        if abs(graph.out_degree(n) - graph.in_degree(n)) == 1:
            num_semi_nodes += 1
        elif abs(graph.out_degree(n) - graph.in_degree(n)) > 1:
            return "-1"

    if not (num_semi_nodes == 0 or num_semi_nodes == 2):
        return "-1"

    start_node = nodes[0]
    curr_path = [start_node]

    circuit = []

    while curr_path:
        curr_v = curr_path[-1]
        if d[curr_v]:
            next_v = d[curr_v].pop()
            curr_path.append(next_v)
        else:
            circuit.append(curr_path.pop())

    out_arr = []
    for i in range(len(circuit) - 1, -1, -1):
        out_arr.append(circuit[i])
    # print(out_arr)

    out = ""
    counter = 0
    for string in out_arr:
        if counter == 0:
            out += string
        else:
            out += string[-1]
        counter += 1

    return out


substrings = readFile()
graph, d = createGraph(substrings)
out = eulerianPath(graph, d)
f = open("out.txt", "w")
f.write(out)
f.close()
print(out)
