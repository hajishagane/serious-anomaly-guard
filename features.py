from datetime import timedelta

FEATURE_NAMES = [
    "amount_kes",
    "time_since_last_tx",
    "tx_count_1h",
    "tx_count_24h",
    "hour_of_day",
    "is_weekend",
    "orig_balance_zeroed",
    "amount_over_old_balance",
    "balance_change_orig",
    "dest_balance_after",
]

# The 10 features the trained model expects, in order.
MODEL_FEATURE_NAMES = FEATURE_NAMES


def compute_velocity_features(session, origin_account_id, timestamp, TransactionModel):
    """
    Query the transaction log for the given sender account in the past 24 hours prior to timestamp.
    Returns: (time_since_last_tx_in_minutes, tx_count_15min, tx_count_24h)
    For cold starts (no prior transactions in 24h window), returns (0.0, 0, 0).
    """
    cutoff_24h = timestamp - timedelta(hours=24)
    cutoff_15min = timestamp - timedelta(minutes=15)

    recent_txs = (
        session.query(TransactionModel)
        .filter(
            TransactionModel.origin_account_id == origin_account_id,
            TransactionModel.timestamp >= cutoff_24h,
            TransactionModel.timestamp < timestamp,
        )
        .all()
    )

    if not recent_txs:
        return (0.0, 0, 0)

    last_tx_time = max(tx.timestamp for tx in recent_txs)
    time_since_last_tx = (timestamp - last_tx_time).total_seconds() / 60.0

    tx_count_15min = sum(1 for tx in recent_txs if tx.timestamp >= cutoff_15min)
    tx_count_24h = len(recent_txs)

    return (float(time_since_last_tx), tx_count_15min, tx_count_24h)


def compute_syndicate_fan_in(session, vendor_hash, origin_account_id, timestamp, TransactionModel):
    """
    Detect coordinated money-mule / syndicate fan-in: multiple distinct sender accounts
    routing funds into the same recipient/vendor wallet within a 15-minute window.
    Returns: (distinct_other_senders_15min, total_prior_inflow_kes_15min)
    """
    if not vendor_hash:
        return (0, 0.0)

    cutoff_15min = timestamp - timedelta(minutes=15)
    recent_inflows = (
        session.query(TransactionModel)
        .filter(
            TransactionModel.vendor_hash == vendor_hash,
            TransactionModel.timestamp >= cutoff_15min,
            TransactionModel.timestamp < timestamp,
        )
        .all()
    )

    if not recent_inflows:
        return (0, 0.0)

    distinct_other_senders = {
        tx.origin_account_id
        for tx in recent_inflows
        if tx.origin_account_id != origin_account_id
    }
    total_inflow = sum(float(tx.amount_kes or 0.0) for tx in recent_inflows)
    return (len(distinct_other_senders), round(total_inflow, 2))
