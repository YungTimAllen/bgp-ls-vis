"""Graphing tools for bgp_ls_vis"""
import networkx as nx
import matplotlib.pyplot as plt


def lsa_cost(lsa: dict) -> int:
    """Checks a given LSA to see if the igpMetric attribute is present in the lsattr

    Args:
        lsa: lsa dict object from lsdb (See: GoBGPQueryWrapper.build_nx_from_lsdb)

    Returns:
        Integer value for cost inside lsattr if present, else zero
    """
    if "igpMetric" not in lsa["lsattribute"]["link"].keys():
        lsa["lsattribute"]["link"]["igpMetric"] = 0
    return lsa["lsattribute"]["link"]["igpMetric"]


def lsa_pseudonode(lsa: dict) -> bool:
    """Checks given LSA for value pf pseudonode key if present

    Args:
        lsa: lsa dict object from lsdb (See: GoBGPQueryWrapper.build_nx_from_lsdb)

    Returns:
        bool value for pseudonode status inside lsa if present, else false
    """
    b_pseudonode = False
    if "pseudonode" in list(lsa["localNode"].keys()):
        b_pseudonode = lsa["localNode"]["pseudonode"]
    return b_pseudonode


def build_nx_from_lsdb(lsdb: list) -> nx.MultiDiGraph:
    """Given list of LSAs (LSDB), builds NetworkX Graph object

    Args:
        lsdb: List<Dict> pulled from GoBGPQueryWrapper.get_lsdb call

    Returns:
        NetworkX MultiDiGraph object
    """
    graph = nx.MultiDiGraph()

    # First iteration over LSDB initialises all nodes to the nx.graph object
    # Nodes are keyed by igpRouterId - this is renamed to TLV137 values if known later
    for lsa in lsdb:
        if lsa["type"] == "Node":
            graph.add_node(lsa["localNode"]["igpRouterId"])

    # new_name_map is a dict keyed by node (IGP RID) [oldname], where value is string for new-name
    # - Value is pulled from TLV137 if present in Node LSA
    new_name_map = {}
    # node_lsa_attrs is a dict keyed by node (IGP RID) and value: a dict of arb. data
    # - node_lsa_attrs[node]['lsa'] is the raw LSA seen in the LSDB given from rpc.get_lsdb
    # - node_lsa_attrs[node]['prefixes'] is a list of all associated Prefix LSAs for this node (key)
    node_lsa_attrs = {node: {"lsa": None, "prefixes": []} for node in graph.nodes}

    for lsa in lsdb:
        igp_rid = lsa["localNode"]["igpRouterId"]

        if lsa["type"] == "Link":  # If LSA is an Edge ...
            graph.add_edge(
                igp_rid,
                lsa["remoteNode"]["igpRouterId"],
                cost=lsa_cost(lsa),
                pseudonode="pseudonode" in lsa["remoteNode"].keys(),
                color="black",
                weight=1,
                lsa=lsa,  # We store arbitrary data: the lsattrs of the NLRI
            )

        # Node type LSAs might have the node's true name (TLV137) under lsattrs
        # so we prep a rename map (Dict where key: old name, val: new name)
        # and call nx.relabel_nodes for the current graph, where `copy=false` renames in-place
        if lsa["type"] == "Node":
            if lsa["lsattribute"]["node"]:
                # We check for existence of TLV137
                if "name" in list(lsa["lsattribute"]["node"].keys()):
                    # and prep the new-name dict which is keyed by old name (IGP RID)
                    old_name = igp_rid
                    new_name = lsa["lsattribute"]["node"]["name"]
                    new_name_map[old_name] = new_name

                # Node stores pseudonode state under key localNode
                # We prep this as arb. data to node_lsa_attrs
                node_lsa_attrs[igp_rid]["pseudonode"] = lsa_pseudonode(lsa)

                # Node type LSAs come with lsattrs, and we want to add those as arb. data
                # to the nx.node in the nx.graph. e.g. Bandwidth stuff from the TED is here
                node_lsa_attrs[igp_rid]["lsa"] = lsa

        # Prefixes are associated with a node, which we initially build under IGP RID
        # Whilst this will be renamed later (to the TLV137 value), it is currently still
        # IGP RID until this initial loop ends. So, we can start assocaiting prefix LSAs
        # to node objects.
        if lsa["type"] == "Prefix":
            node_lsa_attrs[igp_rid]["prefixes"].append(lsa)

    # node_lsa_attrs is prepped with key:node, value:arbitrary data (k/v pairs)
    # nx.set_node_attributes
    # """If you provide a dictionary of dictionaries as the second argument, the outer dictionary
    #    is assumed to be keyed by node to an inner dictionary of node attributes for that node:"""
    # https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.set_node_attributes.html
    nx.set_node_attributes(graph, node_lsa_attrs)

    # Node relabel is called AFTER the networkx graph is built from the LSDB
    nx.relabel_nodes(graph, new_name_map, copy=False)

    return graph


def draw_pyplot_graph(graph: nx.Graph):
    """Will open a window with the NetworkX graph object drawn

    Given NetworkX graph object, calls matplotlib.pyplot to draw then show the graph object

    Args:
        graph: NetworkX Graph object, or derivative

    Requires:
        import matplotlib.pyplot as plt
    """
    # Node colouring + Pseudonode handling
    # Create dict keyed by node, value is pseudonode status (bool)
    pns = {v: d["pseudonode"] for _, v, d in graph.edges(data=True)}
    # color_map is an ordered list, where order is for `node in graph`
    # This is the same order nx.draw encounters nodes
    color_map = [
        "green" if not node in list(pns.keys()) else "blue" if pns[node] else "green"
        for node in graph
    ]

    # Edge labelling
    edge_labels = {
        (u, v): d["cost"] if d["cost"] > 0 else "" for u, v, d in graph.edges(data=True)
    }

    # Edge Colouring
    edge_color = nx.get_edge_attributes(graph, "color").values()

    # Edge weight
    edge_weight = nx.get_edge_attributes(graph, "weight").values()

    pos = nx.spring_layout(graph)
    nx.draw(
        graph,
        pos,
        node_color=color_map,
        edge_color=edge_color,
        width=list(edge_weight),
        with_labels=True,
        font_size=7,
    )
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7
    )
    plt.show()


def draw_graphviz_graph(graph: nx.Graph, outfile: str):
    """Draws NetworkX graph object to file using Graphviz

    Args:
        graph: NetworkX Graph object, or derivative

    Requires:
        pip3 install pygraphviz
        redhat: graphviz-devel python3-dev graphviz pkg-config
        debian: python3-dev graphviz libgraphviz-dev pkg-config
    """

    # Weight labels
    # Edges are returned as tuples with optional data in the order (node, neighbor, data).
    # https://networkx.org/documentation/networkx-1.10/reference/generated/networkx.Graph.edges.html
    for _, _, data in graph.edges(data=True):
        data["label"] = f"Cost: {data.get('cost', '')}"

    graph = nx.drawing.nx_agraph.to_agraph(graph)
    graph.layout("dot")
    graph.draw(outfile)
