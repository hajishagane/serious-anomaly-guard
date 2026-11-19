import os
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    Integer,
    DateTime,
    Text,
    ForeignKey,
    event,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

DB_PATH = os.getenv("DB_PATH", "data/anomaly_guard.db")
if os.getenv("TESTING") == "true":
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    os.makedirs(os.path.dirname(DB_PATH) if os.path.dirname(DB_PATH) else ".", exist_ok=True)
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=15000")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Transaction(Base):
    """Parsed_Transactions entity (Proposal Figure 3.4)."""
    __tablename__ = "parsed_transactions"
    tx_id = Column(String, primary_key=True)
    origin_account_id = Column(String, index=True)
    vendor_hash = Column(String, index=True)
    tx_type = Column(String, default="PAYMENT")
    amount_kes = Column(Float)
    oldbalance_org = Column(Float, default=0.0)
    newbalance_orig = Column(Float, default=0.0)
    oldbalance_dest = Column(Float, nullable=True)
    newbalance_dest = Column(Float, default=0.0)
    timestamp = Column(DateTime, index=True)
    tx_count_15min = Column(Integer, default=0)
    tx_count_24h = Column(Integer, default=0)
    time_since_last_tx = Column(Float, default=0.0)
    verdict = Column(Integer, default=0)
    score = Column(Float, default=0.0)


class InferenceLog(Base):
    """ML_Inference_Log entity (Proposal Figure 3.4) with analyst case management."""
    __tablename__ = "ml_inference_log"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    tx_id = Column(String, ForeignKey("parsed_transactions.tx_id", ondelete="CASCADE"), unique=True, index=True)
    anomaly_score = Column(Float, nullable=False)
    ml_score = Column(Float, default=0.0)
    policy_score = Column(Float, default=0.0)
    scoring_source = Column(String, default="HYBRID")
    binary_verdict = Column(Integer, nullable=False)
    static_rule_verdict = Column(Integer, default=0)
    threshold_used = Column(Float, default=0.80)
    action_taken = Column(String, nullable=False)
    latency_ms = Column(Float, default=0.0)
    vendor_unique_senders_15min = Column(Integer, default=0)
    vendor_inflow_15min = Column(Float, default=0.0)
    triggering_features = Column(Text, default="[]")
    review_status = Column(String, default="PENDING")  # PENDING, CONFIRMED_FRAUD, FALSE_POSITIVE
    reviewed_at = Column(DateTime, nullable=True)
    logged_at = Column(DateTime, default=datetime.utcnow)


class SystemSetting(Base):
    """Persisted SOC Administrator configuration."""
    __tablename__ = "system_settings"
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)


def _migrate_parsed_transactions():
    """Safely add new columns to an existing SQLite DB without losing data."""
    expected_columns = {
        "tx_type": "VARCHAR DEFAULT 'PAYMENT'",
        "oldbalance_org": "FLOAT DEFAULT 0.0",
        "newbalance_orig": "FLOAT DEFAULT 0.0",
        "oldbalance_dest": "FLOAT",
        "newbalance_dest": "FLOAT DEFAULT 0.0",
    }
    with engine.begin() as conn:
        rows = conn.execute(text("PRAGMA table_info(parsed_transactions)")).fetchall()
        existing = {row[1] for row in rows}
        for col_name, col_def in expected_columns.items():
            if col_name not in existing:
                conn.execute(text(f"ALTER TABLE parsed_transactions ADD COLUMN {col_name} {col_def}"))


def init_db():
    Base.metadata.create_all(bind=engine)
    _migrate_parsed_transactions()


def reset_db():
    """Clear transactional records while preserving schema (used by tests & admin reset)."""
    init_db()
    session = SessionLocal()
    try:
        session.query(InferenceLog).delete()
        session.query(Transaction).delete()
        session.commit()
    finally:
        session.close()
