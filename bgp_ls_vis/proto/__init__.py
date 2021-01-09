"""t"""
# Standard Imports
from collections import defaultdict
from google.protobuf.json_format import MessageToDict

# RPC & GoBGP imports
import grpc
from . import gobgp_pb2 as gobgp
from . import gobgp_pb2_grpc
from . import attribute_pb2


class GoBGPQueryWrapper:
    """Class to add abstraction for RPC calls to a GoBGP Instance"""

    def __init__(self, target_ipv4_address, target_rpc_port):
        """Constructor initialises RPC session

        Args:
            target_ipv4_address: Management IPv4 Address of GoBGP instance
            target_rpc_port: Management Port of GoBGP Instance
        """
        channel = grpc.insecure_channel(f"{target_ipv4_address}:{target_rpc_port}")
        self.stub = gobgp_pb2_grpc.GobgpApiStub(channel)

    @staticmethod
    def __build_rpc_request() -> gobgp.ListPathRequest:
        """Builds a structured message for RPC query to get BGP-LS table

        Returns:
            gobgp.ListPathRequest: Structured message for RPC query
        """
        request = gobgp.ListPathRequest(
            table_type=gobgp.LOCAL,
            name="",
            family=gobgp.Family(afi=gobgp.Family.AFI_LS, safi=gobgp.Family.SAFI_LS),
            prefixes=None,
            sort_type=True,
        )
        return request

    def __get_bgp_ls_lsdb(self) -> list:
        """Submits RPC query (structured message) for BGP-LS table

        Sends gobgp.ListPathRequest object over RPC session to get BGP-LS NLRI objects

        Returns:
            List of NLRI objects for the BGP-LS AFI/SAFI

        Notes:
            To build required structured, message, calls __build_rpc_request() first
        """
        request = self.__build_rpc_request()
        response = self.stub.ListPath(request)
        rtn = [MessageToDict(nlri) for nlri in response]
        return rtn

    def get_lsdb(self) -> list:
        """Public method to get a version of the BGP-LS LSDB thats more concise

        The default return from calling self.stub.ListPath(request) is more verbose than the
        usecase requires, so this method cuts out most of the unncessary information and
        provides a concise structure of LSAs.

        Returns:
            List of Link and Prefix dict objects, filtered for only relevent key-value pairs
        """
        brib = self.__get_bgp_ls_lsdb()

        filtered_lsdb = []

        for lsa in brib:

            nlri = dict(lsa["destination"]["paths"][0]["nlri"]["nlri"])

            if nlri["@type"] == "type.googleapis.com/gobgpapi.LsLinkNLRI":
                filtered_lsdb.append(
                    {
                        "type": "Link",
                        "localNode": nlri["localNode"],
                        "remoteNode": nlri["remoteNode"],
                        "linkDescriptor": nlri["linkDescriptor"],
                    }
                )
            elif nlri["@type"] == "type.googleapis.com/gobgpapi.LsPrefixV4NLRI":
                filtered_lsdb.append(
                    {
                        "type": "Prefix",
                        "localNode": nlri["localNode"],
                        "prefixDescriptor": nlri["prefixDescriptor"],
                    }
                )

        return filtered_lsdb
