"""Cached BGP-LS table, scratch testing script"""
import yaml

import bgp_ls_vis.proto
import bgp_ls_vis.graphing


def main():
    """First method called when ran as script"""
    # To load a BGP-LS table from file instead of a gRPC connection, `connect` param is set false
    rpc = bgp_ls_vis.proto.GoBGPQueryWrapper(connect=False)

    # Calling get_lsdb with param `filename` set will trigger loading from file instead of RPC
    # There are several sample topologies under /tests/
    # To dump a topology to yaml as we have done, yaml.dump(GoBGPQueryWrapper.dump())
    lsdb = rpc.get_lsdb(filename="bgp-ls_table_dumps/18-node-isis-w-bcast-segment.yaml")
    graph1 = bgp_ls_vis.graphing.build_nx_from_lsdb(lsdb)
    lsdb = rpc.get_lsdb(filename="bgp-ls_table_dumps/solar_table.yaml")
    graph2 = bgp_ls_vis.graphing.build_nx_from_lsdb(lsdb)
    lsdb = rpc.get_lsdb(filename="bgp-ls_table_dumps/junos_bgpls_nopsn.yml")
    graph3 = bgp_ls_vis.graphing.build_nx_from_lsdb(lsdb)

    # print(yaml.dump(lsdb))  # Print filtered LSDB to stdout, optional dev assistance

    bgp_ls_vis.graphing.draw_pyplot_graph(graph1)
    bgp_ls_vis.graphing.draw_pyplot_graph(graph2)
    bgp_ls_vis.graphing.draw_pyplot_graph(graph3)


if __name__ == "__main__":
    main()
