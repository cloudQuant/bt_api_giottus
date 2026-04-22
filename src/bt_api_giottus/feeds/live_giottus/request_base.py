from __future__ import annotations

from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient

from bt_api_giottus.exchange_data import GiottusExchangeDataSpot


class GiottusRequestData(Feed):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "GIOTTUS___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = GiottusExchangeDataSpot()
        self._params.api_key = kwargs.get("public_key") or kwargs.get("api_key") or ""
        self._params.api_secret = (
            kwargs.get("private_key") or kwargs.get("secret_key") or kwargs.get("api_secret") or ""
        )
        self._http_client = HttpClient(venue=self.exchange_name, timeout=10)

    def _get_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "User-Agent": "bt-api-plugin/1.0"}
        if getattr(self._params, "api_key", None):
            headers["X-API-KEY"] = self._params.api_key
        return headers

    def request(
        self,
        path: str,
        params: Any = None,
        body: Any = None,
        extra_data: Any = None,
        timeout: int = 10,
    ):
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path
        response = self._http_client.request(
            method=method,
            url=self._params.rest_url + request_path,
            headers=self._get_headers(),
            json_data=body if method == "POST" else None,
            params=params,
        )
        return RequestData(response, extra_data or {})

    async def async_request(
        self,
        path: str,
        params: Any = None,
        body: Any = None,
        extra_data: Any = None,
        timeout: int = 5,
    ):
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path
        response = await self._http_client.async_request(
            method=method,
            url=self._params.rest_url + request_path,
            headers=self._get_headers(),
            json_data=body if method == "POST" else None,
            params=params,
        )
        return RequestData(response, extra_data or {})

    def async_callback(self, future: Any):
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as exc:
            self.logger.error("Async callback error: %s", exc)

    def _get_server_time(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.rest_paths.get("get_server_time", "GET /v1/time")
        extra_data = extra_data or {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_server_time",
                "normalize_function": self._get_server_time_normalize_function,
            }
        )
        return path, {}, extra_data

    def get_server_time(self, extra_data: Any = None, **kwargs: Any):
        path, params, extra_data = self._get_server_time(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    @staticmethod
    def _get_server_time_normalize_function(input_data: Any, extra_data: Any):
        if not input_data:
            return None, False
        if isinstance(input_data, dict):
            ts = input_data.get("timestamp", input_data.get("time", input_data.get("serverTime")))
            return ts, True
        return input_data, True

    def push_data_to_queue(self, data: Any):
        if self.data_queue is not None:
            self.data_queue.put(data)

    def connect(self):
        pass

    def disconnect(self):
        super().disconnect()

    def is_connected(self):
        return True
