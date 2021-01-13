"""Cached BGP-LS table, scratch testing script"""
import yaml

# RPC tools
from proto import GoBGPQueryWrapper

# Graphing tools
import graphing


def main():
    """First method called when ran as script"""
    # To load a BGP-LS table from file instead of a gRPC connection, `connect` param is set false
    rpc = GoBGPQueryWrapper(connect=False)

    # Calling get_lsdb with param `filename` set will trigger loading from file instead of RPC
    # There are several sample topologies under /tests/
    # To dump a topology to yaml as we have done, yaml.dump(GoBGPQueryWrapper.dump())
    lsdb = rpc.get_lsdb(filename="../tests/bgp-ls_table_dumps/18-node-isis-w-bcast-segment.yaml")
    #lsdb = rpc.get_lsdb(filename="../tests/bgp-ls_table_dumps/solar_table.yaml")
    #lsdb = rpc.get_lsdb(filename="../tests/bgp-ls_table_dumps/junos_bgpls_nopsn.yml")

    graph = graphing.build_nx_from_lsdb(lsdb)

    print(yaml.dump(lsdb))  # Print filtered LSDB to stdout, optional dev assistance

    graphing.draw_pyplot_graph(graph)


if __name__ == "__main__":
    main()
