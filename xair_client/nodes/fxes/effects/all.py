# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

from enum import IntEnum
from typing import TypeAlias
from .fx_00_hall_reverb import HallReverbFxParams
from .fx_01_ambience import AmbienceFxParams
from .fx_02_rich_plate_reverb import RichPlateReverbFxParams
from .fx_03_room_reverb import RoomReverbFxParams
from .fx_04_chamber_reverb import ChamberReverbFxParams
from .fx_05_plate_reverb import PlateReverbFxParams
from .fx_06_vintage_reverb import VintageReverbFxParams
from .fx_07_vintage_room import VintageRoomFxParams
from .fx_08_gated_reverb import GatedReverbFxParams
from .fx_09_reverse_reverb import ReverseReverbFxParams
from .fx_10_stereo_delay import StereoDelayFxParams
from .fx_11_3_tap_delay import Fx3TapDelayFxParams
from .fx_12_rhythm_delay import RhythmDelayFxParams
from .fx_13_stereo_chorus import StereoChorusFxParams
from .fx_14_stereo_flanger import StereoFlangerFxParams
from .fx_15_stereo_phaser import StereoPhaserFxParams
from .fx_16_dimensional_chorus import DimensionalChorusFxParams
from .fx_17_mood_filter import MoodFilterFxParams
from .fx_18_rotary_speaker import RotarySpeakerFxParams
from .fx_19_tremolo_panner import TremoloPannerFxParams
from .fx_20_suboctaver import SuboctaverFxParams
from .fx_21_delay_chamber import DelayChamberFxParams
from .fx_22_chorus_chamber import ChorusChamberFxParams
from .fx_23_flanger_chamber import FlangerChamberFxParams
from .fx_24_delay_chorus import DelayChorusFxParams
from .fx_25_delay_flanger import DelayFlangerFxParams
from .fx_26_modulation_delay import ModulationDelayFxParams
from .fx_27_dual_graphic_eq import DualGraphicEqFxParams
from .fx_28_stereo_graphic_eq import StereoGraphicEqFxParams
from .fx_29_dual_trueq import DualTrueqFxParams
from .fx_30_stereo_trueq import StereoTrueqFxParams
from .fx_31_dual_deesser import DualDeesserFxParams
from .fx_32_stereo_deesser import StereoDeesserFxParams
from .fx_33_stereo_xtec_eq1 import StereoXtecEq1FxParams
from .fx_34_dual_xtec_eq1 import DualXtecEq1FxParams
from .fx_35_stereo_xtec_eq5 import StereoXtecEq5FxParams
from .fx_36_dual_xtec_eq5 import DualXtecEq5FxParams
from .fx_37_wave_designer import WaveDesignerFxParams
from .fx_38_precision_limiter import PrecisionLimiterFxParams
from .fx_39_stereo_combinator import StereoCombinatorFxParams
from .fx_40_dual_combinator import DualCombinatorFxParams
from .fx_41_stereo_fair_compressor import StereoFairCompressorFxParams
from .fx_42_m_s_fair_compressor import MSFairCompressorFxParams
from .fx_43_dual_fair_compressor import DualFairCompressorFxParams
from .fx_44_stereo_leisure_compressor import StereoLeisureCompressorFxParams
from .fx_45_dual_leisure_compressor import DualLeisureCompressorFxParams
from .fx_46_stereo_ultimo_compressor import StereoUltimoCompressorFxParams
from .fx_47_dual_ultimo_compressor import DualUltimoCompressorFxParams
from .fx_48_dual_enhancer import DualEnhancerFxParams
from .fx_49_stereo_enhancer import StereoEnhancerFxParams
from .fx_50_dual_exciter import DualExciterFxParams
from .fx_51_stereo_exciter import StereoExciterFxParams
from .fx_52_stereo_imager import StereoImagerFxParams
from .fx_53_edison_ex1 import EdisonEx1FxParams
from .fx_54_sound_maxer import SoundMaxerFxParams
from .fx_55_dual_guitar_amp import DualGuitarAmpFxParams
from .fx_56_stereo_guitar_amp import StereoGuitarAmpFxParams
from .fx_57_dual_tube_stage import DualTubeStageFxParams
from .fx_58_stereo_tube_stage import StereoTubeStageFxParams
from .fx_59_dual_pitch_shifter import DualPitchShifterFxParams
from .fx_60_stereo_pitch_shifter import StereoPitchShifterFxParams

