from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging

from .const import DOMAIN, REG_GROUP_HEATING_CURVE
from .coordinator import ThermiaDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class ThermiaGenericNumber(
    CoordinatorEntity[ThermiaDataUpdateCoordinator], NumberEntity
):
    """Represents a generic number entity for Home Assistant."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ThermiaDataUpdateCoordinator,
        idx: int,
        is_online_prop: str,
        number_name: str,
        mdi_icon: str,
        entity_category: EntityCategory | None,
        device_class: NumberDeviceClass | None,
        state_class: NumberStateClass | None,
        value_prop: str,
        reg_name: str,
        native_unit_of_measurement: str | None = None,
        native_max_value: float | None = None,
        native_min_value: float | None = None,
        native_step: float | None = None,
    ) -> None:
        """
        Initializes a new GenericNumberEntity.
        """
        super().__init__(coordinator)
        self.idx: int = idx

        self._is_online_prop: str = is_online_prop
        self._number_name: str = number_name
        self._mdi_icon: str = mdi_icon
        self._entity_category: EntityCategory | None = entity_category
        self._device_class: NumberDeviceClass | None = device_class
        self._state_class: NumberStateClass | None = state_class
        self._value_prop: str = value_prop
        self._reg_name: str = reg_name
        self._native_max_value: float | None = native_max_value
        self._native_min_value: float | None = native_min_value
        self._native_step: float | None = native_step

        self._attr_native_unit_of_measurement: str | None = native_unit_of_measurement

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._is_online_prop)

    @property
    def name(self) -> str:
        """Return the name of the number."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name} {self._number_name}"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the number."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name}_{self._number_name.lower().replace(' ', '_')}"

    @property
    def icon(self) -> str | None:
        """Return the icon of the number."""
        return self._mdi_icon

    @property
    def device_info(self) -> dict:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.data.heat_pumps[self.idx].id)},
            "name": self.coordinator.data.heat_pumps[self.idx].name,
            "manufacturer": "Thermia",
            "model": self.coordinator.data.heat_pumps[self.idx].model,
            "model_id": self.coordinator.data.heat_pumps[self.idx].model_id,
        }

    @property
    def entity_category(self) -> EntityCategory | None:
        """Return the category of the number."""
        return self._entity_category

    @property
    def device_class(self) -> NumberDeviceClass | None:
        """Return the device class of the number."""
        return self._device_class

    @property
    def state_class(self) -> NumberStateClass | None:
        """Return the state class of the number."""
        return self._state_class

    @property
    def native_value(self) -> float | None:
        """Return value of the number."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._value_prop)

    @property
    def native_min_value(self) -> float | None:
        """Return the minimum value."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._native_min_value)

    @property
    def native_max_value(self) -> float | None:
        """Return the maximum value."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._native_max_value)

    @property
    def native_step(self) -> float | None:
        """Return the step value."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._native_step)

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        _LOGGER.debug("Setting new setting: %s for %s", value, self._number_name)
        _LOGGER.debug("Index: %s", self.idx)

        await self.hass.async_add_executor_job(
            lambda: self.coordinator.data.heat_pumps[
                self.idx
            ].set_register_data_by_register_group_and_name(
                REG_GROUP_HEATING_CURVE, self._reg_name, value
            )
        )
        await self.coordinator.async_request_refresh()

