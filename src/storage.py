import csv
from pathlib import Path
from typing import List
from datetime import date

from models import Transaction

CSV_HEADER = ["date", "type", "category", "amount", "comment"]

def ensure_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)

def load_transactions(path: Path) -> List[Transaction]:
    ensure_csv(path)
    txns: List[Transaction] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # пропустим странные/пустые строки
            if not row.get("date") or not row.get("type") or not row.get("category") or not row.get("amount"):
                continue
            dt = date.fromisoformat(row["date"])
            txn_type = row["type"]
            category = row["category"]
            amount = float(row["amount"])
            comment = row.get("comment", "") or ""
            txns.append(Transaction(dt=dt, txn_type=txn_type, category=category, amount=amount, comment=comment))
    return txns

def save_transactions(path: Path, txns: List[Transaction]) -> None:
    ensure_csv(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADER)
        for t in txns:
            writer.writerow([t.dt.isoformat(), t.txn_type, t.category, f"{t.amount:.2f}", t.comment or ""])

def append_transaction(path: Path, t: Transaction) -> None:
    ensure_csv(path)
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([t.dt.isoformat(), t.txn_type, t.category, f"{t.amount:.2f}", t.comment or ""])