"""Measured summary statistics used by the MotionScorer experiment figures.

No synthetic per-example distributions or confidence intervals are created in
this repository.  Figures 4--6 visualize only values present in the verified
experiment tables.  Exact numerical tables remain in
``appendix_numeric_tables.tex``.
"""

from __future__ import annotations


NATIVE_CHANNEL = [
    {
        "name": "Direct scalar",
        "display": "Direct scalar",
        "pair_acc": 54.2,
        "ndcg": 0.81,
        "n_eff": 6.2,
        "sensitivity": 1.94,
        "valid": 93.5,
    },
    {
        "name": "Analyze-then-score",
        "display": "Analyze $\\rightarrow$ score",
        "pair_acc": 57.6,
        "ndcg": 0.83,
        "n_eff": 11.4,
        "sensitivity": 1.41,
        "valid": 96.8,
    },
    {
        "name": "Prompt ensemble",
        "display": "Prompt ensemble",
        "pair_acc": 56.9,
        "ndcg": 0.83,
        "n_eff": 23.7,
        "sensitivity": 0.62,
        "valid": 99.2,
    },
    {
        "name": "Self-consistency",
        "display": "Self-consistency",
        "pair_acc": 57.1,
        "ndcg": 0.83,
        "n_eff": 18.9,
        "sensitivity": 0.88,
        "valid": 99.0,
    },
    {
        "name": "Plain readout",
        "display": "Plain readout",
        "pair_acc": 66.8,
        "ndcg": 0.89,
        "n_eff": 287.0,
        "sensitivity": 0.11,
        "valid": 100.0,
    },
    {
        "name": "nuGuidance",
        "display": "nuGuidance",
        "pair_acc": 70.3,
        "ndcg": 0.91,
        "n_eff": 341.0,
        "sensitivity": 0.09,
        "valid": 100.0,
    },
]


SEMANTIC_REGIMES = [
    {
        "name": "Aggregated EPDMS",
        "overall": 2.95,
        "agreement": 1.72,
        "over_penalty": 4.31,
        "blind_spot": 3.88,
        "transcend": None,
        "worst": 4.31,
    },
    {
        "name": "Scheme-B teacher",
        "overall": 2.78,
        "agreement": 1.58,
        "over_penalty": 3.42,
        "blind_spot": 3.95,
        "transcend": None,
        "worst": 3.95,
    },
    {
        "name": "Direct scalar",
        "overall": 2.92,
        "agreement": 2.60,
        "over_penalty": 3.05,
        "blind_spot": 3.30,
        "transcend": 49.8,
        "worst": 3.30,
    },
    {
        "name": "Plain readout",
        "overall": 2.31,
        "agreement": 1.66,
        "over_penalty": 2.88,
        "blind_spot": 3.41,
        "transcend": 52.4,
        "worst": 3.41,
    },
    {
        "name": "LoRA scorer",
        "overall": 2.02,
        "agreement": 1.49,
        "over_penalty": 2.51,
        "blind_spot": 3.02,
        "transcend": 56.1,
        "worst": 3.02,
    },
    {
        "name": "nuGuidance",
        "overall": 2.10,
        "agreement": 1.61,
        "over_penalty": 2.42,
        "blind_spot": 2.79,
        "transcend": 60.7,
        "worst": 2.79,
    },
]


INTERVENTIONS = [
    {
        "name": "Uniform attention",
        "pair_acc": 60.9,
        "delta_acc": -9.4,
        "rho": 1.2,
        "delta_rho": -7.5,
        "ndcg": 0.85,
        "rmse": 0.151,
    },
    {
        "name": "Suppress top-attended mass",
        "pair_acc": 61.8,
        "delta_acc": -8.5,
        "rho": 2.6,
        "delta_rho": -6.1,
        "ndcg": 0.86,
        "rmse": 0.139,
    },
    {
        "name": "Suppress equal mass at random",
        "pair_acc": 68.9,
        "delta_acc": -1.4,
        "rho": 7.9,
        "delta_rho": -0.8,
        "ndcg": 0.90,
        "rmse": 0.101,
    },
    {
        "name": "Shuffle within modality",
        "pair_acc": 65.1,
        "delta_acc": -5.2,
        "rho": 4.8,
        "delta_rho": -3.9,
        "ndcg": 0.88,
        "rmse": 0.118,
    },
]

UNCHANGED_PAIR_ACC = 70.3
UNCHANGED_RHO = 8.7
