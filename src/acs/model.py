#!/usr/bin/env python3
"""
Adaptive Capillary Skin (ACS) computational model v0.1
Concept: Suela Kociu
Date: 2026-08-19

STATUS
------
This code produces VIRTUAL / COMPUTATIONAL predictions only. It does not
represent physical experimental measurements. The model is intended to make
the ACS concept falsifiable by translating its core claims into explicit
parameters, equations and pass/fail gates.

Main modeled functions
----------------------
1. Redundant capillary-network hydraulics (Hagen-Poiseuille conductances).
2. Damage leak at a central node.
3. Passive hydrogel-collar isolation represented as an exponentially decaying
   leak conductance after a short wetting delay.
4. Idealized electrokinetic/streaming-potential readout based on a
   Smoluchowski-type proportionality. This is a surrogate, not a calibrated
   transducer model.
5. Hygromorphic gating represented by a hysteretic sigmoid.
6. Simple evaporative-cooling and fog-capture bounding calculations.
7. Monte Carlo falsification under broad and refined design parameter ranges.

Core falsification gate
-----------------------
- late leak reduction >= 80%
- time to 80% leak reduction <= 600 s after damage
- useful outlet flow retained >= 70%
- idealized sensing effect >= 5 assumed readout-noise standard deviations

No physical claim should be made from these outputs until a prototype is
built and tested using the preregistered protocol supplied with the project.
"""

from pathlib import Path
from collections import defaultdict
import json
import numpy as np
import pandas as pd

WATER_MU = 1.0e-3
WATER_EPS = 7.08e-10


def build_grid(nx=5, ny=5, r_mean=90e-6, r_sd=8e-6, L=0.02,
               mu=WATER_MU, rng=None):
    rng = np.random.default_rng(0) if rng is None else rng
    nodes = [(i, j) for i in range(nx) for j in range(ny)]
    edges = []
    for i in range(nx):
        for j in range(ny):
            if i < nx - 1:
                r = max(30e-6, rng.normal(r_mean, r_sd))
                G = np.pi * r**4 / (8 * mu * L)
                edges.append(((i, j), (i + 1, j), G, r, L))
            if j < ny - 1:
                r = max(30e-6, rng.normal(r_mean, r_sd))
                G = np.pi * r**4 / (8 * mu * L)
                edges.append(((i, j), (i, j + 1), G, r, L))
    return nodes, edges


def solve_network(nodes, edges, fixed_pressure, leaks=None):
    leaks = {} if leaks is None else leaks
    unknown = [n for n in nodes if n not in fixed_pressure]
    index = {n: k for k, n in enumerate(unknown)}
    A = np.zeros((len(unknown), len(unknown)))
    b = np.zeros(len(unknown))
    adjacency = defaultdict(list)
    for a, c, G, r, L in edges:
        adjacency[a].append((c, G)); adjacency[c].append((a, G))
    for n in unknown:
        k = index[n]; total = 0.0
        for m, G in adjacency[n]:
            total += G
            if m in fixed_pressure: b[k] += G * fixed_pressure[m]
            else: A[k, index[m]] -= G
        total += leaks.get(n, 0.0); A[k, k] += total
    pressure = dict(fixed_pressure)
    if unknown:
        solution = np.linalg.solve(A, b)
        pressure.update({n: solution[index[n]] for n in unknown})
    return pressure


def calculate_state(nodes, edges, source_pressure=1000.0, leak_G=0.0,
                    zeta=-0.03, conductivity=0.01,
                    noise_sd_V=0.0, rng=None):
    nx = ny = 5; damage_node = (2, 2)
    fixed = {(0, j): source_pressure for j in range(ny)}
    fixed.update({(nx - 1, j): 0.0 for j in range(ny)})
    pressure = solve_network(nodes, edges, fixed, {damage_node: leak_G} if leak_G > 0 else {})
    Qin = Qout = 0.0
    for a, b, G, r, L in edges:
        q = G * (pressure[a] - pressure[b])
        if a[0] == 0 and b[0] == 1: Qin += q
        elif b[0] == 0 and a[0] == 1: Qin -= q
        if b[0] == nx - 1 and a[0] == nx - 2: Qout += q
        elif a[0] == nx - 1 and b[0] == nx - 2: Qout -= q
    Qleak = leak_G * pressure[damage_node]
    Csp = WATER_EPS * zeta / (WATER_MU * conductivity)
    deltaP_sensor = pressure[(2, 2)] - pressure[(3, 2)]
    noise = 0.0 if rng is None else rng.normal(0.0, noise_sd_V)
    voltage = Csp * deltaP_sensor + noise
    return Qin, Qout, Qleak, pressure[damage_node], voltage, deltaP_sensor


def leak_conductance(t_s, tau_s, G0, Gmin, damage_time_s=300.0, wetting_delay_s=5.0):
    if t_s < damage_time_s: return 0.0
    u = max(0.0, t_s - damage_time_s - wetting_delay_s)
    if u <= 0: return G0
    return Gmin + (G0 - Gmin) * np.exp(-u / tau_s)


