"""RPC Connection, scratch testing script"""
import yaml
import bgp_ls_vis.proto
import bgp_ls_vis.graphing


def main():
    """First method called when ran as script"""
    gobgp_target = {"target_ipv4_address": "172.20.10.2", "target_rpc_port": 50051}
    rpc = bgp_ls_vis.proto.GoBGPQueryWrapper(**gobgp_target)

    lsdb = rpc.get_lsdb()
    graph = bgp_ls_vis.graphing.build_nx_from_lsdb(lsdb)

    print(yaml.dump(lsdb))  # Print filtered LSDB to stdout, optional dev assistance

    bgp_ls_vis.graphing.draw_pyplot_graph(graph)


if __name__ == "__main__":
    main()
