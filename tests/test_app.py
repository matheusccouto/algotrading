"""Unit-tests for the apps."""

import app

class TestTimeHistory:
    """Tests for the get_time_history function."""

    @staticmethod
    def test_func():
        app.get_stock_time_history("PETR3")
