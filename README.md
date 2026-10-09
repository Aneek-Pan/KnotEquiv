# KnotEquiv

An AI system that attacks the Knot Equivalence Problem directly: given two knots, predict whether they're equivalent, and — inspired by AlphaGeometry's (problem, proof) synthetic training approach — generate the actual Reidemeister move sequence connecting equivalent pairs, or construct structurally-close-but-provably-distinct examples for non-equivalent pairs.

## Status

Working end-to-end pipeline: knot representation → Reidemeister moves (R1/R2/R3) → dataset generation (positive/negative pairs) → graph neural network classifier → training loop. Trained on 8 verified prime knots; current test accuracy ~97.6% (see caveats below).

## Setup

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Generate a dataset and train:
```powershell
python run_training.py
```

Run tests:
```powershell
pytest tests/ -v
```

## Project structure

- `knot/` — core knot representation (Gauss codes), seed knot library, invariants, canonical form, planarity validator
- `moves/` — Reidemeister move implementations (R1, R2, R3) and a unified move detector
- `dataset/` — positive/negative pair generation, serialization, dataset orchestration
- `model/` — knot-to-graph conversion, featurization, GNN encoder, siamese classifier
- `training/` — training loop, evaluation, checkpointing
- `visualization/` — chord diagram plotting

## Known simplifications (intentional, revisit if needed)

- Negative-pair closeness metric is crossing-count difference only — produces same-complexity pairs but not necessarily visually similar ones.
- `knot/validator.py` only checks the *necessary* Gauss-parity condition for planarity, not full realizability (Lovász trip-matrix or similar).
- `moves/r2.py`'s `apply_r2_add(i, j)` for arbitrary far-apart gaps is not guaranteed realizable — only `apply_r2_add_local` is safe without face-structure info (`knot/faces.py`, not yet built).
- Model has only been trained/tested within the same 8-seed knot pool (no held-out-seed generalization test yet).

## Corrections log

- Seeds (trefoil, cinquefoil, figure-eight) were originally hand-derived with a non-alternating O/U pattern. Verified against Wikipedia's cited Gauss codes and a SageMath/KnotInfo docstring example; corrected to the proper alternating pattern. Models trained before this fix are stale.
- 5_2, 6_1, 6_2, 6_3 added via SnapPy, cross-validated against independently-cited DT codes where available (all except 6_1, which rests on the SnapPy method alone).

## Credits / tools used

- [SnapPy](https://snappy.computop.org/) — used as a one-time sourcing tool to generate and verify seed knot data (not a runtime dependency).
