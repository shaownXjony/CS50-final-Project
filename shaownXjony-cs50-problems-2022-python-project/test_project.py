import pytest
from datetime import datetime
from project import get_today, hash_password, get_week_range, load_users, save_users

def test_get_today():
    result = get_today()
    assert len(result) == 10
    assert result[4] == '-'
    assert result[7] == '-'
    datetime.strptime(result, "%Y-%m-%d")

def test_hash_password():
    password = "testpassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 == hash2
    assert len(hash1) == 64
    assert hash_password("password1") != hash_password("password2")

    empty_hash = hash_password("")
    assert len(empty_hash) == 64

def test_get_week_range():
    start, end = get_week_range()
    assert hasattr(start, 'weekday')
    assert hasattr(end, 'weekday')

    assert start.weekday() == 0
    assert (end - start).days == 6
    assert end > start

def test_load_users():
    """Test loading users from file"""
    result = load_users()
    assert isinstance(result, dict)

def test_save_users():
    test_users = {
        "testuser": {
            "password": "hashedpassword",
            "weekly_budget": 100.0,
            "savings": 50.0,
            "expenses": []
        }
    }

    try:
        save_users(test_users)
        assert True
    except Exception as e:
        pytest.fail(f"save_users raised an exception: {e}")
    try:
        save_users({})
        assert True
    except Exception as e:
        pytest.fail(f"save_users with empty dict raised an exception: {e}")

def test_expense_calculations():
    expenses = [
        {"date": "2025-07-01", "amount": 25.50, "category": "food"},
        {"date": "2025-07-02", "amount": 15.75, "category": "transport"},
        {"date": "2025-07-03", "amount": 30.00, "category": "entertainment"}]
    total = sum(expense["amount"] for expense in expenses)
    assert total == 71.25
