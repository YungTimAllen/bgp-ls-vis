import yaml
import bgp_ls_vis.proto
import bgp_ls_vis.graphing
import bgp_ls_vis.dashboard


def main():
    """Example usages of bgp_ls_vis package"""
    example1()
    # example2()
    # example3()


def example1():
    """Running the Dash (webgui) frontend"""

    # Prep RPC connection params to GoBGP instance
    # and create new connection object (GoBGPQueryWrapper)
    gobgp_target = {"target_ipv4_address": "172.20.10.2", "target_rpc_port": 50051}
    rpc = bgp_ls_vis.proto.GoBGPQueryWrapper(**gobgp_target)

    # Use the RPC connection to push an RPC query for the contents of the BGP-LS table
    # and return a concise LSDB
    # - get_lsdb() sends the RPC request and filters the LSDB to be "nice" autonomously
    lsdb = rpc.get_lsdb()

    # build_nx_from_lsdb will create a NetworkX graph object from the LSDB given by get_lsdb()
    graph = bgp_ls_vis.graphing.build_nx_from_lsdb(lsdb)

    # Call dashboard package
    bgp_ls_vis.dashboard.main(nx_graph=graph)


def example2():
    """Running the pyplot graph visualiser frontend"""

    # Same 3 steps from example1()
    gobgp_target = {"target_ipv4_address": "172.20.10.2", "target_rpc_port": 50051}
    rpc = bgp_ls_vis.proto.GoBGPQueryWrapper(**gobgp_target)
    lsdb = rpc.get_lsdb()

    # build_nx_from_lsdb will create a NetworkX graph object from the LSDB given by get_lsdb()
    graph = bgp_ls_vis.graphing.build_nx_from_lsdb(lsdb)

    bgp_ls_vis.graphing.draw_pyplot_graph(graph)


def example3():
    """Loading a cached LSDB from file, where an RPC connection is not required"""

    # To load a BGP-LS table from file instead of a gRPC connection, `connect` param is set false
    rpc = bgp_ls_vis.proto.GoBGPQueryWrapper(connect=False)

    # Calling get_lsdb with param `filename` set will trigger loading from file instead of RPC
    # There are several sample topologies under /tests/
    # To dump a topology to yaml as we have done, yaml.dump(GoBGPQueryWrapper.dump())
    dumps_dir = "../tests/bgp-ls_table_dumps"

    lsdb = rpc.get_lsdb(filename=f"{dumps_dir}/18-node-isis-w-bcast-segment.yaml")
    graph1 = bgp_ls_vis.graphing.build_nx_from_lsdb(lsdb)
    lsdb = rpc.get_lsdb(filename=f"{dumps_dir}/solar_table.yaml")
    graph2 = bgp_ls_vis.graphing.build_nx_from_lsdb(lsdb)
    lsdb = rpc.get_lsdb(filename=f"{dumps_dir}/junos_bgpls_nopsn.yml")
    graph3 = bgp_ls_vis.graphing.build_nx_from_lsdb(lsdb)

    bgp_ls_vis.graphing.draw_pyplot_graph(graph1)
    bgp_ls_vis.graphing.draw_pyplot_graph(graph2)
    bgp_ls_vis.graphing.draw_pyplot_graph(graph3)


if __name__ == "__main__":
    main()
