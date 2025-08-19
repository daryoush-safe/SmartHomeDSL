import networkx as nx


# Function to add nodes and edges to the NetworkX graph
def add_to_graph(graph, node, parent=None):
    if node is not None:
        # Add the current node to the graph
        graph.add_node(node.number, label=node.value)
        # If there's a parent, add an edge from the parent to the current node
        if parent is not None:
            graph.add_edge(parent.number, node.number)
        # add the child nodes to the graph
        for child in node.children:
            add_to_graph(graph, child, node)


def transform_ast_to_networkx(ast_root_node):
    graph = nx.DiGraph()
    add_to_graph(graph, ast_root_node)
    return graph


def show_ast(ast_root_node,file_name=None):
    from matplotlib import pyplot as plt
    from networkx.drawing.nx_pydot import graphviz_layout
    plt.rcParams["figure.figsize"] = (32, 18)
    graph = transform_ast_to_networkx(ast_root_node)
    pos = graphviz_layout(graph, prog="dot")
    nx.draw(graph, pos, node_size=700, labels=nx.get_node_attributes(graph, "label"), alpha=0.5, node_color="cyan",
            with_labels=True)
    ax = plt.gca()
    ax.margins(0.05)
    plt.axis("off")
    if file_name is not None:
        plt.savefig(fname=file_name+".jpg",dpi=512,bbox_inches='tight')
        plt.close()
    else:
        plt.show()
