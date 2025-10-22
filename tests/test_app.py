"""
Unit tests for app module
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from app import greet, add, multiply

def test_greet():
    """Test greet function"""
    assert greet("John") == "Hello, John!"
    assert greet("Jenkins") == "Hello, Jenkins!"

def test_greet_empty_name():
    """Test greet with empty name"""
    with pytest.raises(ValueError):
        greet("")

def test_add():
    """Test add function"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_multiply():
    """Test multiply function"""
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0

def test_multiply_by_zero():
    """Test multiply by zero"""
    assert multiply(100, 0) == 0
