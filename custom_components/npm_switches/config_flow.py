"""Adds config flow for Blueprint."""
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import voluptuous as vol

from .api import NpmSwitchesApiClient
from .const import (
    CONF_NPM_URL,
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
    PLATFORMS,
    CONF_INDLUDE_PROXY,
    CONF_INCLUDE_REDIR,
    CONF_INCLUDE_STREAMS,
    CONF_INCLUDE_DEAD,
    CONF_INCLUDE_SENSORS,
    DEFAULT_INDLUDE_PROXY,
    DEFAULT_INCLUDE_REDIR,
    DEFAULT_INCLUDE_STREAMS,
    DEFAULT_INCLUDE_DEAD,
    DEFAULT_INCLUDE_SENSORS,
)


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self.clean_npm_url = None

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            scheme_end = user_input[CONF_NPM_URL].find("://")+3
            self.clean_npm_url = user_input[CONF_NPM_URL][scheme_end:]

            # existing_entry = self._async_entry_for_username(user_input[CONF_NPM_URL])
            existing_entry = self._async_entry_for_username(self.clean_npm_url)
            # if existing_entry and not self.reauth:
            if existing_entry:
                return self.async_abort(reason="already_configured")

            valid = await self._test_credentials(
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
                user_input[CONF_NPM_URL],
            )
            if valid:
                return self.async_create_entry(
                    title=self.clean_npm_url, data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_USERNAME] = ""
        user_input[CONF_PASSWORD] = ""
        user_input[CONF_NPM_URL] = "http://"

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BlueprintOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=user_input[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                    vol.Required(CONF_NPM_URL, default=user_input[CONF_NPM_URL]): str,
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password, npm_url):
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = NpmSwitchesApiClient(username, password, npm_url, session)
            await client.async_get_new_token()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False

    @callback
    def _async_entry_for_username(self, username):
        """Find an existing entry for a username."""
        for entry in self._async_current_entries():
            # if entry.data.get(CONF_NPM_URL) == username:
            if entry.title == username:
                return entry
        return None


class BlueprintOptionsFlowHandler(config_entries.OptionsFlow):
    """Blueprint config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema = vol.Schema(
                {
                    vol.Optional(
                        CONF_INDLUDE_PROXY,
                        default=self.config_entry.options.get(
                            CONF_INDLUDE_PROXY, DEFAULT_INDLUDE_PROXY
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_INCLUDE_REDIR,
                        default=self.config_entry.options.get(
                            CONF_INCLUDE_REDIR, DEFAULT_INCLUDE_REDIR
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_INCLUDE_STREAMS,
                        default=self.config_entry.options.get(
                            CONF_INCLUDE_STREAMS, DEFAULT_INCLUDE_STREAMS
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_INCLUDE_DEAD,
                        default=self.config_entry.options.get(
                            CONF_INCLUDE_DEAD, DEFAULT_INCLUDE_DEAD
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_INCLUDE_SENSORS,
                        default=self.config_entry.options.get(
                            CONF_INCLUDE_SENSORS, DEFAULT_INCLUDE_SENSORS
                        ),
                    ): bool,
                }
            )
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
