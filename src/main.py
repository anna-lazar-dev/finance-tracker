from pathlib import Path
from datetime import date, timedelta

from models import Transaction
from storage import load_transactions, append_transaction, save_transactions
from reports import filter_by_period, summary, top_expense_categories
from utils import (
    ask, ask_optional, parse_date, parse_amount,
    normalize_type, normalize_category, press_enter
)

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "transactions.csv"

def choose_period() -> tuple[date, date]:
    print("\nВыбери период:")
    print("1) Сегодня")
    print("2) Последние 7 дней")
    print("3) Текущий месяц")
    print("4) Произвольный (дата_от — дата_до)")
    choice = ask("> ")

    today = date.today()

    if choice == "1":
        return today, today
    if choice == "2":
        return today - timedelta(days=6), today
    if choice == "3":
        start = today.replace(day=1)
        return start, today
    if choice == "4":
        start = parse_date(ask("Дата от (YYYY-MM-DD): "))
        end = parse_date(ask("Дата до (YYYY-MM-DD): "))
        if end < start:
            raise ValueError("Дата 'до' не может быть раньше даты 'от'.")
        return start, end

    raise ValueError("Неверный выбор периода.")

def print_transactions(txns: list[Transaction]) -> None:
    if not txns:
        print("\n(пусто)")
        return
    print("\n# | date       | type    | category     | amount   | comment")
    print("--+------------+---------+--------------+----------+--------")
    for i, t in enumerate(txns, start=1):
        cmt = (t.comment or "").strip()
        print(f"{i:2d}| {t.dt.isoformat():10s} | {t.txn_type:7s} | {t.category:12s} | {t.amount:8.2f} | {cmt}")

def add_transaction() -> None:
    print("\nДобавление транзакции")
    dt = parse_date(ask_optional("Дата (YYYY-MM-DD, пусто = сегодня): "))
    txn_type = normalize_type(ask("Тип (расход/доход): "))
    category = normalize_category(ask("Категория (например еда/здоровье/транспорт/счета/другое): "))
    amount = parse_amount(ask("Сумма: "))
    comment = ask_optional("Комментарий (необязательно): ")

    t = Transaction(dt=dt, txn_type=txn_type, category=category, amount=amount, comment=comment)
    append_transaction(DATA_PATH, t)
    print("✅ Сохранено.")

def show_transactions() -> None:
    txns = load_transactions(DATA_PATH)
    start, end = choose_period()
    subset = filter_by_period(txns, start, end)
    print(f"\nТранзакции за период {start.isoformat()} — {end.isoformat()}:")
    print_transactions(subset)

def show_summary() -> None:
    txns = load_transactions(DATA_PATH)
    start, end = choose_period()
    subset = filter_by_period(txns, start, end)
    inc, exp, bal = summary(subset)
    print(f"\nИтоги за {start.isoformat()} — {end.isoformat()}:")
    print(f"Доходы : {inc:.2f}")
    print(f"Расходы: {exp:.2f}")
    print(f"Баланс : {bal:.2f}")

def show_top_categories() -> None:
    txns = load_transactions(DATA_PATH)
    start, end = choose_period()
    subset = filter_by_period(txns, start, end)
    top = top_expense_categories(subset, top_n=5)
    print(f"\nТоп категорий расходов за {start.isoformat()} — {end.isoformat()}:")
    if not top:
        print("(нет расходов в выбранном периоде)")
        return
    for i, (cat, total) in enumerate(top, start=1):
        print(f"{i}. {cat}: {total:.2f}")

def delete_transaction() -> None:
    txns = load_transactions(DATA_PATH)
    if not txns:
        print("\nУдалять нечего — список пуст.")
        return

        print("\nВсе транзакции:")
    print_transactions(txns)
    raw = ask("\nВведи номер для удаления (0 = отмена): ")
    if not raw.isdigit():
        print("Нужно число.")
        return
    idx = int(raw)
    if idx == 0:
        return
    if idx < 1 or idx > len(txns):
        print("Нет транзакции с таким номером.")
        return

    removed = txns.pop(idx - 1)
    save_transactions(DATA_PATH, txns)
    print(f"🗑️ Удалено: {removed.dt.isoformat()} {removed.txn_type} {removed.category} {removed.amount:.2f}")

def main() -> None:
    while True:
        print("\n=== Finance Tracker ===")
        print("1. Добавить транзакцию")
        print("2. Показать периоды")
        print("3. Краткий отчет")
        print("4. Топ категорий расходов")
        print("5. Удалить транзакцию")
        print("0. Выход")

        choice = ask("> ")

        try:
            if choice == "1":
                add_transaction()
                press_enter()
            elif choice == "2":
                show_transactions()
                press_enter()
            elif choice == "3":
                show_summary()
                press_enter()
            elif choice == "4":
                show_top_categories()
                press_enter()
            elif choice == "5":
                delete_transaction()
                press_enter()
            elif choice == "0":
                print("Пока!")
                break
            else:
                print("Неверный пункт меню.")
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            press_enter()

if __name__ == "__main__":
    main()