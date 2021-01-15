import bgp_ls_vis.proto
import bgp_ls_vis.graphing
import bgp_ls_vis.dashboard


gobgp_target = {"target_ipv4_address": "172.20.10.2", "target_rpc_port": 50051}
rpc = bgp_ls_vis.proto.GoBGPQueryWrapper(**gobgp_target)

bgp_ls_vis.dashboard.main(rpc)
