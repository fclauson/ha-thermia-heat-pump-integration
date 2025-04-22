from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.number import NumberEntity, NumberDeviceClass

from .const import DOMAIN
from .coordinator import ThermiaDataUpdateCoordinator

class ThermiaGenericSensor(
    CoordinatorEntity[ThermiaDataUpdateCoordinator], SensorEntity
    
class ThermiaGenericNumberEntity:
    """Represents a generic number entity for Home Assistant."""

    def __init__(self, name, coordinator, unique_id, initial_value=0, min_value=None, max_value=None, step=None, unit_of_measurement=None, device_class=None):
        """
        Initializes a new GenericNumberEntity.

        Args:
            name (str): The friendly name of the entity.
            coordinator 
            unique_id (str): A unique identifier for the entity.
            initial_value (float, optional): The initial value of the number. Defaults to 0.
            min_value (float, optional): The minimum allowed value. Defaults to None.
            max_value (float, optional): The maximum allowed value. Defaults to None.
            step (float, optional): The step increment for the number. Defaults to None.
            unit_of_measurement (str, optional): The unit of measurement. Defaults to None.
            device_class (str, optional): The device class of the number entity (e.g., temperature, humidity). Defaults to None.
        """
        super().__init__(coordinator)
        self.idx: int = idx
        
        self._name = name
        self._unique_id = unique_id
        self._state = initial_value
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._unit_of_measurement = unit_of_measurement
        self._device_class = device_class
        self._callbacks = []  # List to store callbacks for state changes

    @property
    def name(self):
        """Return the friendly name of the entity."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the entity."""
        return self._unique_id

    @property
    def state(self):
        """Return the current state of the entity."""
        return self._state

    @property
    def min_value(self):
        """Return the minimum value of the number."""
        return self._min_value

    @property
    def max_value(self):
        """Return the maximum value of the number."""
        return self._max_value

    @property
    def step(self):
        """Return the step increment of the number."""
        return self._step

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the entity."""
        return self._unit_of_measurement

    @property
    def device_class(self):
        """Return the device class of the entity."""
        return self._device_class

    def set_value(self, new_value):
        """Set the new value of the entity and notify listeners."""
        try:
            new_value = float(new_value)
            if self._min_value is not None and new_value < self._min_value:
                self._state = self._min_value
            elif self._max_value is not None and new_value > self._max_value:
                self._state = self._max_value
            else:
                self._state = new_value
            self._notify_callbacks()
        except ValueError:
            print(f"Invalid value: {new_value}. Must be a number.")

    def register_callback(self, callback):
        """Register a callback function to be called when the state changes."""
        self._callbacks.append(callback)

    def _notify_callbacks(self):
        """Notify all registered callback functions about the state change."""
        for callback in self._callbacks:
            callback(self._state)
