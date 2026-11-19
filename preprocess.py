import os
import pandas as pd
import numpy as np

def compute_velocity_features(df):
    df = df.copy()
    df["hour_of_day"] = df["step"] % 24
    df["day_of_week"] = (df["step"] // 24) % 7
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df = df.sort_values(["origin_account_id", "step"]).reset_index(drop=True)
    df["time_since_last_tx"] = df.groupby("origin_account_id")["step"].diff().fillna(0.0) * 60.0
    df["tx_count_1h"] = df.groupby("origin_account_id")["step"].transform(lambda x: x.rolling(window=6, min_periods=1).count() - 1).fillna(0).astype(int)
    df["tx_count_24h"] = df.groupby("origin_account_id")["step"].transform(lambda x: x.rolling(window=144, min_periods=1).count() - 1).fillna(0).astype(int)
    
    def compute_avg_30d(group):
        amounts = group["amount_kes"].values
        cumulative_avg = np.zeros(len(amounts))
        for i in range(len(amounts)):
            if i == 0:
                cumulative_avg[i] = 0.0
            else:
                cumulative_avg[i] = np.mean(amounts[:i])
        return cumulative_avg
    
    df["amount_vs_avg_30d"] = df.groupby("origin_account_id").apply(compute_avg_30d, include_groups=False).explode().values
    df["amount_vs_avg_30d"] = df["amount_vs_avg_30d"].fillna(0.0)
    dest_counts = df.groupby("vendor_hash")["step"].transform("min")
    df["dest_is_new"] = (df["step"] == dest_counts).astype(int)
    
    if "oldbalanceOrg" in df.columns and "newbalanceOrig" in df.columns:
        df["orig_balance_zeroed"] = ((df["oldbalanceOrg"] > 0) & (df["newbalanceOrig"] == 0)).astype(int)
        df["amount_over_old_balance"] = (df["amount_kes"] > df["oldbalanceOrg"]).astype(int)
        df["balance_change_orig"] = df["oldbalanceOrg"] - df["newbalanceOrig"]
        df["dest_balance_after"] = df.get("newbalanceDest", 0.0)
    else:
        df["orig_balance_zeroed"] = 0
        df["amount_over_old_balance"] = 0
        df["balance_change_orig"] = 0.0
        df["dest_balance_after"] = 0.0
    
    df = df.fillna(0.0)
    return df

def sample_keep_all_fraud(frame, fraud_ratio=0.09, seed=42, label="split"):
    fraud = frame[frame["isFraud"] == 1]
    legit = frame[frame["isFraud"] == 0]
    n_fraud = len(fraud)
    if n_fraud == 0:
        print(f"{label}: no fraud — returning random sample")
        return frame.sample(frac=1, random_state=seed).reset_index(drop=True)
    n_legit_target = int(n_fraud * (1 - fraud_ratio) / fraud_ratio)
    if len(legit) > n_legit_target:
        legit = legit.sample(n=n_legit_target, random_state=seed)
    out = pd.concat([fraud, legit], ignore_index=True)
    out = out.sample(frac=1, random_state=seed).reset_index(drop=True)
    print(f"{label}: {n_fraud:,} fraud + {len(out)-n_fraud:,} legit = {len(out):,} rows ({100*n_fraud/len(out):.2f}% fraud)")
    return out

def preprocess_paysim(input_path="paysim.csv", train_output="processed_train.csv", sim_output="processed_sim.csv", test_output="processed_test.csv", fraud_ratio=0.09):
    if not os.path.exists(input_path):
        print(f"ERROR: {input_path} not found")
        return False
    
    print(f"Loading {input_path}...")
    usecols = ["step", "type", "amount", "nameOrig", "nameDest", "isFraud", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]
    df = pd.read_csv(input_path, usecols=usecols)
    df = df[df["type"].isin(["TRANSFER", "CASH_OUT", "PAYMENT"])].copy()
    df = df.rename(columns={"amount": "amount_kes", "nameOrig": "origin_account_id", "nameDest": "vendor_hash"})
    
    train_raw = df[df["step"] <= 500].copy()
    sim_raw = df[(df["step"] > 500) & (df["step"] <= 600)].copy()
    test_raw = df[df["step"] > 600].copy()

    print(f"\nRaw splits:")
    print(f"  Train (steps 1-500):    {len(train_raw):,} rows, {int(train_raw.isFraud.sum()):,} fraud")
    print(f"  Sim   (steps 501-600):  {len(sim_raw):,} rows, {int(sim_raw.isFraud.sum()):,} fraud")
    print(f"  Test  (steps 601-744):  {len(test_raw):,} rows, {int(test_raw.isFraud.sum()):,} fraud")

    print(f"\nSampling with target fraud_ratio={fraud_ratio:.2%}")
    train_sample = sample_keep_all_fraud(train_raw, fraud_ratio, label="train")
    sim_sample = sample_keep_all_fraud(sim_raw, fraud_ratio, label="sim")
    test_sample = sample_keep_all_fraud(test_raw, fraud_ratio, label="test")

    print("\nComputing velocity features...")
    train_sample = compute_velocity_features(train_sample)
    sim_sample = compute_velocity_features(sim_sample)
    test_sample = compute_velocity_features(test_sample)

    train_sample.to_csv(train_output, index=False)
    sim_sample.to_csv(sim_output, index=False)
    test_sample.to_csv(test_output, index=False)

    print(f"\nWrote {train_output} ({len(train_sample):,} rows)")
    print(f"Wrote {sim_output} ({len(sim_sample):,} rows)")
    print(f"Wrote {test_output} ({len(test_sample):,} rows)")

if __name__ == "__main__":
    preprocess_paysim()
