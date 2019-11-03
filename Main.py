import random

import matplotlib.pyplot as plt
import networkx as nx
from numpy.core.defchararray import lower


def merge_two_dicts(dict, dict2, dict2_name):
    for key, value in dict2.items():
        if dict.get(key) is None:
            dict[key] = {}
        dict[key][dict2_name] = value
    return dict


def merge_dicts(dicts):
    init_dict = {}
    for key, value in dicts.items():
        init_dict = merge_two_dicts(init_dict, value, key)
    return init_dict


def draw(G):
    types = nx.get_node_attributes(G, 'type')
    pos = nx.get_node_attributes(g, 'pos')
    xs = nx.get_node_attributes(G, 'x')
    ys = nx.get_node_attributes(G, 'y')
    zs = nx.get_node_attributes(G, 'z')
    bs = nx.get_node_attributes(G, 'b')
    ls = nx.get_node_attributes(G, 'l')
    rs = nx.get_node_attributes(G, 'r')

    labels = merge_dicts({
        "x": xs,
        "y": ys,
        "z": zs,
        "b": bs,
        "l": ls,
        "r": rs,
        "t": types
    })

    labels_traversed = {}

    for key, value in labels.items():
        label = ""
        for ikey, value in value.items():
            label += ikey + "=" + str(value) + " "
        labels_traversed[key] = label

    nx.draw(G, labels=labels_traversed, pos=pos)
    plt.show()


def create_rectangle():
    g = nx.Graph()
    g.add_node('v1', type='v', pos=(0, 0))
    g.add_node('v2', type='v', pos=(15, 0))
    g.add_node('v3', type='v', pos=(15, 15))
    g.add_node('v4', type='v', pos=(0, 15))
    g.add_node('i1', type='i', pos=(12, 6))
    g.add_node('i2', type='i', pos=(4, 10))
    g.add_edge('v1', 'v2')
    g.add_edge('v2', 'v3')
    g.add_edge('v3', 'v4')
    g.add_edge('v4', 'v1')
    g.add_edge('v1', 'v3')
    g.add_edge('i1', 'v1')
    g.add_edge('i1', 'v2')
    g.add_edge('i1', 'v3')
    g.add_edge('i2', 'v1')
    g.add_edge('i2', 'v3')
    g.add_edge('i2', 'v4')

    return g


def find_i_nodes(g):
    nodes = dict(g.nodes)
    i_node_list = []
    for key in nodes:
        if 'i' == lower(nodes[key]['type']):
            i_node_list.append((key, nodes[key]))

    return i_node_list


def get_triangle_nodes(g, node_name):
    triangle_nodes = list(g.neighbors(node_name))
    triangle_nodes.append(node_name)

    return triangle_nodes


def check_if_triangle_should_be_refined(g, node_name):
    triangle_nodes = get_triangle_nodes(g, node_name)
    triangle_graph = g.subgraph(triangle_nodes)
    # invoke function to estimate approximation error passing triangle_graph as an argument
    # approximation_error = 0.1
    epsilon = 2
    draw(triangle_graph)

    return random.randint(2, 3) > epsilon


def mark_triangles_to_refine(g):
    # it may be done in one iteration i.e:
    # when type == 'i' then execute logic in below loop
    i_node_list = find_i_nodes(g)
    attributes = {}
    for i_node in i_node_list:
        node_name = i_node[0]
        is_node_to_mark = check_if_triangle_should_be_refined(g, node_name)
        attributes.update(
            {
                node_name: {
                    'r': is_node_to_mark
                }
            }
        )
    nx.set_node_attributes(g, attributes)

    # to check if 'marked' attribute is set
    print(nx.get_node_attributes(g, 'r'))
    return g


if __name__ == "__main__":
    g = create_rectangle()
    marked_graph = mark_triangles_to_refine(g)
    draw(marked_graph)
