# Falsification protocol — ACS v0.1

This document defines conditions under which the present ACS mechanism should be rejected or materially revised.

## Primary hypothesis

A water-responsive local restriction can be triggered by the hydraulic consequences of damage and reduce leakage while a redundant network retains useful transport.

## Computational gate

A virtual trial passes only if all four conditions hold:

1. late leak reduction ≥ 80%;
2. time to 80% leak reduction ≤ 600 s after puncture;
3. useful outlet-flow retention ≥ 70%;
4. idealized electrical-state effect ≥ 5 assumed readout-noise standard deviations.

These thresholds were chosen as engineering decision gates, not discovered natural constants.

## Physical rejection conditions

The mechanism should be rejected or redesigned if matched experiments show one or more of the following reproducibly:

- leakage falls similarly in hydrogel-free controls;
- apparent isolation is explained by reservoir depletion or passive drainage;
- collars swell but do not meaningfully reduce hydraulic conductance;
- useful flow falls below the preregistered retention criterion;
- the response is too slow to satisfy the time gate;
- neighboring paths fail to maintain transport after isolation;
- the electrical signal does not distinguish damage from ordinary flow drift under blinded trials;
- repeated wet/dry or puncture cycles cause rapid irreversible loss of function.

## Anti-HARKing rule

If a physical prototype fails a preregistered gate, the gate must not be silently changed after inspecting the data. A revised mechanism or threshold must be released as a new version with the original failure preserved.
