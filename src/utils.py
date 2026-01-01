from datetime import datetime, date
from typing import Optional

def parse_date(s: str) -> date:
    s = s.strip()
    if not s:
        return date.today()
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError("Неверный формат даты. Используй YYYY-MM-DD (например 2025-01-02).") from e

def parse_amount(s: str) -> float:
    s = s.strip().replace(",", ".")
    try:
        val = float(s)
    except ValueError as e:
        raise ValueError("Сумма должна быть числом (например 1200 или 12.50).") from e
    if val <= 0:
        raise ValueError("Сумма должна быть больше 0.")
    return val

def normalize_type(s: str) -> str:
    s = s.strip().lower()
    # поддержим ввод по-русски, чтобы было проще
    if s in ("расход", "р", "expense", "e"):
        return "expense"
    if s in ("доход", "д", "income", "i"):
        return "income"
    raise ValueError("Тип должен быть: расход/доход (или expense/income).")

def normalize_category(s: str) -> str:
    s = s.strip().lower()
    if not s:
        return "other"
    return s

def ask(prompt: str) -> str:
    return input(prompt).strip()

def ask_optional(prompt: str) -> str:
    return input(prompt).strip()

def press_enter() -> None:
    input("\nНажми Enter чтобы продолжить...")