FxParamsNode: TypeAlias = (
    HallReverbFxParams |
    AmbienceFxParams |
    RichPlateReverbFxParams |
    RoomReverbFxParams |
    ChamberReverbFxParams |
    PlateReverbFxParams |
    VintageReverbFxParams |
    VintageRoomFxParams |
    GatedReverbFxParams |
    ReverseReverbFxParams |
    StereoDelayFxParams |
    Fx3TapDelayFxParams |
    RhythmDelayFxParams |
    StereoChorusFxParams |
    StereoFlangerFxParams |
    StereoPhaserFxParams |
    DimensionalChorusFxParams |
    MoodFilterFxParams |
    RotarySpeakerFxParams |
    TremoloPannerFxParams |
    SuboctaverFxParams |
    DelayChamberFxParams |
    ChorusChamberFxParams |
    FlangerChamberFxParams |
    DelayChorusFxParams |
    DelayFlangerFxParams |
    ModulationDelayFxParams |
    DualGraphicEqFxParams |
    StereoGraphicEqFxParams |
    DualTrueqFxParams |
    StereoTrueqFxParams |
    DualDeesserFxParams |
    StereoDeesserFxParams |
    StereoXtecEq1FxParams |
    DualXtecEq1FxParams |
    StereoXtecEq5FxParams |
    DualXtecEq5FxParams |
    WaveDesignerFxParams |
    PrecisionLimiterFxParams |
    StereoCombinatorFxParams |
    DualCombinatorFxParams |
    StereoFairCompressorFxParams |
    MSFairCompressorFxParams |
    DualFairCompressorFxParams |
    StereoLeisureCompressorFxParams |
    DualLeisureCompressorFxParams |
    StereoUltimoCompressorFxParams |
    DualUltimoCompressorFxParams |
    DualEnhancerFxParams |
    StereoEnhancerFxParams |
    DualExciterFxParams |
    StereoExciterFxParams |
    StereoImagerFxParams |
    EdisonEx1FxParams |
    SoundMaxerFxParams |
    DualGuitarAmpFxParams |
    StereoGuitarAmpFxParams |
    DualTubeStageFxParams |
    StereoTubeStageFxParams |
    DualPitchShifterFxParams |
    StereoPitchShifterFxParams
)

class FxType(IntEnum):
    HallReverb = 0
    Ambience = 1
    RichPlateReverb = 2
    RoomReverb = 3
    ChamberReverb = 4
    PlateReverb = 5
    VintageReverb = 6
    VintageRoom = 7
    GatedReverb = 8
    ReverseReverb = 9
    StereoDelay = 10
    Fx3TapDelay = 11
    RhythmDelay = 12
    StereoChorus = 13
    StereoFlanger = 14
    StereoPhaser = 15
    DimensionalChorus = 16
    MoodFilter = 17
    RotarySpeaker = 18
    TremoloPanner = 19
    Suboctaver = 20
    DelayChamber = 21
    ChorusChamber = 22
    FlangerChamber = 23
    DelayChorus = 24
    DelayFlanger = 25
    ModulationDelay = 26
    DualGraphicEq = 27
    StereoGraphicEq = 28
    DualTrueq = 29
    StereoTrueq = 30
    DualDeesser = 31
    StereoDeesser = 32
    StereoXtecEq1 = 33
    DualXtecEq1 = 34
    StereoXtecEq5 = 35
    DualXtecEq5 = 36
    WaveDesigner = 37
    PrecisionLimiter = 38
    StereoCombinator = 39
    DualCombinator = 40
    StereoFairCompressor = 41
    MSFairCompressor = 42
    DualFairCompressor = 43
    StereoLeisureCompressor = 44
    DualLeisureCompressor = 45
    StereoUltimoCompressor = 46
    DualUltimoCompressor = 47
    DualEnhancer = 48
    StereoEnhancer = 49
    DualExciter = 50
    StereoExciter = 51
    StereoImager = 52
    EdisonEx1 = 53
    SoundMaxer = 54
    DualGuitarAmp = 55
    StereoGuitarAmp = 56
    DualTubeStage = 57
    StereoTubeStage = 58
    DualPitchShifter = 59
    StereoPitchShifter = 60

