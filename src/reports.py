from __future__ import annotations
from datetime import date
from typing import List, Tuple, Dict

from models import Transaction

def filter_by_period(txns: List[Transaction], start: date, end: date) -> List[Transaction]:
    # включительно
    return [t for t in txns if start <= t.dt <= end]

def summary(txns: List[Transaction]) -> Tuple[float, float, float]:
    income = sum(t.amount for t in txns if t.txn_type == "income")
    expense = sum(t.amount for t in txns if t.txn_type == "expense")
    balance = income - expense
    return income, expense, balance

def top_expense_categories(txns: List[Transaction], top_n: int = 5) -> List[Tuple[str, float]]:
    totals: Dict[str, float] = {}
    for t in txns:
        if t.txn_type != "expense":
            continue
        totals[t.category] = totals.get(t.category, 0.0) + t.amount
    items = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    return items[:top_n]