"""Thermia numbers integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.number import NumberEntity, NumberDeviceClass

from .const import DOMAIN
from .coordinator import ThermiaDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Thermia numbers."""

    coordinator: ThermiaDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass_thermia_numbers = []

    for idx, heat_pump in enumerate(coordinator.data.heat_pumps):
        
    async_add_entities(hass_thermia_numbers)
