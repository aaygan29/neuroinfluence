"""Independent verification of stage 20's monitor/attacker geometry.

Re-derives, in numpy (independent of the torch code under test), the invariants the defense stage
relies on, on synthetic activations shaped like the real ones. If these fail, the defense claim is
built on a geometry bug, not a finding. Run: python3 -m pytest tests/test_stage20_geometry.py -q
"""

import numpy as np


def build(seed, d=2560, k=10):
    """Mirror stage20's construction on synthetic per-item principal/control activations."""
    rng = np.random.default_rng(seed)
    rp = rng.standard_normal((k, d))
    rc = rng.standard_normal((k, d))
    # single monitor: mean diff-of-means, unit
    d_mon = rp.mean(0) - rc.mean(0)
    d_mon /= np.linalg.norm(d_mon) + 1e-8
    # subspace monitor: orthonormal basis of the k per-item contrasts (reduced QR on transpose)
    contrasts = rp - rc  # (k, d)
    Q, _ = np.linalg.qr(contrasts.T)  # (d, k)
    B = Q.T  # (k, d), orthonormal rows
    # a causal direction and the two adaptive covert variants
    d_j = rng.standard_normal(d)
    d_j /= np.linalg.norm(d_j) + 1e-8
    d_cs = d_j - (d_j @ d_mon) * d_mon
    d_cs /= np.linalg.norm(d_cs) + 1e-8
    d_cu = d_j - B.T @ (B @ d_j)
    d_cu /= np.linalg.norm(d_cu) + 1e-8
    return dict(d_mon=d_mon, B=B, d_j=d_j, d_cs=d_cs, d_cu=d_cu, k=k)


def test_subspace_basis_orthonormal():
    g = build(0)
    assert np.allclose(g["B"] @ g["B"].T, np.eye(g["k"]), atol=1e-6)


def test_covert_single_evades_single_monitor():
    for s in range(5):
        g = build(s)
        assert abs(g["d_cs"] @ g["d_mon"]) < 1e-6  # no component on the probe direction


def test_covert_subspace_evades_subspace_monitor():
    for s in range(5):
        g = build(s)
        assert np.linalg.norm(g["B"] @ g["d_cu"]) < 1e-6  # no component in the whole subspace


def test_single_probe_lies_inside_the_subspace():
    # d_mon is (close to) a member of the contrast span, so the subspace monitor reads at least
    # what the single monitor reads: the defenses are nested, subspace is strictly >= single.
    for s in range(5):
        g = build(s)
        assert np.linalg.norm(g["B"] @ g["d_mon"]) > 0.999


def test_covert_single_is_still_visible_to_the_subspace_monitor():
    # The attacker that beats the single probe still has mass in the subspace, so a multi-probe
    # monitor can catch what the single probe misses. This is the whole point of the defense.
    seen = []
    for s in range(20):
        g = build(s)
        seen.append(np.linalg.norm(g["B"] @ g["d_cs"]))
    seen = np.array(seen)
    # not a fluke of one seed: the single-probe evasion is subspace-visible on average
    assert seen.mean() > 1e-3
    assert (seen > 1e-6).mean() > 0.8


def test_evading_the_subspace_costs_more_causal_mass_than_evading_the_probe():
    # Projecting out the whole subspace removes at least as much of the causal direction as
    # projecting out the single probe does, so the covert-subspace attacker is weaker (or equal).
    for s in range(10):
        g = build(s)
        kept_cs = abs(g["d_cs"] @ g["d_j"])   # overlap of single-covert with the causal direction
        kept_cu = abs(g["d_cu"] @ g["d_j"])   # overlap of subspace-covert with the causal direction
        assert kept_cu <= kept_cs + 1e-9


if __name__ == "__main__":
    import sys
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    fails = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            fails += 1
            print(f"FAIL {fn.__name__}: {e}")
    sys.exit(1 if fails else 0)
