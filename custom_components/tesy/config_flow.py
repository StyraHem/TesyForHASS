"""Adds config flow for Shelly."""
# pylint: disable=dangerous-default-value
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import *

from homeassistant.const import (
    CONF_PASSWORD, CONF_USERNAME
)
from .configuration_schema import STEP_SCHEMA

_LOGGER = logging.getLogger(__name__)

class ShellyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HA"""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""

    async def async_step_user(self, user_input={}):
        return self.async_show_form(
            step_id='input',
            data_schema=STEP_SCHEMA
        )

    async def async_step_input(self, user_input={}):
        return self.async_create_entry(
            title=user_input["id_prefix"],
            data=user_input
        )

    async def async_step_import(self, user_input):
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        for entry in self._async_current_entries():
            if entry.source == "import":
                return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml",
                                       data=user_input)