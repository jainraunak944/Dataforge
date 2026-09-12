"""Prototype bearing-fault detection/diagnosis model for the NAADI concept deck.

India Chem 2026 Youth Innovation Challenge — Team NIT Warangal (Raunak Jain,
Anushriya Bhattacharya). DRAFT prepared with AI assistance; the team must run,
review and ratify this before any result is presented as team work.

Data: Case Western Reserve University (CWRU) Bearing Data Center seeded-fault
test data, 12 kHz drive-end accelerometer + normal baseline. Public dataset,
obtained via the s-whynot/cwru-dataset GitHub mirror of the official files
(https://engineering.case.edu/bearingdatacenter).

Honesty-by-design choices (deliberate, defensible in jury Q&A):
- Windows from the same recording NEVER cross the train/test boundary
  (a random window split leaks near-identical windows and inflates accuracy).
- Headline evaluation holds out an entire unseen operating condition
  (motor load 3 hp): train on 0/1/2 hp recordings, test on 3 hp recordings.
- Features are classical, physically interpretable condition indicators
  (ISO 13373-style time-domain indicators + octave-band energies), so every
  model input can be explained to a reliability engineer.

Outputs: model/results/metrics.json, confusion_matrix.csv, feature_importances.csv
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import scipy.io
from scipy.signal import welch
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA_ROOT = Path("/home/user/s-whynot/cwru-dataset")
OUT_DIR = Path(__file__).parent / "results"
FS = 12_000  # Hz, drive-end accelerometer sampling rate
WINDOW = 2048  # samples per window (~0.17 s)
SEED = 42

CLASSES = ["Normal", "InnerRace", "Ball", "OuterRace"]


def de_signal(mat_path: Path) -> np.ndarray:
    """Load the drive-end accelerometer channel from a CWRU .mat file."""
    mat = scipy.io.loadmat(mat_path)
    keys = [k for k in mat if k.endswith("_DE_time")]
    if not keys:
        raise ValueError(f"no DE channel in {mat_path}")
    return mat[keys[0]].ravel().astype(float)


def window_features(x: np.ndarray) -> np.ndarray:
    """Classical condition indicators for one vibration window."""
    rms = np.sqrt(np.mean(x**2))
    peak = np.max(np.abs(x))
    std = np.std(x)
    mean_abs = np.mean(np.abs(x))
    # avoid division blowups on pathological windows
    eps = 1e-12
    kurtosis = np.mean((x - x.mean()) ** 4) / (std**4 + eps)
    skew = np.mean((x - x.mean()) ** 3) / (std**3 + eps)
    crest = peak / (rms + eps)
    shape = rms / (mean_abs + eps)
    impulse = peak / (mean_abs + eps)
    p2p = np.ptp(x)
    time_feats = [rms, p2p, std, kurtosis, skew, crest, shape, impulse]

    # Octave-ish band energies from Welch PSD up to Nyquist (6 kHz)
    f, psd = welch(x, fs=FS, nperseg=512)
    edges = [0, 100, 300, 600, 1000, 1800, 2800, 4200, 6000]
    band_feats = []
    total = np.trapezoid(psd, f) + eps
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (f >= lo) & (f < hi)
        band_feats.append(np.trapezoid(psd[m], f[m]) / total)
    return np.array(time_feats + band_feats)


FEATURE_NAMES = [
    "rms", "peak_to_peak", "std", "kurtosis", "skewness", "crest_factor",
    "shape_factor", "impulse_factor",
    "band_0_100Hz", "band_100_300Hz", "band_300_600Hz", "band_600_1000Hz",
    "band_1000_1800Hz", "band_1800_2800Hz", "band_2800_4200Hz", "band_4200_6000Hz",
]


def collect_dataset():
    """Return X, y, load (hp), group (recording id) for all windows."""
    records = []  # (path, class, load)
    for p in sorted((DATA_ROOT / "Normal").glob("*.mat")):
        load = int(p.stem.split("_")[-1])
        records.append((p, "Normal", load))
    fault_map = {"IR": "InnerRace", "B": "Ball", "OR": "OuterRace"}
    for folder, cls in fault_map.items():
        for p in sorted((DATA_ROOT / "12k_Drive_End_Bearing_Fault_Data" / folder).rglob("*.mat")):
            load = int(p.stem.split("_")[-1])
            records.append((p, cls, load))

    X, y, loads, groups = [], [], [], []
    for path, cls, load in records:
        sig = de_signal(path)
        n_windows = len(sig) // WINDOW
        for i in range(n_windows):
            w = sig[i * WINDOW:(i + 1) * WINDOW]
            X.append(window_features(w))
            y.append(cls)
            loads.append(load)
            groups.append(path.stem)
    return (np.array(X), np.array(y), np.array(loads), np.array(groups),
            len(records))


def evaluate(y_true, y_pred, label: str) -> dict:
    out = {
        "evaluation": label,
        "n_test_windows": int(len(y_true)),
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "macro_precision": round(float(precision_score(y_true, y_pred, average="macro")), 4),
        "macro_recall": round(float(recall_score(y_true, y_pred, average="macro")), 4),
        "macro_f1": round(float(f1_score(y_true, y_pred, average="macro")), 4),
    }
    # Binary framing: does the system detect that a fault exists at all?
    bt = np.where(y_true == "Normal", "Normal", "Fault")
    bp = np.where(y_pred == "Normal", "Normal", "Fault")
    out["fault_detection_precision"] = round(float(precision_score(bt, bp, pos_label="Fault")), 4)
    out["fault_detection_recall"] = round(float(recall_score(bt, bp, pos_label="Fault")), 4)
    out["normal_misflagged_as_fault_rate"] = round(
        float(np.mean(bp[bt == "Normal"] == "Fault")), 4)
    return out


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    X, y, loads, groups, n_recordings = collect_dataset()
    print(f"windows={len(X)} recordings={n_recordings} classes={dict(zip(*np.unique(y, return_counts=True)))}")

    rf = RandomForestClassifier(n_estimators=300, random_state=SEED, n_jobs=-1)
    logit = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=2000, random_state=SEED))

    results = {"dataset": {
        "source": "CWRU Bearing Data Center, 12k drive-end + normal baseline",
        "n_recordings": n_recordings,
        "n_windows": int(len(X)),
        "window_samples": WINDOW,
        "sampling_hz": FS,
        "features": FEATURE_NAMES,
    }, "evaluations": []}

    # 1) Headline: unseen operating condition (train 0/1/2 hp, test 3 hp)
    tr, te = loads < 3, loads == 3
    rf.fit(X[tr], y[tr])
    pred = rf.predict(X[te])
    results["evaluations"].append(
        evaluate(y[te], pred, "random_forest__train_0-2hp__test_unseen_3hp"))
    cm = confusion_matrix(y[te], pred, labels=CLASSES)
    np.savetxt(OUT_DIR / "confusion_matrix.csv",
               cm, fmt="%d", delimiter=",",
               header=",".join(CLASSES), comments="")

    logit.fit(X[tr], y[tr])
    results["evaluations"].append(
        evaluate(y[te], logit.predict(X[te]),
                 "logistic_baseline__train_0-2hp__test_unseen_3hp"))

    # 2) Recording-held-out 5-fold CV (no recording crosses the boundary)
    gkf = GroupKFold(n_splits=5)
    pred_cv = cross_val_predict(rf, X, y, groups=groups, cv=gkf, n_jobs=-1)
    results["evaluations"].append(
        evaluate(y, pred_cv, "random_forest__grouped_5fold_by_recording"))

    imp = sorted(zip(FEATURE_NAMES, rf.feature_importances_),
                 key=lambda t: -t[1])
    with open(OUT_DIR / "feature_importances.csv", "w") as f:
        f.write("feature,importance\n")
        for name, v in imp:
            f.write(f"{name},{v:.4f}\n")

    with open(OUT_DIR / "metrics.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results["evaluations"], indent=2))


if __name__ == "__main__":
    main()
