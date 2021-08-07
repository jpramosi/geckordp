""" This is a helper script to create a formatted output log from pcap-dumps.
"""
import argparse
import json
from pathlib import Path
from scapy.all import PcapReader, re, Raw, TCP, IP


class JSONNode():

    def __init__(self, idx: int, packet_idx: int):
        self.idx = idx
        self.packet_idx = packet_idx
        self.packets_list = []

    def __str__(self):
        return f"i:{self.idx} p:{self.packet_idx} c:{self.packets_list}"

    def __repr__(self):
        return str(self)


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=str, default="",
                        help="Input file to convert to.")
    parser.add_argument("-p", "--port", type=int, default=6000,
                        help="The port of the remote debug server.")
    args, _ = parser.parse_known_args()

    input_file = Path(args.input).absolute()
    if (not input_file.exists() or input_file.is_dir()):
        print(f"invalid input file '{input_file}'")

    buffer = ""
    req_brackets = []
    res_brackets = []
    gpackets = []
    with PcapReader(str(input_file)) as packets:
        for packet_idx, p in enumerate(packets):

            # format payload and append to list
            payload = str(p[Raw].load)
            payload = payload.replace("b'", "")[:-1]
            gpackets.append(payload)

            # check whether it uses TCP protocol
            if p.haslayer(TCP) and p.haslayer(Raw):
                if (len(payload) < 4):
                    continue
                root_nodes = []

                # helper function to stack or pop nodes
                def parse(brackets):
                    for idx, c in enumerate(payload):
                        if (c == "{"):
                            brackets.append(JSONNode(idx, packet_idx))
                            continue
                        if (c == "}"):
                            if (len(brackets) <= 0):
                                break
                            node = brackets.pop()
                            # check if root element
                            if (len(brackets) == 0):
                                root_nodes.append(
                                    (node, JSONNode(idx, packet_idx)))
                            continue
                    return brackets

                # parse and check whether it is a request
                # or response by checking the destination port
                if (args.port == p[TCP].dport):
                    req_brackets = parse(req_brackets)
                    if (len(req_brackets) > 0):
                        req_brackets[0].packets_list.append(packet_idx)
                        continue
                    buffer += "->REQUEST\n"
                else:
                    res_brackets = parse(res_brackets)
                    if (len(res_brackets) > 0):
                        res_brackets[0].packets_list.append(packet_idx)
                        continue
                    buffer += "<-RESPONSE\n"

                # one packet may contain multiple root nodes
                # one root node is just a json message
                for node in root_nodes:

                    new_payload = ""
                    # if it's only a single packet, no need to merge payloads
                    if (len(node[0].packets_list) <= 0):
                        # set new payload which contains only the json data
                        new_payload = payload[node[0].idx:node[1].idx+1]
                    else:
                        adjust_offset = 1
                        # merge payloads and its related sizes
                        for pidx in node[0].packets_list:
                            adjust_offset += len(gpackets[pidx])
                            new_payload += gpackets[pidx]
                        # append last packet
                        new_payload += gpackets[node[1].packet_idx]
                        # shift index by new offset
                        node[1].idx += adjust_offset
                        # set new payload which contains only the json data
                        new_payload = new_payload[node[0].idx:node[1].idx]

                    # format payload
                    new_payload = new_payload.replace("'", "\\'")
                    try:
                        new_payload = json.loads(new_payload, strict=False)
                        new_payload = json.dumps(new_payload, indent=2)
                    except Exception as ex:
                        print(f"{ex}\n\n", new_payload)
                        return 1
                    new_payload = "\t".expandtabs(
                        8) + new_payload.replace("\n", "\n\t".expandtabs(8))
                    buffer += f"{new_payload}\n"
    

    # write buffer to the same path
    output_file = f"{input_file.parent.joinpath(input_file.stem)}.log"
    with open(output_file, "w") as f:
        f.write(buffer)
    print(f"converted pcap-dump in '{output_file}'")



if __name__ == "__main__":
    main()
