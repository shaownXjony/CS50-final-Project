import os
import json
from datetime import datetime,timedelta
from hashlib import sha256

CATEGORIES=["food","transportation","entertainment","rent"]
DATA_FILE="users_data.json"

def clear_screen():
    os.system("cls" if os.name=="nt"  else "clear")

def get_today():
    return datetime.today().strftime("%Y-%m-%d")

def get_week_range():
    today=datetime.today()
    start=today-timedelta(days=today.weekday())
    return start.date(),(start+timedelta(days=6)).date()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("⚠️ Could not read user data file. Starting with empty user list.")
            return {}
    return {}


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users,f,indent=4)

def prompt_float(prompt):
    while True:
        try:
            value=float(input(prompt).strip())
            if value <0:
                print("❌ Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("❌ Invalid number.")
            continue

def prompt_date(prompt,default=None):
    date_str=input(prompt).strip()
    if not date_str and default:
        return default
    try:
        return datetime.strptime(date_str,"%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print("❌ Invalid Date format. Using default.")
        return default or get_today()

def register_user(users):
    username = input("Enter new username: ").strip()
    if not username:
        print("\n❌ Username cannot be empty.")
        return None

    username_lower = username.lower()
    existing_usernames = {k.lower(): k for k in users.keys()}

    if username_lower in existing_usernames:
        print("\n❌ Username already exists.")
        return None

    password = input("Enter password: ").strip()
    if not password:
        print("\n❌ Password cannot be empty.")
        return None

    users[username] = {
        "password": hash_password(password),
        "weekly_budget": 0,
        "savings": 0.0,
        "last_transfer": "",
        "savings_log": [],
        "expenses": []
    }
    save_users(users)
    print("\n✅ Registration successful!")
    return username


def login_user(users):
    username=input("Enter username: ").strip()
    password=input("Enter password: ").strip()

    if not username or not password:
        print("\n❌ Username and password cannot be empty.")
        return None

    for stored_username, user_data in users.items():
        if stored_username.lower() == username.lower():
            if user_data["password"] == hash_password(password):
                print("\n✅ Login successful!")
                return stored_username
            else:
                print("\n❌ Invalid username or password")
                return None

    print("\n❌ Invalid username or password")
    return None

def perform_transfer(users,username,auto=False):
    today=datetime.today()
    print("\n Manual transfer only allowed on sunday")
    if not auto and today.weekday()!=6:
        return
    if auto and users[username]["last_transfer"]==get_today():
        return
    start,end=get_week_range()
    total_spent=sum(
        e["amount"] for e in users[username]["expenses"]
        if start <= datetime.strptime(e["date"], "%Y-%m-%d").date() <= end
    )
    remaining =users[username]["weekly_budget"] - total_spent
    users[username]["savings"]+=remaining
    users[username]["last_transfer"]=get_today()
    users[username]["savings_log"].append({"date":get_today(),"amount":remaining})
    save_users(users)

    if auto:
        print("\n Auto transferred weekly remaining to savings")
    if remaining >=0:
        print(f" ${remaining:.2f} added to savings.")
    else:
        print(f" ${remaining:.2f} deducted from savings.")
    if auto:
        input("\nPress Enter to continue...")

def set_budget(users,username):
    amount=prompt_float("Enter your weekly budget: $")
    if amount:
        users[username]["weekly_budget"]=amount
        save_users(users)
        print("\n✅ Weekly budget set successfully!")

def add_expenses(users,username):
    print("\n Add Expenses")
    date=prompt_date("Enter date (YYYY-MM-DD) [default: today]: ",get_today())
    print("\n Leave blank or 0 to skip a category.\n")
    for cat in CATEGORIES:
        value=input(f"Enter expense for {cat.capitalize()}: ").strip()
        if not value or value=="0":
            continue
        try:
            amount=float(value)
            if amount>=0:
                users[username]["expenses"].append({
                    "date":date,
                    "category":cat,
                    "amount":amount
                })
        except ValueError:
            print(f"❌ Invalid amount for {cat}.Skipped.")
    while input("\nAdd a custom category? (yes/no): ").strip().lower()=="yes":
        cat=input("Enter custom category name: ").strip().lower()
        if not cat:
            print("Category name cannot be empty")
            continue
        amount=prompt_float(f"Enter amount for {cat.capitalize()}: ")
        if amount is not None:
            users[username]["expenses"].append({
                "date":date,
                "category":cat,
                "amount":amount
            })
    save_users(users)
    print("\n✅ Expenses added successfully.")

def edit_delete_expense(users, username):
    expenses = users[username]["expenses"]
    if not expenses:
        print("\n📭 No expenses to edit or delete.")
        return

    print("\n📋 All Expenses:")
    for i, e in enumerate(expenses, 1):
        print(f"{i}. {e['date']} - ${e['amount']} [{e['category']}]")

    try:
        idx = int(input("\nEnter the number of the expense to edit/delete: ")) - 1
        if not 0 <= idx < len(expenses):
            raise ValueError
        e = expenses[idx]
        print(f"\nSelected: {e['date']} - ${e['amount']} [{e['category']}]")
        action = input("Type 'edit' to modify or 'delete' to remove this expense: ").strip().lower()

        if action == "edit":
            new_date = prompt_date(f"New date [Leave blank to keep '{e['date']}']: ", e['date'])
            new_category = input(f"New category [Leave blank to keep '{e['category']}']: ").strip() or e['category']
            new_amount = input(f"New amount [Leave blank to keep ${e['amount']}]: ").strip()

            e['date'] = new_date
            e['category'] = new_category
            if new_amount:
                try:
                    e['amount'] = float(new_amount)
                except ValueError:
                    print("❌ Invalid amount. Keeping old amount.")
            save_users(users)
            print("\n✅ Expense updated successfully!")
        elif action == "delete":
            if input("Are you sure? (yes/no): ").strip().lower() == "yes":
                expenses.pop(idx)
                save_users(users)
                print("🗑️ Expense deleted.")
        else:
            print("❌ Invalid action.")
    except ValueError:
        print("❌ Invalid selection.")

def view_report(users,username):
    start,end=get_week_range()
    print(f"\n Weekly Report ({start} to {end})")
    print("=" *40)
    total=0
    for e in users[username]["expenses"]:
        date=datetime.strptime(e["date"],"%Y-%m-%d").date()
        if start<=date<=end:
            print(f"{e['date']} - ${e['amount']:.2f} [{e['category']}]")
            total+=e["amount"]
    remaining=users[username]["weekly_budget"]-total
    print("=" *40)
    print(f"Total Spent: ${total:.2f}")
    print(f"Remaining: ${remaining:.2f}")

def display_summary(users,username):
    start,end=get_week_range()
    total_spent=0
    category_totals={}

    for e in users[username]["expenses"]:
        date=datetime.strptime(e["date"],"%Y-%m-%d").date()
        if start<=date<=end:
            total_spent+=e["amount"]
            cat=e["category"].capitalize()
            category_totals[cat]=category_totals.get(cat,0)+e["amount"]

    remaining=users[username]["weekly_budget"]-total_spent
    print(f"\n📊 Weekly Budget: ${users[username]['weekly_budget']:.2f}")
    print(f"💸 Spent: ${total_spent:.2f}")
    print(f"💵 Remaining: ${remaining:.2f}")
    print(f"💼 Savings: ${users[username]['savings']:.2f}")

    if category_totals:
        print("\n Recent Expenses by Category:")
        for cat,amt in category_totals.items():
            print(f" - {cat}: ${amt:.2f}")
    else:
        print("\n No expenses this week")

def main_menu(users,username):
    while True:
        clear_screen()
        print(f"====Smart Weekly Budget Planner (User: {username}) ====")
        display_summary(users,username)

        print("\n1. Set Weekly Budget")
        print("2. Expense Management")
        print("3. View Weekly Report")
        print("4. Transfer Remaining to Savings (Sunday only)")
        print("5. Save and Exit")
        print("6. Logout")

        choice=input("Select an option (1-6): ").strip()

        if choice=="1":
            set_budget(users,username)
        elif choice=="2":
            print("\nExpense Management:")
            print(" a. Add Expense")
            print(" b. Edit/delete Expense")
            sub=input("Choose an option (a/b): ").strip().lower()
            if sub=="a":
                add_expenses(users,username)
            elif sub=="b":
                edit_delete_expense(users,username)
            else:
                print("❌ Invalid choice ")
            input("\nPress Enter to continue...")
        elif choice=="3":
            view_report(users,username)
            input("\nPress Enter to return...")
        elif choice=="4":
            perform_transfer(users,username,auto=False)
            input("\nPress Enter to return...")
        elif choice=="5":
            save_users(users)
            print("\n Data saved. ...Goodbye...")
            break
        elif choice=="6":
            return
        else:
            print("❌ Invalid Choice")
            input("\nPress Enter to return...")

def main():
    users = load_users()
    username = None

    while not username:
        clear_screen()
        print("===== Smart Weekly Budget Planner =====")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()
        if choice == "1":
            username = login_user(users)
            if username:
                perform_transfer(users, username, auto=True)
        elif choice == "2":
            username = register_user(users)
        elif choice == "3":
            print("\n...Goodbye!...")
            return
        else:
            print("❌ Invalid choice.")
            input("Press Enter to continue...")

    main_menu(users, username)


if __name__ == "__main__":
    main()
