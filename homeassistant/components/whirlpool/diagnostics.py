"""Diagnostics support for Whirlpool."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import WhirlpoolConfigEntry

TO_REDACT = {
    "SERIAL_NUMBER",
    "macaddress",
    "username",
    "password",
    "token",
    "unique_id",
    "SAID",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    config_entry: WhirlpoolConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    whirlpool = config_entry.runtime_data
    diagnostics_data = {
        "Washer_dryers": {
            wd["NAME"]: dict(wd.items())
            for wd in whirlpool.appliances_manager.washer_dryers
        },
        "aircons": {
            ac["NAME"]: dict(ac.items()) for ac in whirlpool.appliances_manager.aircons
        },
        "ovens": {
            oven["NAME"]: dict(oven.items())
            for oven in whirlpool.appliances_manager.ovens
        },
    }

    return {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "appliances": async_redact_data(diagnostics_data, TO_REDACT),
    }
