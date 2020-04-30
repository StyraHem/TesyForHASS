"""
Tesy platform for the climate component.

#For more details about this platform, please refer to the documentation
#https://home-assistant.io/components/tesy/
"""

import logging

from homeassistant.const import (
    TEMP_CELSIUS,
    PRECISION_WHOLE,
    STATE_OFF,
    STATE_ON,
    TEMP_CELSIUS,
    ATTR_TEMPERATURE
)
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.components.water_heater import (WaterHeaterDevice, SUPPORT_OPERATION_MODE, SUPPORT_TARGET_TEMPERATURE)
from . import (TESY_DEVICES, TESY_CONFIG) #, get_device_from_hass)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STATES = {"OFF" : "off",
          "READY" : "on",
          "HEATING" : "heat"}

async def async_setup_entry(hass, _config_entry, async_add_entities):
    """Set up Tesy sensor dynamically."""
    async def async_discover_sensor(dev, instance):
        """Discover and add a discovered sensor."""
        async_add_entities([TesyWaterHeater(dev, instance)])

    async_dispatcher_connect(
        hass,
        "tesy_new_water_heater",
        async_discover_sensor
    )

# async def async_setup_platform(hass, _config, async_add_entities,
#                                discovery_info=None):
#     """Setup the Tesy Sensor platform."""
#     dev = get_device_from_hass(hass, discovery_info)
#     async_add_entities([TesyWaterHeater(dev, hass)])

class TesyWaterHeater(WaterHeaterDevice):
    """Representation of a Shelly Sensor."""

    def __init__(self, dev, instance):
        """Initialize an ShellySwitch."""
        self._unique_id = "tesy_" + dev.id
        self.entity_id = "water_heater.tesy_" + dev.id
        self._config = instance.conf
        self._dev = dev
        self._instance = instance
        dev.on_updated.append(self._updated)
        self._state = None

    def _updated(self, _dev):
        self.schedule_update_ha_state(True)

    @property
    def state(self):
        """Return the state of the sensor."""
        return STATES.get( self._dev.state, "unknown" )

    @property
    def precision(self):
        """Return the precision of the system."""
        return PRECISION_WHOLE

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_OPERATION_MODE | SUPPORT_TARGET_TEMPERATURE

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

    def set_operation_mode(self, operation_mode):
        if operation_mode == "on":
            self._dev.turn_on()
        else:
            self._dev.turn_off()

    @property
    def current_operation(self):
        """Return current operation ie. eco, electric, performance, ..."""
        if self._dev.state == "OFF":
            return "off"
        return "on"

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return ["on", "off"]

    @property
    def device_info(self):
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        return {
            'identifiers': {
                (DOMAIN, self._dev.id)
            },
            'name': self._dev.id,
            'manufacturer': 'Tesy',
            'model': "Heater",
            'sw_version': "0.1"
        }
