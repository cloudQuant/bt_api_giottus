from __future__ import annotations

from typing import TYPE_CHECKING

from bt_api_base.plugins.protocol import PluginInfo

from bt_api_giottus import __version__
from bt_api_giottus.registry_registration import register_giottus

if TYPE_CHECKING:
    from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
    from bt_api_base.registry import ExchangeRegistry


def register_plugin(
    registry: type[ExchangeRegistry], runtime_factory: type[GatewayRuntimeRegistrar]
) -> PluginInfo:
    register_giottus(registry)
    return PluginInfo(
        name="bt_api_giottus",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("GIOTTUS___SPOT",),
        supported_asset_types=("SPOT",),
    )
