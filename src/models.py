from dataclasses import dataclass
from datetime import date
from typing import Optional, Literal

TxnType = Literal["expense", "income"]

@dataclass(frozen=True)
class Transaction:
    dt: date
    txn_type: TxnType
    category: str
    amount: float
    comment: Optional[str] = ""
