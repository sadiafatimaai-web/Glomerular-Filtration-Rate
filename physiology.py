# physiology.py
import numpy as np

# --- Starling forces and core metrics ---
def nfp(Pgc: float, Pbs: float, pi_gc: float, pi_bs: float = 0.0) -> float:
    """Net Filtration Pressure in mmHg."""
    return (Pgc - Pbs) - (pi_gc - pi_bs)

def gfr(Kf: float, nfp_val: float) -> float:
    """GFR in mL/min from Kf (mL/min/mmHg) and NFP (mmHg)."""
    return max(0.0, Kf * max(0.0, nfp_val))

def rpf_from_map(MAP: float, Ra: float, Re: float) -> float:
    """
    Very simple hemodynamic model:
    RPF ∝ MAP / (Ra + Re). Scaled to ~650 mL/min at MAP=100, Ra=1, Re=2.
    """
    scale = 650.0
    baseline = 100.0 / (1.0 + 2.0)
    return max(0.0, scale * (MAP / (Ra + Re)) / baseline)

def rbf_from_rpf(RPF: float, Hct: float) -> float:
    """RBF = RPF / (1 - Hct). Hct in percent."""
    frac = max(0.01, 1.0 - (Hct / 100.0))
    return RPF / frac

def filtration_fraction(GFR: float, RPF: float) -> float:
    return 0.0 if RPF <= 0 else 100.0 * (GFR / RPF)

# --- Autoregulation toy model (flat plateau ~80–180 mmHg) ---
def autoregulated_values(MAP: float):
    """
    Return (GFR_auto, RPF_auto) for display. Uses a smoothed clamp around
    Normal GFR ~120 mL/min, RPF ~650 mL/min between 80-180 mmHg.
    """
    # Piecewise plateau
    if MAP < 80:
        k = MAP / 80.0
        return (120.0 * k, 650.0 * k)
    if MAP > 180:
        k = 1.0 + 0.5 * ((MAP - 180) / 40.0)  # gentle rise out of range
        return (120.0 * k, 650.0 * k)
    return (120.0, 650.0)
