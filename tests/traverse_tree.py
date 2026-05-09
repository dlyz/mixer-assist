import os

from xair_client.client import XAirConnection
from xair_client.nodes_base import MixerNode, MixerPropertyNode
from xair_client.text_tree_service import MixerTextTreeService
from xair_client.nodes.mixer import Mixer

from dotenv import load_dotenv

load_dotenv()


def main():
    ip = os.environ["MIXER_IP"]
    with XAirConnection(ip=ip, timeout=1.0) as client:
        print(f"Connected to {ip}, mixer model: {client.mixer_model.id}")

        silent = True

        mixer = Mixer(client)
        text_tree = MixerTextTreeService(mixer)

        def dfs(path: str, node: MixerNode):
            content = text_tree.expand_node(path, verbose=True)
            if not silent:
                print(content)
                print()

            for name, child in node.children:
                subpath = f"{path}/{name}"
                if isinstance(child, MixerPropertyNode):
                    content = text_tree.expand_node(subpath, verbose=True)
                    if not silent:
                        print(content)
                        print()
                else:
                    dfs(subpath, child)

        dfs("/", mixer)

    print("Test succeeded")


main()
