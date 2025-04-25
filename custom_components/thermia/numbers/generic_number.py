"""Thermia Generic number integration."""

from __future__ import annotations

import logging

from homeassistant.components.number import NumberEnitity  
from homeassistant.helpers.update_coordinator import CoordinatorEntity


from ..const import DOMAIN
from ..coordinator import ThermiaDataUpdateCoordinator

from ThermiaOnlineAPI.const import (
    REG_GROUP_HEATING_CURVE,
    REG_DESIRED_DISTR_CIR1,
    REG_DESIRED_DISTR_CIR2,
    REG_HEATING_HEAT_CURVE,
    REG_HEATING_HEAT_CURVE_MIN,
    REG_HEATING_HEAT_CURVE_MAX,
    REG_HEATING_CURVE_PLUS5,
    REG_HEATING_CURVE_0,
    REG_HEATING_CURVE_MINUS5,
    REG_HEATING_HEAT_STOP,
    REG_HEATING_ROOM_FACTOR

)


_LOGGER = logging.getLogger(__name__)

class ThermiaGenericNumber(
    CoordinatorEntity[ThermiaDataUpdateCoordinator], NumberEntity
):   
    """Represents a generic number entity for Home Assistant."""

    def __init__(
        self, 
        coordinator, 
        idx,
        is_online_prop : str,
        number_name: str,
        mdi_icon : str, 
        entity_category: str,
        device_class: str | None,
        state_class : str, 
        value_prop: str,
        reg_name : str,
        unit_of_measurement=None,
          
    ):
        """
        Initializes a new GenericNumberEntity.
        """
        super().__init__(coordinator)
        self.idx: int = idx
        
        self._is_online_prop: str = is_online_prop
        self._number_name: str = number_name
        self._mdi_icon: str = mdi_icon
        self._entity_category: str = entity_category
        self._device_class: str | None = device_class
        self._state_class: str = state_class
        self._value_prop: str = value_prop
        self._reg_name : str = reg_name

        self._unit_of_measurement: str | None = unit_of_measurement
        # self.step: float step | None = step

        
    @property
    def available(self):
        """Return True if entity is available."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._is_online_prop)

    @property
    def name(self):
        """Return the name of the number."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name} {self._number_name}"

    @property
    def unique_id(self):
        """Return the unique ID of the number."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name}_{self._number_name.lower().replace(' ', '_')}"

    @property
    def icon(self):
        """Return the icon of the number."""
        return self._mdi_icon

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
    def entity_category(self):
        """Return the category of the number."""
        return self._entity_category

    @property
    def device_class(self):
        """Return the device class of the number."""
        return self._device_class

    @property
    def state_class(self):
        """Return the state class of the number."""
        return self._state_class

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of the number."""
        return self._unit_of_measurement

    ## Need a way of getting the value - which we have as this is the HC... call 
    @property
    def native_value(self):
        """Return value of the number."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._value_prop)

    # will use this to set the value 
    # def set_register_data_by_register_group_and_name(
    #    self, register_group: str, register_name: str, value: int
    # 

    async def async_set_value(self, value : float):
        """Set new target temperature."""
        _LOGGER.info("setting new setting  : %s", value)
        _LOGGER.info("idx: %s", self.idx)
        _LOGGER.info("value prop %s",self._value_prop) 

        await self.hass.async_add_executor_job(
            lambda: self.coordinator.data.heat_pumps[self.idx].set_register_data_by_register_group_and_name( 
                REG_GROUP_HEATING_CURVE, self._reg_name, value 
            )
        )

