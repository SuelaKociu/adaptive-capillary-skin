# ACS V1 system architecture

## Functional stack

1. **Capture surface** — intended to intercept fog, dew or deposited water.
2. **Hygromorphic gates** — passive humidity-responsive apertures; modeled only phenomenologically in v0.1.
3. **Redundant capillary network** — distributes the working fluid without an active pump in the core hypothesis.
4. **Electrokinetic sensing nodes** — proposed to encode local pressure/flow state; the present voltage model is an idealized surrogate.
5. **Swelling isolation collars** — water-responsive elements placed around vulnerable branches.
6. **Bypass manifold / redundant paths** — preserves useful transport after a branch is locally restricted.

## Core causal chain

```text
damage
  ↓
new hydraulic leak path
  ↓
local pressure / flow redistribution
  ↓
increased local wetting of isolation element
  ↓
swelling and falling leak conductance
  ↓
local branch restriction
  ↓
flow reroutes through redundant paths
```

The architecture is interesting only if the physical device can realize this chain **without an electronic controller ordering the isolation event**.

## What is not claimed

ACS v0.1 does not establish atmospheric-water yield, useful electric power generation, self-healing of structural material, thermal performance, lifetime, manufacturability or medical sensing. Those remain separate hypotheses.
