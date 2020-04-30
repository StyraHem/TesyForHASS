"""
Tesy platform for the climate component.

#For more details about this platform, please refer to the documentation
#https://home-assistant.io/components/te/
"""

import logging

from homeassistant.const import (TEMP_CELSIUS, STATE_OFF, STATE_ON, TEMP_CELSIUS, ATTR_TEMPERATURE)
#                                 DEVICE_CLASS_TEMPERATURE,
#                                 TEMP_CELSIUS, POWER_WATT)
#from homeassistant.const import (
#    ATTR_TEMPERATURE, PRECISION_TENTHS, PRECISION_WHOLE, SERVICE_TURN_OFF,
#    SERVICE_TURN_ON, STATE_OFF, STATE_ON, TEMP_CELSIUS)
from homeassistant.components.climate.const import (SUPPORT_TARGET_TEMPERATURE, HVAC_MODE_HEAT, HVAC_MODE_OFF)
#    ATTR_PRESET_MODE, CURRENT_HVAC_COOL, CURRENT_HVAC_HEAT, CURRENT_HVAC_IDLE,
#    CURRENT_HVAC_OFF, HVAC_MODE_COOL, HVAC_MODE_HEAT, HVAC_MODE_OFF,
#    PRESET_AWAY, SUPPORT_PRESET_MODE, SUPPORT_TARGET_TEMPERATURE, PRESET_NONE)

#from homeassistant.helpers.entity import Entity
from homeassistant.components.climate import ClimateDevice

from . import (TESY_DEVICES, TESY_CONFIG, get_device_from_hass)

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Setup the Tesy Sensor platform."""
    dev = get_device_from_hass(hass, discovery_info)
    async_add_entities([TesyClimate(dev, hass)])

class TesyClimate(ClimateDevice):
    """Representation of a Shelly Sensor."""

    def __init__(self, dev, hass):
        """Initialize an ShellySwitch."""
        self._unique_id = "tesy_" + dev.id
        self.entity_id = "climate.tesy_" + dev.id
        self._config = hass.data[TESY_CONFIG]
        self._dev = dev
        dev.on_updated.append(self._updated)

        self._state = None
        #self.update()

    def _updated(self, dev):
        self.schedule_update_ha_state(True)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._dev.state

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE 

    @property
    def current_temperature(self):
        """Return the sensor temperature."""
        return self._dev.temp

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._dev.target_temp

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return 15

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return 75

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        self._dev.set_temp(temperature)
        #await self._async_control_heating(force=True)
        #await self.async_update_ha_state()

    @property
    def target_temperature_step(self):# -> Optional[float]:
        """Return the supported step of target temperature."""
        return 1

    @property
    def hvac_modes(self):
        """List of available operation modes."""
        return [HVAC_MODE_HEAT, HVAC_MODE_OFF]
        