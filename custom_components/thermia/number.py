""" Thermia numbers integration """

from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfTemperature, UnitOfTime, UnitOfPressure 
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import ThermiaDataUpdateCoordinator
from .numbers.generic_number import ThermiaGenericNumber


from .const import (
    DOMAIN,
    MDI_TEMPERATURE_ICON,
    MDI_TIMER_COG_OUTLINE_ICON,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the platform."""

    coordinator: ThermiaDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass_thermia_numbers = []

    _LOGGER = logging.getLogger(__name__)
    _LOGGER.debug("Number starting ")
    
    for idx, heat_pump in enumerate(coordinator.data.heat_pumps):
        _LOGGER.debug("Start loop")
        if heat_pump.HC_REG_HEATING_HEAT_CURVE:
            _LOGGER.debug("inside heat curve")
            hass_thermia_numbers.append(
                ThermiaGenericNumber(
                    coordinator,
                    idx,
                    "is_online",
                    "HEATING HEAT CURVE",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.CONFIG,
                    "temperature",
                    "measurement",
                    "HC_REG_HEATING_HEAT_CURVE",
                    UnitOfTemperature.CELSIUS,
                )
            )



    async_add_entities(hass_thermia_numbers) 

