import os

from xair_client.client import XAirConnection
from xair_client.text_tree_service import MixerTextTreeService
from xair_client.nodes.mixer import Mixer
from xair_client.nodes.effects.all import FxType

from dotenv import load_dotenv

load_dotenv()


def main():
    ip = os.environ["MIXER_IP"]
    with XAirConnection(ip=ip, timeout=1.0) as client:
        print(f"Connected to {ip}, mixer model: {client.mixer_model.id}")

        silent = True

        mixer = Mixer(client)
        text_tree = MixerTextTreeService(mixer)

        for type in FxType:
            mixer.fx[1].effect_type = type
            content = text_tree.expand_node("/fx/1/effect_params", verbose=True)
            if not silent:
                print(content)
                print()

    print("Test succeeded")


main()
