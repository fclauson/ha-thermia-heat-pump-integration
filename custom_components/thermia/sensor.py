"""Thermia sensor integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfTime, UnitOfPressure 
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import ThermiaDataUpdateCoordinator
from .sensors.active_alarms_sensor import ThermiaActiveAlarmsSensor
from .sensors.generic_sensor import ThermiaGenericSensor

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
    """Set up the Thermia sensors."""

    coordinator: ThermiaDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass_thermia_sensors = []

    for idx, heat_pump in enumerate(coordinator.data.heat_pumps):
        if heat_pump.heat_temperature:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Heat Target Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "heat_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if (
            heat_pump.is_outdoor_temp_sensor_functioning
            and heat_pump.outdoor_temperature is not None
        ):
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Outdoor Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "outdoor_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if (
            heat_pump.has_indoor_temp_sensor
            and heat_pump.indoor_temperature is not None
        ):
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Indoor Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "indoor_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if (
            heat_pump.is_hot_water_active
            and heat_pump.hot_water_temperature is not None
        ):
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Hot Water Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "hot_water_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        # Added by Francis 
        if heat_pump.lower_hot_water_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Lower Hot Water temp ",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "lower_hot_water_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )
            
        if heat_pump.weighted_hot_water_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Weighted Hot Water Temp",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "weighted_hot_water_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        ###########################################################################
        # Other temperature sensors
        ###########################################################################

        if heat_pump.supply_line_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Supply Line Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "supply_line_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if heat_pump.desired_supply_line_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Desired Supply Line Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "desired_supply_line_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if heat_pump.return_line_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Return Line Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "return_line_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if heat_pump.brine_out_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Brine Out Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "brine_out_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if heat_pump.brine_in_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Brine In Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "brine_in_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if heat_pump.cooling_tank_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Cooling Tank Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "cooling_tank_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if heat_pump.cooling_supply_line_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Cooling Supply Line Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "cooling_supply_line_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if heat_pump.buffer_tank_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Buffer Tank Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "buffer_tank_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )

        if heat_pump.pool_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Pool Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "pool_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )
       
        #####################################
        ## Only available if you have an installer login - Francis 26/03/2025
        #####################################
        if heat_pump.start_hot_water_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Start Hot Water Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "start_hot_water_temperature",
                    UnitOfTemperature.CELSIUS,
                )
            )
        

        ###########################################################################
        # Operational status data
        ###########################################################################

        if heat_pump.operational_status_integral is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Integral",
                    "mdi:math-integral",
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "measurement",
                    "operational_status_integral",
                    None,
                )
            )

        if heat_pump.operational_status_pid is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "PID",
                    "mdi:math-integral-box",
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "measurement",
                    "operational_status_pid",
                    None,
                )
            )

        ###########################################################################
        # Operational time data
        ###########################################################################

        if heat_pump.compressor_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Compressor Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "compressor_operational_time",
                    UnitOfTime.HOURS,
                )
            )

        if heat_pump.heating_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Heating Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "heating_operational_time",
                    UnitOfTime.HOURS,
                )
            )

        if heat_pump.hot_water_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Hot Water Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "hot_water_operational_time",
                    UnitOfTime.HOURS,
                )
            )

        if heat_pump.auxiliary_heater_1_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Auxiliary Heater 1 Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "auxiliary_heater_1_operational_time",
                    UnitOfTime.HOURS,
                )
            )

        if heat_pump.auxiliary_heater_2_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Auxiliary Heater 2 Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "auxiliary_heater_2_operational_time",
                    UnitOfTime.HOURS,
                )
            )

        if heat_pump.auxiliary_heater_3_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Auxiliary Heater 3 Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "auxiliary_heater_3_operational_time",
                    UnitOfTime.HOURS,
                )
            )
        ###########################################################################
        # Diagnostic data - added by Francis 
        ###########################################################################
        if heat_pump.evaporator_pressure is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Evaporator Pressure",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "measurement",
                    "evaporator_pressure",
                    UnitOfPressure.BAR, 
                )
            )
        if heat_pump.suction_temp is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Suction Temp",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "measurement",
                    "suction_temp",
                    UnitOfTemperature.CELSIUS, 
                )
            )
        if heat_pump.evaporator_temp is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Evaporator temp",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "measurement",
                    "evaporator_temp",
                    UnitOfTemperature.CELSIUS, 
                )
            )
        if heat_pump.super_heat is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Super Heat",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "measurement",
                    "super_heat",
                    UnitOfTemperature.CELSIUS, 
                )
            )
        if heat_pump.opening_degree is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Opening degree",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "measurement",
                    "opening_degree",
                    None, 
                )
            )

    hass_thermia_active_alarms_sensors = [
        ThermiaActiveAlarmsSensor(coordinator, idx)
        for idx, _ in enumerate(coordinator.data.heat_pumps)
    ]

    async_add_entities([*hass_thermia_active_alarms_sensors, *hass_thermia_sensors])

