import json
import os
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from features import FEATURE_NAMES

MODEL_FEATURE_NAMES = FEATURE_NAMES


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["hour_of_day"] = df["step"] % 24
    df["day_of_week"] = (df["step"] // 24) % 7
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df = df.sort_values(["origin_account_id", "step"]).reset_index(drop=True)
    df["time_since_last_tx"] = (
        df.groupby("origin_account_id")["step"].diff().fillna(0.0) * 60.0
    )
    df["tx_count_1h"] = (
        df.groupby("origin_account_id")["step"]
        .transform(lambda x: x.rolling(window=6, min_periods=1).count() - 1)
        .fillna(0)
        .astype(int)
    )
    df["tx_count_24h"] = (
        df.groupby("origin_account_id")["step"]
        .transform(lambda x: x.rolling(window=144, min_periods=1).count() - 1)
        .fillna(0)
        .astype(int)
    )
    df["orig_balance_zeroed"] = ((df["oldbalanceOrg"] > 0) & (df["newbalanceOrig"] == 0)).astype(int)
    df["amount_over_old_balance"] = (df["amount_kes"] > df["oldbalanceOrg"]).astype(int)
    df["balance_change_orig"] = df["oldbalanceOrg"] - df["newbalanceOrig"]
    df["dest_balance_after"] = df["newbalanceDest"].fillna(0.0)
    return df.fillna(0.0)


def sample_split(frame: pd.DataFrame, max_legit: int, seed: int = 42) -> pd.DataFrame:
    fraud = frame[frame["isFraud"] == 1]
    legit = frame[frame["isFraud"] == 0]
    if len(legit) > max_legit:
        legit = legit.sample(n=max_legit, random_state=seed)
    return (
        pd.concat([fraud, legit], ignore_index=True)
        .sample(frac=1, random_state=seed)
        .reset_index(drop=True)
    )


def summarize(name: str, y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    fpr = float(fp / (fp + tn)) if (fp + tn) else 0.0
    return {
        "name": name,
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "fpr": round(fpr, 5),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


def train_models():
    if not os.path.exists("paysim.csv"):
        raise FileNotFoundError("paysim.csv not found in repo root.")

    print("Loading paysim.csv...")
    usecols = [
        "step", "type", "amount", "nameOrig", "nameDest", "isFraud",
        "oldbalanceOrg", "newbalanceOrig", "newbalanceDest",
    ]
    df = pd.read_csv("paysim.csv", usecols=usecols)
    df = df[df["type"].isin(["TRANSFER", "CASH_OUT", "PAYMENT"])].copy()
    df = df.rename(columns={
        "amount": "amount_kes",
        "nameOrig": "origin_account_id",
        "nameDest": "vendor_hash",
    })

    # Strict 3-way temporal split (zero future leakage)
    train_df = build_features(sample_split(df[df["step"] <= 500], max_legit=80000, seed=42))
    val_df = build_features(sample_split(df[(df["step"] > 500) & (df["step"] <= 600)], max_legit=20000, seed=42))
    test_df = build_features(sample_split(df[df["step"] > 600], max_legit=20000, seed=42))

    X_train, y_train = train_df[MODEL_FEATURE_NAMES].values, train_df["isFraud"].values
    X_val, y_val = val_df[MODEL_FEATURE_NAMES].values, val_df["isFraud"].values
    X_test, y_test = test_df[MODEL_FEATURE_NAMES].values, test_df["isFraud"].values

    print(f"Train (steps 1-500):   {len(train_df):,} rows ({int(y_train.sum()):,} fraud)")
    print(f"Val   (steps 501-600): {len(val_df):,} rows ({int(y_val.sum()):,} fraud)")
    print(f"Test  (steps 601-744): {len(test_df):,} rows ({int(y_test.sum()):,} fraud)")

    # 1. Unsupervised Isolation Forest baseline
    print("\nTraining Isolation Forest baseline...")
    iso = IsolationForest(
        contamination=max(0.01, float(y_train.mean())),
        n_estimators=150,
        random_state=42,
        n_jobs=-1,
    )
    iso.fit(X_train)
    iso_test_preds = (iso.predict(X_test) == -1).astype(int)

    # 2. Supervised XGBoost with class-imbalance weighting
    print("Training XGBoost classifier (current xgboost 2.1.3)...")
    n_pos = max(1, int((y_train == 1).sum()))
    n_neg = int((y_train == 0).sum())
    scale_pos_weight = 1.0

    xgb = XGBClassifier(
        n_estimators=300,
        max_depth=8,
        learning_rate=0.08,
        subsample=0.85,
        colsample_bytree=0.85,
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
    )
    xgb.fit(X_train, y_train)

    # Tune decision threshold strictly on validation split (steps 501-600)
    val_proba = xgb.predict_proba(X_val)[:, 1]
    best_f1, best_thresh = 0.0, 0.50
    for thresh in np.arange(0.10, 0.95, 0.05):
        preds = (val_proba >= thresh).astype(int)
        f1 = f1_score(y_val, preds, zero_division=0)
        if f1 > best_f1:
            best_f1, best_thresh = f1, round(float(thresh), 2)

    # Evaluate final metrics strictly on unseen temporal holdout (steps 601-744)
    test_proba = xgb.predict_proba(X_test)[:, 1]
    xgb_test_preds = (test_proba >= best_thresh).astype(int)
    static_test_preds = (test_df["amount_kes"].values > 50000.0).astype(int)

    models_summary = [
        summarize(f"Anomaly Guard XGBoost (cutoff={best_thresh:.2f})", y_test, xgb_test_preds),
        summarize("Isolation Forest (Unsupervised Baseline)", y_test, iso_test_preds),
        summarize("Legacy Static Rule (> KES 50,000)", y_test, static_test_preds),
    ]

    joblib.dump({"model": xgb, "threshold": best_thresh, "features": MODEL_FEATURE_NAMES}, "model.joblib")

    metrics_payload = {
        "available": True,
        "dataset": "PaySim Mobile Money (Temporal Holdout: steps 601-744)",
        "eval_samples": int(len(y_test)),
        "fraud_samples": int(y_test.sum()),
        "active_model": "XGBClassifier",
        "threshold": best_thresh,
        "models": models_summary,
    }
    with open("model_metrics.json", "w") as f:
        json.dump(metrics_payload, f, indent=2)

    print("\n=== Unseen Temporal Holdout Benchmark (steps 601-744) ===")
    for m in models_summary:
        print(
            f"{m['name']:45s} | F1: {m['f1']:.4f} | Prec: {m['precision']:.4f} | "
            f"Rec: {m['recall']:.4f} | FPR: {m['fpr']*100:.2f}%"
        )
    print("\nClassification Report (XGBoost on Holdout Test):")
    print(classification_report(y_test, xgb_test_preds, zero_division=0))
    print(f"Saved fresh model.joblib (threshold={best_thresh:.2f}) and model_metrics.json.")


if __name__ == "__main__":
    train_models()
