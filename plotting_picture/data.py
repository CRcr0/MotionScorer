"""Verified summary statistics used by the MotionScorer experiment figures.

The repository currently contains summary-level results rather than per-example
predictions.  The figures therefore visualize only quantities directly reported
in the experimental tables; no synthetic score histograms, seed clouds, or
confidence intervals are generated.
"""

from __future__ import annotations


NATIVE_METHODS = [
    "Direct\nscalar",
    "Analyze\nthen score",
    "Prompt\nensemble",
    "Self-\nconsistency",
    "Plain\nreadout",
    "nuGuidance",
]

NATIVE_PAIR_ACC = [54.2, 57.6, 56.9, 57.1, 66.8, 70.3]
NATIVE_NDCG = [0.81, 0.83, 0.83, 0.83, 0.89, 0.91]
NATIVE_N_EFF = [6.2, 11.4, 23.7, 18.9, 287.0, 341.0]
NATIVE_SENSITIVITY = [1.94, 1.41, 0.62, 0.88, 0.11, 0.09]
NATIVE_VALID_RATE = [93.5, 96.8, 99.2, 99.0, 100.0, 100.0]


SEMANTIC_METHODS = [
    "EPDMS",
    "Scheme-B\nteacher",
    "Direct\nprompting",
    "Plain\nreadout",
    "LoRA\nscorer",
    "nuGuidance",
]

SEMANTIC_REGIMES = [
    "Teacher–human\nagreement",
    "Rule\nover-penalty",
    "Rule-pass\nblind spot",
]

SEMANTIC_MAE = {
    "EPDMS": [1.72, 4.31, 3.88],
    "Scheme-B teacher": [1.58, 3.42, 3.95],
    "Direct prompting": [2.60, 3.05, 3.30],
    "Plain readout": [1.66, 2.88, 3.41],
    "LoRA scorer": [1.49, 2.51, 3.02],
    "nuGuidance": [1.61, 2.42, 2.79],
}

SEMANTIC_PROFILE_X = [
    "Overall",
    "Agreement",
    "Over-\npenalty",
    "Blind\nspot",
]

SEMANTIC_PROFILE = {
    "EPDMS": [2.95, 1.72, 4.31, 3.88],
    "Scheme-B teacher": [2.78, 1.58, 3.42, 3.95],
    "Plain readout": [2.31, 1.66, 2.88, 3.41],
    "LoRA scorer": [2.02, 1.49, 2.51, 3.02],
    "nuGuidance": [2.10, 1.61, 2.42, 2.79],
}

TRANSCEND_METHODS = ["Direct", "Plain", "LoRA", "nuGuidance"]
TRANSCEND_RATE = [49.8, 52.4, 56.1, 60.7]

WORST_GROUP_METHODS = [
    "EPDMS",
    "Teacher",
    "Direct",
    "Plain",
    "LoRA",
    "nuGuidance",
]
WORST_GROUP_MAE = [4.31, 3.95, 3.30, 3.41, 3.02, 2.79]


INTERVENTIONS = [
    "Uniform\nattention",
    "Top-attended\nmass",
    "Equal-mass\nrandom",
    "Within-modality\nshuffle",
]

DELTA_PAIR_ACC = [-9.4, -8.5, -1.4, -5.2]
DELTA_RHO_TCD = [-7.5, -6.1, -0.8, -3.9]
ABS_PAIR_ACC = [60.9, 61.8, 68.9, 65.1]
ABS_RHO_TCD = [1.2, 2.6, 7.9, 4.8]
