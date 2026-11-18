import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from engine import THRESHOLDS, eb_shrink
import numpy as np

def test_thresholds_are_ordered():
    assert THRESHOLDS["relaxed"]["pressure_matches"] < THRESHOLDS["current"]["pressure_matches"] < THRESHOLDS["strict"]["pressure_matches"]

def test_eb_shrink_reduces_extreme_estimates():
    raw=np.array([10.,-8.,4.,-3.,7.])
    se=np.array([1.,1.,1.,1.,1.])
    shrunk=eb_shrink(raw,se)
    assert np.all(np.abs(shrunk)<=np.abs(raw)+1e-9)
