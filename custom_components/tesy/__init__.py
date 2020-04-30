"""
Support for Shelly smart home devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/shelly/
"""
#from datetime import timedelta
import logging

from homeassistant.const import (
    CONF_HOSTS, CONF_PASSWORD, CONF_SCAN_INTERVAL, CONF_USERNAME,
    EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers import discovery
from homeassistant import config_entries
from .const import *
from .configuration_schema import (CONFIG_SCHEMA_ROOT)
from homeassistant.helpers.dispatcher import async_dispatcher_send
import asyncio

REQUIREMENTS = ['pytesy==0.0.3']

_LOGGER = logging.getLogger(__name__)

__version__ = "0.0.2"
VERSION = __version__

async def async_setup(hass, config):
    """Set up this integration using yaml."""
    if DOMAIN not in config:
        return True
    data = dict(config.get(DOMAIN))
    hass.data["yaml_tesy"] = data
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data={}
        )
    )
    return True

async def async_setup_entry(hass, config_entry):
    """Setup Tesy component"""

    _LOGGER.info("Starting tesy, %s", __version__)

    if not DOMAIN in hass.data:
        hass.data[DOMAIN] = {}

    if config_entry.source == "import":
        #if config_entry.options: #config.yaml
        #    data = config_entry.options.copy()
        #else:
        if "yaml_tesy" in hass.data:
            data = hass.data["yaml_tesy"]
        else:
            data = {}
            await hass.config_entries.async_remove(config_entry.entry_id)
    else:
        data = config_entry.data.copy()
        data.update(config_entry.options)

    conf = CONFIG_SCHEMA_ROOT(data)

    hass.data[DOMAIN][config_entry.entry_id] = \
        TesyInstance(hass, config_entry, conf)

    return True

class TesyInstance():
    def __init__(self, hass, config_entry, conf):
        self.hass = hass
        self.config_entry = config_entry
        self.conf = conf
        self.platforms = {}

        _LOGGER.info("Starting tesy, %s", __version__)

        hass.loop.create_task(
            self.start_up()
        )

    def device_added(self, device):
        self.hass.add_job(self._async_add_device("water_heater", device))

    async def _async_add_device(self, platform, device):
        if platform not in self.platforms:
            self.platforms[platform] = asyncio.Event()
            await self.hass.config_entries.async_forward_entry_setup(
                    self.config_entry, platform)
            self.platforms[platform].set()

        await self.platforms[platform].wait()
        async_dispatcher_send(self.hass, "tesy_new_" + platform \
                                , device, self)

    async def start_up(self):
        conf = self.conf

        try:
            from .pytesy import PyTesy
            _LOGGER.info("Loading local pyTesy")
        except ImportError:
            from pyTesy import pyTesy

        tesy = PyTesy(conf[CONF_USERNAME], conf[CONF_PASSWORD])
        tesy.on_device_added.append(self.device_added)
        self.pyTesy = tesy
        tesy.start(5)

        _LOGGER.info("pyTesy, %s", tesy.version)

    # def stop_tesy():
    #     """Stop Tesy."""
    #     _LOGGER.info("Shutting down Tesy")
    #     #.close()

    #hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_tesy)

    #return True
