from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class HemodynamicsInput:
    MAP: float = 100.0
    Ra: float = 1.0
    Re: float = 1.0
    Pbs: float = 10.0
    pi_gc: float = 25.0
    Kf: float = 12.0
    Hct: float = 45.0

@dataclass
class HemodynamicsOutput:
    Pgc: float
    NFP: float
    GFR: float
    RBF: float
    RPF: float
    FF: float

def compute_hemodynamics(inp: HemodynamicsInput) -> HemodynamicsOutput:
    pgc_raw = 55.0 * (inp.MAP / 100.0) * (1.0 + 0.35*(inp.Re - 1.0) - 0.25*(inp.Ra - 1.0))
    Pgc = float(np.clip(pgc_raw, 35.0, 99.0))
    NFP = Pgc - inp.Pbs - inp.pi_gc
    GFR = max(inp.Kf * NFP, 0.0)
    SCALE_RBF = 2680.0
    denom = (inp.Ra + inp.Re)
    RBF = max(SCALE_RBF * (inp.MAP / 100.0) / denom, 0.0)
    RPF = RBF * (1.0 - inp.Hct / 100.0)
    FF = (GFR / RPF * 100.0) if RPF > 0 else 0.0
    return HemodynamicsOutput(Pgc=Pgc, NFP=NFP, GFR=GFR, RBF=RBF, RPF=RPF, FF=FF)

AUTOREG_MIN = 80.0
AUTOREG_MAX = 180.0
BASELINE_GFR = 120.0
BASELINE_RPF = 650.0

def curve_without_autoreg(map_vals, base_inp: HemodynamicsInput):
    gfr, rpf = [], []
    for m in map_vals:
        out = compute_hemodynamics(HemodynamicsInput(MAP=float(m), Ra=base_inp.Ra, Re=base_inp.Re,
                              Pbs=base_inp.Pbs, pi_gc=base_inp.pi_gc,
                              Kf=base_inp.Kf, Hct=base_inp.Hct))
        gfr.append(out.GFR)
        rpf.append(out.RPF)
    return np.array(gfr), np.array(rpf)

def curve_with_autoreg(map_vals, base_inp: HemodynamicsInput):
    g_wo, r_wo = curve_without_autoreg(map_vals, base_inp)
    g, r = [], []
    for m, g0, r0 in zip(map_vals, g_wo, r_wo):
        if AUTOREG_MIN <= m <= AUTOREG_MAX:
            g.append(BASELINE_GFR + 0.15*(g0 - BASELINE_GFR))
            r.append(BASELINE_RPF + 0.25*(r0 - BASELINE_RPF))
        else:
            dist = min(abs(m - AUTOREG_MIN), abs(m - AUTOREG_MAX))
            w = np.exp(-dist / 25.0)
            edge_map = AUTOREG_MIN if m < AUTOREG_MIN else AUTOREG_MAX
            edge_out = compute_hemodynamics(HemodynamicsInput(MAP=float(edge_map), Ra=base_inp.Ra,
                               Re=base_inp.Re, Pbs=base_inp.Pbs, pi_gc=base_inp.pi_gc,
                               Kf=base_inp.Kf, Hct=base_inp.Hct))
            g_edge, r_edge = edge_out.GFR, edge_out.RPF
            g.append(w * g_edge + (1 - w) * g0)
            r.append(w * r_edge + (1 - w) * r0)
    return np.array(g), np.array(r)

def point_analysis(MAP: float, base_inp: HemodynamicsInput):
    g_wo, r_wo = curve_without_autoreg([MAP], base_inp)
    g_w, r_w   = curve_with_autoreg([MAP], base_inp)
    return float(g_w[0]), float(r_w[0]), float(g_wo[0]), float(r_wo[0])
