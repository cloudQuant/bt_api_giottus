"""Tests for GiottusExchangeData container."""

from __future__ import annotations

from bt_api_giottus.exchange_data import GiottusExchangeData


class TestGiottusExchangeData:
    """Tests for GiottusExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = GiottusExchangeData()

        assert exchange.exchange_name == "GIOTTUS___SPOT"
