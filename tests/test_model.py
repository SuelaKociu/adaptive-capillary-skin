import numpy as np
from acs.model import build_grid, fast_metrics, wetbulb_stull, monte_carlo


def test_grid_topology():
    nodes, edges = build_grid(nx=5, ny=5, rng=np.random.default_rng(1))
    assert len(nodes) == 25
    assert len(edges) == 40


def test_nominal_design_meets_declared_virtual_gate():
    lr, ret, iso, se, *_ = fast_metrics(
        seed=1,
        tau_s=90,
        G0=8e-12,
        final_ratio=0.02,
        r_mean=90e-6,
        source_pressure=1000,
        zeta=-0.03,
        conductivity=0.01,
    )
    assert lr >= 80
    assert ret >= 70
    assert np.isfinite(iso) and iso <= 600
    assert se >= 5


def test_wetbulb_is_bounded():
    tw = wetbulb_stull(30.0, 50.0)
    assert 0 < tw < 30.0


def test_small_monte_carlo_has_expected_schema():
    df = monte_carlo(n=4, optimized=False)
    assert len(df) == 4
    assert {"pass_all", "leak_reduction_pct", "flow_retention_pct"}.issubset(df.columns)
