from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class GiottusExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "GIOTTUS___SPOT"
        self.rest_url = "https://api.giottus.com"
        self.wss_url = "wss://api.giottus.com"
        self.rest_paths = {}
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "4h": "4h",
            "1d": "1d",
            "1w": "1w",
        }
        self.legal_currency = ["INR", "USDT", "USD", "BTC", "ETH"]

    def get_period(self, period: str) -> str:
        return self.kline_periods.get(period, period)


class GiottusExchangeDataSpot(GiottusExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "spot"
