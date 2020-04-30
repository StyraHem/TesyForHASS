"""
Support for Shelly smart home devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/shelly/
"""
#from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.const import (
    CONF_HOSTS, CONF_PASSWORD, CONF_SCAN_INTERVAL, CONF_USERNAME, 
    EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv


#REQUIREMENTS = ['pytesy==0.0.1']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'tesy'

TESY_DEVICES = 'tesy_devices'
TESY_HOSTS = 'tesy_hosts'
TESY_CONFIG = 'tesy_cfg'

TESY_DEVICE_ID = "tesy_device_id"

__version__ = "0.0.1"
VERSION = __version__

HOST_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOSTS,
                      default=[]): vol.All(cv.ensure_list, [HOST_SCHEMA])
    })
}, extra=vol.ALLOW_EXTRA)

HOSTS = []
DEVICES = {}

def _add_device_key(dev):
    key = dev.id
    if not key in DEVICES:
        DEVICES[key] = dev
    return key

def get_device_from_hass(hass, discovery_info):
    """Get device from HASS"""
    device_key = discovery_info[TESY_DEVICE_ID]
    return DEVICES[device_key]  

async def async_setup(hass, config):
    """Setup Tesy component"""
    _LOGGER.info("Starting tesy, %s", __version__)    

    conf = config.get(DOMAIN, {})
    #update_interval = conf.get(CONF_SCAN_INTERVAL)
    hass.data[TESY_CONFIG] = conf
    #discover = conf.get(CONF_DISCOVERY)

    #try:
    from .pytesy import PyTesy
    _LOGGER.info("Loading local pyTesy")
    #except ImportError:
    #    from pytesy import pyTesy

    hass.data[TESY_HOSTS] = HOSTS
    hass.data[TESY_DEVICES] = DEVICES

    #_LOGGER.info("pyTesy, %s", tesy.version())

    def device_added(device):
        key = _add_device_key(device)
        _LOGGER.info("Test device added {}", key)
        attr = {TESY_DEVICE_ID : key}
        discovery.load_platform(hass, 'water_heater', DOMAIN, attr, config)

    for host in conf[CONF_HOSTS]:
         tesy = PyTesy(host[CONF_USERNAME], host[CONF_PASSWORD])         
         tesy.on_device_added.append(device_added)
         HOSTS.append(tesy)
         tesy.start(5)

    # def stop_tesy():
    #     """Stop Tesy."""
    #     _LOGGER.info("Shutting down Tesy")
    #     #.close()

    #hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_tesy)

    return True
