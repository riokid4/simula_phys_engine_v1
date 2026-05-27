Simula Phys Engine v1 is an early‑stage Python prototype for running simple physics simulations and experimenting with control policies.

## Project description
Simula Phys Engine v1 provides a compact environment and runner for prototyping basic rigid‑body dynamics, controllers, and simple curricula. It includes:
- A top‑level runner: simula.py
- Environment and physics code: simula_env/
- Visualization and tooling scripts: generate-graph.py, curriculum_architect.py, search.py
- Example configuration files: several JSON "brain" files that encode controller parameters and scenarios

## What it can be used for
- Prototyping numerical integrators and collision handling
- Comparing simple controllers (PID, heuristics, small learned policies)
- Designing and testing small curricula or scenario packs
- Producing quick visualizations of trajectories and metrics

## Quickstart (no runtime assumptions)
1. Inspect `simula.py` to find the expected JSON config file names.
2. Open one of the JSON brain files to see required parameters and initial states.
3. This repository is a prototype: it currently lacks a pinned dependency file and full examples. Use the JSON files as the primary guide for inputs.

## Files of interest
- simula.py — main runner and simulation loop
- simula_env/ — environment, bodies, integrator, collision logic
- generate-graph.py — plotting utilities for run logs
- .json — brain and curriculum configs

## Next steps for maintainers
- Add a minimal example brain in `brains/` and a short example command
- Add `requirements.txt` or `pyproject.toml` for reproducibility
- Add a LICENSE and a short test for the integrator

## Contact
Open an issue on this repository for questions or to request a runnable example.