FX_PARAMS_NODE_TYPES_MAP: dict[FxType, type[FxParamsNode]] = {
    FxType.HallReverb: HallReverbFxParams,
    FxType.Ambience: AmbienceFxParams,
    FxType.RichPlateReverb: RichPlateReverbFxParams,
    FxType.RoomReverb: RoomReverbFxParams,
    FxType.ChamberReverb: ChamberReverbFxParams,
    FxType.PlateReverb: PlateReverbFxParams,
    FxType.VintageReverb: VintageReverbFxParams,
    FxType.VintageRoom: VintageRoomFxParams,
    FxType.GatedReverb: GatedReverbFxParams,
    FxType.ReverseReverb: ReverseReverbFxParams,
    FxType.StereoDelay: StereoDelayFxParams,
    FxType.Fx3TapDelay: Fx3TapDelayFxParams,
    FxType.RhythmDelay: RhythmDelayFxParams,
    FxType.StereoChorus: StereoChorusFxParams,
    FxType.StereoFlanger: StereoFlangerFxParams,
    FxType.StereoPhaser: StereoPhaserFxParams,
    FxType.DimensionalChorus: DimensionalChorusFxParams,
    FxType.MoodFilter: MoodFilterFxParams,
    FxType.RotarySpeaker: RotarySpeakerFxParams,
    FxType.TremoloPanner: TremoloPannerFxParams,
    FxType.Suboctaver: SuboctaverFxParams,
    FxType.DelayChamber: DelayChamberFxParams,
    FxType.ChorusChamber: ChorusChamberFxParams,
    FxType.FlangerChamber: FlangerChamberFxParams,
    FxType.DelayChorus: DelayChorusFxParams,
    FxType.DelayFlanger: DelayFlangerFxParams,
    FxType.ModulationDelay: ModulationDelayFxParams,
    FxType.DualGraphicEq: DualGraphicEqFxParams,
    FxType.StereoGraphicEq: StereoGraphicEqFxParams,
    FxType.DualTrueq: DualTrueqFxParams,
    FxType.StereoTrueq: StereoTrueqFxParams,
    FxType.DualDeesser: DualDeesserFxParams,
    FxType.StereoDeesser: StereoDeesserFxParams,
    FxType.StereoXtecEq1: StereoXtecEq1FxParams,
    FxType.DualXtecEq1: DualXtecEq1FxParams,
    FxType.StereoXtecEq5: StereoXtecEq5FxParams,
    FxType.DualXtecEq5: DualXtecEq5FxParams,
    FxType.WaveDesigner: WaveDesignerFxParams,
    FxType.PrecisionLimiter: PrecisionLimiterFxParams,
    FxType.StereoCombinator: StereoCombinatorFxParams,
    FxType.DualCombinator: DualCombinatorFxParams,
    FxType.StereoFairCompressor: StereoFairCompressorFxParams,
    FxType.MSFairCompressor: MSFairCompressorFxParams,
    FxType.DualFairCompressor: DualFairCompressorFxParams,
    FxType.StereoLeisureCompressor: StereoLeisureCompressorFxParams,
    FxType.DualLeisureCompressor: DualLeisureCompressorFxParams,
    FxType.StereoUltimoCompressor: StereoUltimoCompressorFxParams,
    FxType.DualUltimoCompressor: DualUltimoCompressorFxParams,
    FxType.DualEnhancer: DualEnhancerFxParams,
    FxType.StereoEnhancer: StereoEnhancerFxParams,
    FxType.DualExciter: DualExciterFxParams,
    FxType.StereoExciter: StereoExciterFxParams,
    FxType.StereoImager: StereoImagerFxParams,
    FxType.EdisonEx1: EdisonEx1FxParams,
    FxType.SoundMaxer: SoundMaxerFxParams,
    FxType.DualGuitarAmp: DualGuitarAmpFxParams,
    FxType.StereoGuitarAmp: StereoGuitarAmpFxParams,
    FxType.DualTubeStage: DualTubeStageFxParams,
    FxType.StereoTubeStage: StereoTubeStageFxParams,
    FxType.DualPitchShifter: DualPitchShifterFxParams,
    FxType.StereoPitchShifter: StereoPitchShifterFxParams,
}
