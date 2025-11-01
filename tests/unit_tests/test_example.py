"""Example unit tests using pytest.

This file demonstrates basic pytest usage and testing patterns.
Shows how to import and test functions from the app package.
"""

import pytest

from app.main import add_numbers, calculate_factorial, greet, main


def test_greet():
    """Test the greet function."""
    assert greet("World") == "Hello, World!"
    assert greet("Python") == "Hello, Python!"
    assert greet("") == "Hello, !"


def test_add_numbers():
    """Test the add_numbers function."""
    assert add_numbers(2, 3) == 5
    assert add_numbers(0, 0) == 0
    assert add_numbers(-1, 1) == 0
    assert add_numbers(100, 200) == 300


def test_calculate_factorial():
    """Test the calculate_factorial function."""
    assert calculate_factorial(0) == 1
    assert calculate_factorial(1) == 1
    assert calculate_factorial(5) == 120
    assert calculate_factorial(10) == 3628800


def test_calculate_factorial_negative():
    """Test that calculate_factorial raises ValueError for negative numbers."""
    with pytest.raises(
        ValueError, match="Factorial is not defined for negative numbers"
    ):
        calculate_factorial(-1)


def test_basic_assertion():
    """Test basic assertion."""
    assert 1 + 1 == 2


def test_string_operations():
    """Test string operations."""
    text = "hello world"
    assert text.upper() == "HELLO WORLD"
    assert "world" in text


def test_main(capsys):
    """Test the main entry point function.

    Uses pytest's capsys fixture to capture stdout and verify output.
    """
    main()
    captured = capsys.readouterr()
    assert "Hello World!" in captured.out
    assert "Hello, Developer!" in captured.out
    assert "5 + 3 = 8" in captured.out
    assert "5! = 120" in captured.out
