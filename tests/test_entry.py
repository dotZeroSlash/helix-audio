import pytest
from unittest.mock import patch
import sys
from entry import run_main

def test_run_main_success():
    with patch('src.main.main') as mock_main:
        mock_main.return_value = 0
        assert run_main() == 0
        mock_main.assert_called_once()

def test_run_main_failure():
    with patch('src.main.main') as mock_main:
        mock_main.side_effect = Exception("Test error")
        assert run_main() == 1

def test_main_exception_handling():
    with patch('src.main.main') as mock_main:
        mock_main.side_effect = KeyboardInterrupt()
        assert run_main() == 0  # Should exit gracefully

