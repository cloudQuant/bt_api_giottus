from __future__ import annotations

from bt_api_base.balance_utils import simple_balance_handler as _giottus_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_giottus.exchange_data import GiottusExchangeDataSpot
from bt_api_giottus.feeds.live_giottus.spot import GiottusRequestDataSpot


def register_giottus(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("GIOTTUS___SPOT", GiottusRequestDataSpot)
    registry.register_exchange_data("GIOTTUS___SPOT", GiottusExchangeDataSpot)
    registry.register_balance_handler("GIOTTUS___SPOT", _giottus_balance_handler)
