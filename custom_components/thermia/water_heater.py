"""Thermia water heater class."""

from __future__ import annotations

import logging

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ThermiaDataUpdateCoordinator


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Thermia water heater."""

    coordinator: ThermiaDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    # code recongigured so that the new StartWaterHeater can be added - Francis 
    
    hass_water_heaters = [] 
    for idx in range(len(coordinator.data.heat_pumps)) :
        hass_water_heaters.append(ThermiaWaterHeater(coordinator, idx))
        hass_water_heaters.append(StartWaterHeater(coordinator, idx))
    
    async_add_entities(hass_water_heaters)
    
###########################################
# Francis - new device which allows for the control of hot water 
# requires user to have installer priverlidges on their login so that they can see more parameters from the Thermia 

class StartWaterHeater ( CoordinatorEntity[ThermiaDataUpdateCoordinator], WaterHeaterEntity
):
    def __init__(self, coordinator: ThermiaDataUpdateCoordinator, idx: int):
        super().__init__(coordinator)
        self.idx = idx
        
    @property
    def name(self):
        """Return the name of the water heater."""
        return "StartWaterHeater" 

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self.coordinator.data.heat_pumps[self.idx].id + "A"
        
    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:water-pump"

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return 30

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return 60
    @property
    def current_operation(self):
        """Return the unit of measurement."""
        return "watching"

    @property
    def target_temperature(self):
        """Return the start temp setting."""
        ## this will be the start temp value 
        return self.coordinator.data.heat_pumps[self.idx].start_hot_water_temperature
        
    @property
    def current_temperature(self):
        """Return the currnt temp of tank."""
        ## this will be the current tank temprature 
        return self.coordinator.data.heat_pumps[self.idx].hot_water_temperature

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def supported_features(self):
        """Return the list of supported features."""
        features = WaterHeaterEntityFeature.TARGET_TEMPERATURE
        return features

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        _LOGGER.info("start water target temperature update : %s", target_temp)
        if target_temp is not None:
            await self.hass.async_add_executor_job(
                lambda: self.coordinator.data.heat_pumps[self.idx].set_hot_water_start_temperature(
                    target_temp
                )
            )
        else:
            _LOGGER.error("A target temperature must be provided")
    
    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.data.heat_pumps[self.idx].id)},
            "name": self.coordinator.data.heat_pumps[self.idx].name,
            "manufacturer": "Thermia",
            "model": self.coordinator.data.heat_pumps[self.idx].model,
            "model_id": self.coordinator.data.heat_pumps[self.idx].model_id,
        }

    
################################################
# Francis - this is the original water heater - it controls the ROOM temprature setting 
# 
class ThermiaWaterHeater(
    CoordinatorEntity[ThermiaDataUpdateCoordinator], WaterHeaterEntity
):
    """Representation of an Thermia water heater."""

    def __init__(self, coordinator: ThermiaDataUpdateCoordinator, idx: int):
        super().__init__(coordinator)
        self.idx = idx

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.data.heat_pumps[self.idx].is_online

    @property
    def name(self):
        """Return the name of the water heater."""
        return self.coordinator.data.heat_pumps[self.idx].name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self.coordinator.data.heat_pumps[self.idx].id 

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:water-pump"

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.data.heat_pumps[self.idx].id)},
            "name": self.coordinator.data.heat_pumps[self.idx].name,
            "manufacturer": "Thermia",
            "model": self.coordinator.data.heat_pumps[self.idx].model,
            "model_id": self.coordinator.data.heat_pumps[self.idx].model_id,
        }

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        default_min_temp = 0

        if not self.available:
            return default_min_temp

        min_temp = self.coordinator.data.heat_pumps[self.idx].heat_min_temperature_value
        
        ## Min temp hard coded by Francis 
        min_temp = 18 
        
        if min_temp is not None:
            return min_temp
        return default_min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        default_max_temp = 50

        if not self.available:
            return default_max_temp

        max_temp = self.coordinator.data.heat_pumps[self.idx].heat_max_temperature_value
        
        ## max temp hard coded by Francis 
        max_temp = 24
        
        if max_temp is not None:
            return max_temp
        return default_max_temp

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self.coordinator.data.heat_pumps[self.idx].indoor_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self.coordinator.data.heat_pumps[self.idx].heat_temperature

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def current_operation(self):
        """Return current operation ie. eco, off, etc."""
        return self.coordinator.data.heat_pumps[self.idx].operation_mode

    @property
    def operation_list(self):
        """List of available operation modes."""
        return self.coordinator.data.heat_pumps[self.idx].available_operation_modes

    @property
    def supported_features(self):
        """Return the list of supported features."""
        features = WaterHeaterEntityFeature.TARGET_TEMPERATURE

        if (
            self.current_operation is not None
            and self.coordinator.data.heat_pumps[self.idx].is_operation_mode_read_only
            is False
        ):
            features |= WaterHeaterEntityFeature.OPERATION_MODE

        return features

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is not None:
            await self.hass.async_add_executor_job(
                lambda: self.coordinator.data.heat_pumps[self.idx].set_temperature(
                    target_temp
                )
            )
        else:
            _LOGGER.error("A target temperature must be provided")

    async def async_set_operation_mode(self, operation_mode):
        """Set operation mode."""
        if operation_mode is not None:
            await self.hass.async_add_executor_job(
                lambda: self.coordinator.data.heat_pumps[self.idx].set_operation_mode(
                    operation_mode
                )
            )
        else:
            _LOGGER.error("An operation mode must be provided")
