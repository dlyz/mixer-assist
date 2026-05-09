# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class ModeOptions(IntEnum):
    LP = 0
    HP = 1
    BP = 2
    NOTCH = 3

class WaveOptions(IntEnum):
    TRI = 0
    SIN = 1
    SAW = 2
    SAW_MINUS = 3
    RMP = 4
    SQU = 5
    RND = 6

    _LABELS = enum.nonmember({
        TRI: 'TRI',
        SIN: 'SIN',
        SAW: 'SAW',
        SAW_MINUS: 'SAW-',
        RMP: 'RMP',
        SQU: 'SQU',
        RND: 'RND',
    })

class PolesOptions(IntEnum):
    V_2 = 0
    V_4 = 1

    _LABELS = enum.nonmember({
        V_2: '2',
        V_4: '4',
    })

class MoodFilterFxParams(MixerNode):
    description = 'Mood Filter effect parameters (Modulation category).'

    speed = LogFloatProperty("01", 0.05, 20.0, decimals=2, units='Hz')
    depth = LinearFloatProperty("02", 0.0, 100.0, decimals=0, units='%')
    resonance = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    base = LogFloatProperty("04", 20.0, 15000.0, decimals=1, units='Hz')
    mode = EnumIntProperty("05", ModeOptions)
    mix = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')
    wave = EnumIntProperty("07", WaveOptions)
    phase = LinearFloatProperty("08", 0.0, 180.0, decimals=0, units='°')
    env_mod = LinearFloatProperty("09", -100.0, 100.0, decimals=0, units='%')
    attack = LogFloatProperty("10", 10.0, 250.0, decimals=0, units='ms')
    release = LogFloatProperty("11", 10.0, 500.0, decimals=0, units='ms')
    drive = LinearFloatProperty("12", 0.0, 100.0, decimals=0, units='%')
    poles = EnumIntProperty("13", PolesOptions)
    sidechain = BoolProperty("14")

