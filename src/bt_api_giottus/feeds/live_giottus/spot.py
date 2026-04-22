from __future__ import annotations

from typing import Any

from bt_api_base.functions.utils import update_extra_data

from bt_api_giottus.feeds.live_giottus.request_base import GiottusRequestData


class GiottusRequestDataSpot(GiottusRequestData):
    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "GIOTTUS___SPOT")

    def _get_tick(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        path = self._params.rest_paths.get("get_ticker", "GET /v1/ticker")
        extra_data = update_extra_data(
            extra_data,
            request_type="get_tick",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=GiottusRequestDataSpot._get_tick_normalize_function,
        )
        return path, {"symbol": symbol}, extra_data

    @staticmethod
    def _get_tick_normalize_function(input_data: Any, extra_data: Any):
        if not input_data:
            return [], False
        data = input_data if isinstance(input_data, dict) else {}
        ticker = data.get("data", data)
        return [ticker], ticker is not None

    def get_tick(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_tick(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_depth(self, symbol: Any, count: int = 20, extra_data: Any = None, **kwargs: Any):
        path = self._params.rest_paths.get("get_depth", "GET /v1/orderbook")
        extra_data = update_extra_data(
            extra_data,
            request_type="get_depth",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=GiottusRequestDataSpot._get_depth_normalize_function,
        )
        return path, {"symbol": symbol, "limit": count}, extra_data

    @staticmethod
    def _get_depth_normalize_function(input_data: Any, extra_data: Any):
        if not input_data:
            return [], False
        data = input_data if isinstance(input_data, dict) else {}
        depth = data.get("data", data)
        return [depth], depth is not None

    def get_depth(self, symbol: Any, count: int = 20, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_depth(self, symbol: Any, count: int = 20, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_kline(
        self, symbol: Any, period: Any, count: int = 20, extra_data: Any = None, **kwargs: Any
    ):
        path = self._params.rest_paths.get("get_kline", "GET /v1/klines")
        extra_data = update_extra_data(
            extra_data,
            request_type="get_kline",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=GiottusRequestDataSpot._get_kline_normalize_function,
        )
        return (
            path,
            {
                "symbol": symbol,
                "interval": self._params.kline_periods.get(period, period),
                "limit": count,
            },
            extra_data,
        )

    @staticmethod
    def _get_kline_normalize_function(input_data: Any, extra_data: Any):
        if not input_data:
            return [], False
        data = input_data if isinstance(input_data, dict) else {}
        klines = data.get("data", data.get("klines", []))
        return [klines], klines is not None

    def get_kline(
        self, symbol: Any, period: Any, count: int = 20, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_kline(
        self, symbol: Any, period: Any, count: int = 20, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_exchange_info(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.rest_paths.get("get_markets", "GET /v1/markets")
        extra_data = update_extra_data(
            extra_data,
            request_type="get_exchange_info",
            symbol_name="",
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=GiottusRequestDataSpot._get_exchange_info_normalize_function,
        )
        return path, {}, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(input_data: Any, extra_data: Any):
        if not input_data:
            return [], False
        data = input_data if isinstance(input_data, dict) else {}
        markets = data.get("data", data.get("markets", []))
        return [markets], markets is not None

    def get_exchange_info(self, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_balance(self, symbol: Any = None, extra_data: Any = None, **kwargs: Any):
        path = self._params.rest_paths.get("get_balance", "POST /v1/balance")
        extra_data = update_extra_data(
            extra_data,
            request_type="get_balance",
            symbol_name=symbol or "",
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=GiottusRequestDataSpot._get_balance_normalize_function,
        )
        return path, {}, extra_data

    @staticmethod
    def _get_balance_normalize_function(input_data: Any, extra_data: Any):
        if not input_data:
            return [], False
        return [input_data], True

    def get_balance(self, symbol: Any = None, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_balance(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_account(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.rest_paths.get("get_balance", "POST /v1/balance")
        extra_data = update_extra_data(
            extra_data,
            request_type="get_account",
            symbol_name="",
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=GiottusRequestDataSpot._get_account_normalize_function,
        )
        return path, {}, extra_data

    @staticmethod
    def _get_account_normalize_function(input_data: Any, extra_data: Any):
        if not input_data:
            return [], False
        return [input_data], True

    def get_account(self, symbol: Any = "ALL", extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_account(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _make_order(
        self,
        symbol: Any,
        volume: Any,
        price: Any = None,
        order_type: Any = "buy-limit",
        offset: str = "open",
        post_only: bool = False,
        client_order_id: Any = None,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        path = self._params.rest_paths.get("make_order", "POST /v1/order")
        side = "BUY" if "buy" in order_type.lower() else "SELL"
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": str(volume),
            "price": str(price),
            "type": "LIMIT" if price else "MARKET",
        }
        extra_data = update_extra_data(
            extra_data,
            request_type="make_order",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            normalize_function=GiottusRequestDataSpot._make_order_normalize_function,
        )
        return path, params, extra_data

    @staticmethod
    def _make_order_normalize_function(input_data: Any, extra_data: Any):
        if not input_data:
            return [], False
        return [input_data], True

    def make_order(
        self,
        symbol: Any,
        volume: Any,
        price: Any = None,
        order_type: Any = "buy-limit",
        offset: str = "open",
        post_only: bool = False,
        client_order_id: Any = None,
        extra_data: Any = None,
        **kwargs: Any,
    ):
        path, params, extra_data = self._make_order(
            symbol, volume, price, order_type, offset, extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data)

    def _cancel_order(self, symbol: Any, order_id: Any, extra_data: Any = None, **kwargs: Any):
        path = self._params.rest_paths.get("cancel_order", "POST /v1/cancel")
        params = {"orderId": order_id}
        extra_data = update_extra_data(
            extra_data,
            request_type="cancel_order",
            symbol_name=symbol,
            asset_type=self.asset_type,
            exchange_name=self.exchange_name,
            order_id=order_id,
        )
        return path, params, extra_data

    def cancel_order(self, symbol: Any, order_id: Any, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._cancel_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)
