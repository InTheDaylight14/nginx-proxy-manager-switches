"""Switch platform for integration_blueprint."""
import logging
from homeassistant.components.switch import SwitchEntity

# from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .entity import NpmSwitchesEntity
from . import NpmSwitchesUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    api = hass.data[DOMAIN][entry.entry_id].api
    proxy_hosts = await api.get_proxy_hosts()
    redir_hosts = await api.get_redirection_hosts()
    entities = []

    for proxy in proxy_hosts.values():
        entities.append(NpmProxyBinarySwitch(coordinator, entry, proxy))

    for redir in redir_hosts.values():
        entities.append(NpmRedirBinarySwitch(coordinator, entry, redir))

    async_add_entities(entities, True)
    # async_add_devices([NpmProxyBinarySwitch(coordinator, entry, "20")])


class NpmProxyBinarySwitch(NpmSwitchesEntity, SwitchEntity):
    """Switches to enable/disable the Proxy Host Type in NPM"""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        proxy: dict,
    ) -> None:
        """Initialize proxy switch entity."""
        super().__init__(coordinator, entry)
        self.proxy = proxy
        self.proxy_id = str(proxy["id"])
        self.host_type = "proxy-hosts"
        self.friendly_name = (
            "NPM " + self.proxy["domain_names"][0].replace(".", " ").capitalize()
        )

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.enable_host(self.proxy_id, "proxy-hosts")
        self.async_write_ha_state()
        self.proxy = await self.coordinator.api.get_host(self.proxy_id, self.host_type)

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.disable_host(self.proxy_id, "proxy-hosts")
        self.async_write_ha_state()
        self.proxy = await self.coordinator.api.get_host(self.proxy_id, self.host_type)

    # @property
    # def name(self):
    #     """Return the name of the switch."""
    #     return "NPM " + self.proxy["domain_names"][0].replace(".", " ").capitalize()

    @property
    def icon(self):
        """Return the icon of this switch."""
        if self.coordinator.api.is_host_enabled(self.proxy_id, self.host_type):
            return "mdi:check-network"
        return "mdi:close-network"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.api.is_host_enabled(self.proxy_id, self.host_type)

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "id": self.proxy["id"],
            "domain_names": self.proxy["domain_names"],
        }

class NpmRedirBinarySwitch(NpmSwitchesEntity, SwitchEntity):
    """Switches to enable/disable the Redir Host Type in NPM"""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        proxy: dict,
    ) -> None:
        """Initialize proxy switch entity."""
        super().__init__(coordinator, entry)
        self.proxy = proxy
        self.host_type = "redirection-hosts"
        self.proxy_id = str(proxy["id"])
        self.friendly_name = (
            "NPM Redir " + self.proxy["domain_names"][0].replace(".", " ").capitalize()
        )

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.enable_host(self.proxy_id, "redirection-hosts")
        self.async_write_ha_state()
        self.proxy = await self.coordinator.api.get_host(self.proxy_id, self.host_type)

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.disable_host(self.proxy_id, "redirection-hosts")
        self.async_write_ha_state()
        self.proxy = await self.coordinator.api.get_host(self.proxy_id, self.host_type)

    # @property
    # def name(self):
    #     """Return the name of the switch."""
    #     return "NPM " + self.proxy["domain_names"][0].replace(".", " ").capitalize()

    @property
    def icon(self):
        """Return the icon of this switch."""
        if self.coordinator.api.is_host_enabled(self.proxy_id, self.host_type):
            return "mdi:check-network"
        return "mdi:close-network"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.api.is_host_enabled(self.proxy_id, self.host_type)

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "id": self.proxy["id"],
            "domain_names": self.proxy["domain_names"],
            # "forward_domain_name": self.proxy["forward_domain_names"],
        }