def nominal_timeseries(seed=1, t_end_s=900, dt_s=1,
                       tau_s=90, G0=8e-12, Gmin=1.6e-13,
                       r_mean=90e-6, source_pressure=1000,
                       zeta=-0.03, conductivity=0.01,
                       assumed_sensor_noise_V=2e-6):
    rng = np.random.default_rng(seed); nodes, edges = build_grid(r_mean=r_mean, rng=rng); rows = []
    for t in range(0, t_end_s + 1, dt_s):
        G = leak_conductance(t, tau_s, G0, Gmin)
        state = calculate_state(nodes, edges, source_pressure, G, zeta, conductivity, assumed_sensor_noise_V, rng)
        swelling = 0.0 if t < 305 else 1 - np.exp(-(t - 305) / tau_s)
        rows.append([t, *state, G, swelling])
    columns = ["time_s","Qin_m3_s","Qout_m3_s","Qleak_m3_s","P_damage_Pa","sensor_voltage_V","sensor_deltaP_Pa","leak_conductance_m3_Pa_s","hydrogel_swelling_fraction"]
    return pd.DataFrame(rows, columns=columns)


def fast_metrics(seed, tau_s, G0, final_ratio, r_mean, source_pressure, zeta, conductivity, assumed_noise_V=2e-6):
    rng = np.random.default_rng(seed); nodes, edges = build_grid(r_mean=r_mean, rng=rng)
    base = calculate_state(nodes, edges, source_pressure, 0.0, zeta, conductivity)
    peak = calculate_state(nodes, edges, source_pressure, G0, zeta, conductivity)
    Gpost = leak_conductance(900, tau_s, G0, G0 * final_ratio)
    post = calculate_state(nodes, edges, source_pressure, Gpost, zeta, conductivity)
    target = 0.2 * peak[2]; isolation = np.nan
    if post[2] <= target:
        lo, hi = 305.0, 900.0
        for _ in range(18):
            mid = 0.5 * (lo + hi)
            G = leak_conductance(mid, tau_s, G0, G0 * final_ratio)
            q = calculate_state(nodes, edges, source_pressure, G, zeta, conductivity)[2]
            if q <= target: hi = mid
            else: lo = mid
        isolation = hi - 300.0
    leak_reduction = (1 - post[2] / peak[2]) * 100
    retention = post[1] / base[1] * 100
    sensor_effect_sigma = abs(peak[4] - base[4]) / assumed_noise_V
    return leak_reduction, retention, isolation, sensor_effect_sigma, base, peak, post


def monte_carlo(n=1000, optimized=False):
    rows = []
    for seed in range(n):
        rng = np.random.default_rng(seed + (100000 if optimized else 0))
        if optimized:
            tau=float(np.clip(rng.lognormal(np.log(90),0.2),45,160)); ratio=float(np.clip(rng.normal(0.02,0.008),0.003,0.05)); G0=float(rng.lognormal(np.log(8e-12),0.25)); radius=float(np.clip(rng.normal(90e-6,6e-6),75e-6,105e-6)); pressure=float(np.clip(rng.normal(1000,80),800,1200)); zeta=float(rng.normal(-0.03,0.003)); cond=float(np.clip(rng.normal(0.01,0.001),0.007,0.014))
        else:
            tau=float(rng.lognormal(np.log(120),0.35)); ratio=float(np.clip(rng.beta(2,18),0.002,0.25)); G0=float(rng.lognormal(np.log(8e-12),0.35)); radius=float(np.clip(rng.normal(90e-6,8e-6),65e-6,115e-6)); pressure=float(np.clip(rng.normal(1000,120),700,1300)); zeta=float(rng.normal(-0.03,0.004)); cond=float(np.clip(rng.normal(0.01,0.0015),0.005,0.02))
        lr, ret, iso, se, base, peak, post = fast_metrics(seed + (100000 if optimized else 0), tau, G0, ratio, radius, pressure, zeta, cond)
        pass_isolation = lr >= 80 and np.isfinite(iso) and iso <= 600; pass_retention = ret >= 70; pass_sensor = se >= 5
        rows.append({"seed":seed,"optimized_design_envelope":optimized,"hydrogel_tau_s":tau,"final_leak_conductance_ratio":ratio,"initial_leak_conductance":G0,"mean_channel_radius_um":radius*1e6,"source_pressure_Pa":pressure,"zeta_potential_mV":zeta*1e3,"conductivity_S_m":cond,"baseline_out_uL_s":base[1]*1e9,"peak_leak_uL_s":peak[2]*1e9,"post_leak_uL_s":post[2]*1e9,"leak_reduction_pct":lr,"flow_retention_pct":ret,"isolation_time_s":iso,"expected_sensor_effect_sigma":se,"pass_isolation":pass_isolation,"pass_retention":pass_retention,"pass_sensor":pass_sensor,"pass_all":pass_isolation and pass_retention and pass_sensor})
    return pd.DataFrame(rows)


def wetbulb_stull(T_C, RH_pct):
    RH = RH_pct
    return (T_C*np.arctan(0.151977*np.sqrt(RH+8.313659))+np.arctan(T_C+RH)-np.arctan(RH-1.676331)+0.00391838*RH**1.5*np.arctan(0.023101*RH)-4.686035)
