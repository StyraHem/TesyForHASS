import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .const import ( DOMAIN )
from homeassistant.const import (
    CONF_PASSWORD, CONF_USERNAME
)

STEP_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

CONFIG_SCHEMA_ROOT = vol.Schema({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: CONFIG_SCHEMA_ROOT
}, extra=vol.ALLOW_EXTRA)
