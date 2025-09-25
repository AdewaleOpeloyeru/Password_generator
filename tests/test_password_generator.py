import string
import pytest
from unittest.mock import patch
from src import password_generator


def test_get_menu_choice_valid(monkeypatch):
    # Simulate user entering '1'
    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert password_generator.get_menu_choice() == 1

    # Simulate user entering '2'
    monkeypatch.setattr("builtins.input", lambda _: "2")
    assert password_generator.get_menu_choice() == 2


def test_get_menu_choice_invalid_then_valid(monkeypatch):
    # Simulate user entering invalid input then valid input
    inputs = iter(["abc", "3", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert password_generator.get_menu_choice() == 1


def test_get_password_options_all_yes(monkeypatch):
    # Simulate user entering all valid 'yes' options
    inputs = iter(["12", "y", "y", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = password_generator.get_password_options()
    assert result == (12, True, True, True)


def test_get_password_options_all_no(monkeypatch):
    # Simulate user entering all valid 'no' options
    inputs = iter(["10", "n", "n", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = password_generator.get_password_options()
    assert result == (10, False, False, False)


def test_get_password_options_invalid_then_valid(monkeypatch):
    # Simulate user entering invalid then valid inputs
    inputs = iter(["7", "8", "maybe", "y", "no", "n", "ok", "y", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = password_generator.get_password_options()
    # Should accept 8, y, n, y
    assert result == (8, True, False, True)


@pytest.mark.parametrize("length", [8, 16, 32, 64])
def test_password_length(length, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    password = password_generator.generate_password(length, True, True, True)
    assert len(password) == length


def test_password_contains_uppercase(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    password = password_generator.generate_password(12, True, False, False)
    assert any(c.isupper() for c in password)


def test_password_contains_digit(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    password = password_generator.generate_password(12, False, True, False)
    assert any(c.isdigit() for c in password)


def test_password_contains_special(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    password = password_generator.generate_password(12, False, False, True)
    special = "!@#$%&^()_+*-="
    assert any(c in special for c in password)


def test_password_only_lowercase(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    password = password_generator.generate_password(12, False, False, False)
    assert all(c in string.ascii_lowercase for c in password)


def test_password_all_categories(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    password = password_generator.generate_password(20, True, True, True)
    special = "!@#$%&^()_+*-="
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in special for c in password)
    assert any(c.islower() for c in password)


def test_main_generate_and_exit(monkeypatch):
    # Simulate: choose 1 (generate), then provide options, then choose 2 (exit)
    inputs = iter(
        [
            "1",  # menu: generate password
            "12",  # password length
            "y",  # use uppercase
            "n",  # use digits
            "y",  # use special
            "n",  # regenerate password? (exit generation)
            "2",  # menu: exit
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with patch("pyperclip.copy"):
        # Run main, should exit after generating one password and then choosing exit
        password_generator.main()
