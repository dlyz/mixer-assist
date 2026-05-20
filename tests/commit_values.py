import logging
import os
from pathlib import Path
import random
from typing import Callable
import argparse

from xair_client.client import XAirCommitConfirmFailed, XAirConnection
from xair_client.nodes.effects.all import FxType
from xair_client.nodes_base import MixerNode, MixerProperty, MixerPropertyNode
from xair_client.properties.primitive import BoolProperty, FloatProperty
from xair_client.nodes.mixer import Mixer
from xair_client.properties.sources import AnalogSourceProperty

from dotenv import load_dotenv


load_dotenv()
# logging.basicConfig()
# logging.getLogger("xair_client").setLevel(logging.DEBUG)

STEPS_COUNT = 50


def main():
    # TODO: make tests for other type of values to,
    # but have to be careful to exclude phantom power switch,
    # maintain mutes on all the things
    # and do not test non-readable actions like snapshot actions.
    ip_from_env = os.getenv("MIXER_IP") or None

    parser = argparse.ArgumentParser(description="Test module configuration.")
    parser.add_argument("--ip", required=(ip_from_env is None), default=ip_from_env, help="Mixer IP address.")
    parser.add_argument("--with-headamp-gain", action="store_true", help="Test headamps gain (default: false).")
    parser.add_argument(
        "--all-channels", action="store_true", help="Test all channels, otherwise only first one (default: false)"
    )
    parser.add_argument(
        "--all-buses", action="store_true", help="Test all channels, otherwise only first one (default: false)"
    )
    parser.add_argument("--no-fx-params", action="store_true", help="Skips fx params testing.")
    parser.add_argument("--fix-fx-params", action="store_true", help="Fixes grid_size in fx params js(on) definitions.")

    args = parser.parse_args()
    ip: str = args.ip
    with_headamp_gain: bool = args.with_headamp_gain
    all_channels: bool = args.all_channels
    all_buses: bool = args.all_buses
    no_fx_params: bool = args.no_fx_params
    fix_fx_params: bool = args.fix_fx_params

    with XAirConnection(ip=ip, timeout=1.0) as client:
        print(f"Connected to {ip}, mixer model: {client.mixer_model.id}")

        mixer = Mixer(client)

        gen = random.Random(42)

        # mute all for safety reasons
        def mute(path: str, node: MixerPropertyNode):
            if node.name == "mute" and isinstance(node.prop, BoolProperty):
                # testing that all transitions work and muting in the end
                node.value = True
                node.value = False

                node.value = True

        traverse_props("/", mixer, mute)

        def dsisable_input(path: str, node: MixerPropertyNode):
            if isinstance(node.prop, AnalogSourceProperty):
                node.value = 0

        traverse_props("/", mixer, dsisable_input)

        grid_deductions: list[tuple[MixerPropertyNode, int]] = []

        def test(path: str, node: MixerPropertyNode):
            if isinstance(node.prop, FloatProperty):
                if not with_headamp_gain and node.parent in mixer.headamps and node.name == "gain":
                    return

                commit_failed = False
                try:
                    for i in range(0, STEPS_COUNT):
                        if i == 0:
                            value = node.prop.maximum
                        else:
                            value = gen.uniform(node.prop.minimum, node.prop.maximum)

                        try:
                            node.value = value
                        except XAirCommitConfirmFailed as ex:
                            print(f"Failed for {path} = {value}: {ex}")
                            commit_failed = True
                            break

                    if commit_failed:
                        samples: list[float] = []
                        for i in range(0, STEPS_COUNT):
                            value = gen.uniform(node.prop.minimum, node.prop.maximum)
                            try:
                                node.value = value
                            except XAirCommitConfirmFailed as ex:
                                samples.append(ex.actual_value)

                        guessed_grid_size = guess_grid_size(samples)
                        if guessed_grid_size is not None:
                            grid_deductions.append((node, guessed_grid_size))
                        print(f"{path} guessed grid size = {guessed_grid_size}")
                        print()

                finally:
                    node.value = node.prop.minimum

        def test_node_filter(path: str, node: MixerNode):
            if not all_channels and node in mixer.channels:
                return node == mixer.channels[1]
            if not all_buses and node in mixer.buses:
                return node == mixer.buses[1]
            if path.endswith("effect_params"):
                return False
            return True

        traverse_props("/", mixer, test, test_node_filter)

        if not no_fx_params:
            print("Starting fx params tests for all types")
            for type in FxType:
                grid_deductions.clear()
                print(type, type.name)

                mixer.fx[1].effect_type = type
                traverse_props("/fx/1/effect_params", mixer.fx[1].effect_params, test)

                if fix_fx_params and grid_deductions:
                    import yaml

                    path = Path(__file__).resolve().parents[1] / "fx_types" / "types" / f"type{type.value}.yaml"
                    with path.open(encoding="utf-8") as stream:
                        data = yaml.safe_load(stream)

                    for node, grid_size in grid_deductions:
                        prop = node.prop
                        assert isinstance(prop, MixerProperty)
                        param = next(
                            p
                            for p in data["parameters"]
                            if prop.address_provider(node.parent).endswith("/" + p["number"])
                        )
                        param["grid_size"] = grid_size

                    with path.open("w", encoding="utf-8") as stream:
                        yaml.safe_dump(data, stream, sort_keys=False, allow_unicode=True)

    print("Test succeeded")


def traverse_props(
    path: str,
    node: MixerNode,
    action: Callable[[str, MixerPropertyNode], None],
    node_filter: Callable[[str, MixerNode], bool] | None = None,
):
    for name, child in node.children:
        subpath = f"{path}/{name}"
        if isinstance(child, MixerPropertyNode):
            action(subpath, child)
        else:
            if not node_filter or node_filter(subpath, child):
                traverse_props(subpath, child, action, node_filter)


def guess_grid_size(samples: list[float], max_size=4000, eps=1e-5):
    # Standardize data: unique, sorted, and strictly within [0, 1]/hea
    cleaned = sorted(list(set(s for s in samples if 0.0 <= s <= 1.0)))

    if len(cleaned) < 2:
        raise ValueError(f"not enough data. original samples: {samples[:100]}")

    for grid_cells in range(1, max_size + 1):
        step = 1.0 / grid_cells
        max_residual = max(abs(sample - round(sample / step) * step) for sample in cleaned)
        if max_residual < eps:
            return grid_cells + 1

    return None


main()
