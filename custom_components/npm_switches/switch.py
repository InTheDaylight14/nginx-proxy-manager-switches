"""Switch platform for integration_blueprint."""
import logging
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.util import slugify

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
    stream_hosts = await api.get_stream_hosts()
    dead_hosts = await api.get_dead_hosts()
    entities = []

    if entry.data["include_proxy_hosts"]:
        for proxy_host in proxy_hosts.values():
            entities.append(NpmProxyBinarySwitch(coordinator, entry, proxy_host))
    if entry.data["include_redirection_hosts"]:
        for redir_host in redir_hosts.values():
            entities.append(NpmRedirBinarySwitch(coordinator, entry, redir_host))
    if entry.data["include_stream_hosts"]:
        for stream_host in stream_hosts.values():
            entities.append(NpmStreamBinarySwitch(coordinator, entry, stream_host))
    if entry.data["include_dead_hosts"]:
        for dead_host in dead_hosts.values():
            entities.append(NpmDeadBinarySwitch(coordinator, entry, dead_host))

    async_add_entities(entities, True)
    # async_add_devices([NpmProxyBinarySwitch(coordinator, entry, "20")])


class NpmProxyBinarySwitch(NpmSwitchesEntity, SwitchEntity):
    """Switches to enable/disable the Proxy Host Type in NPM"""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        host: dict,
    ) -> None:
        """Initialize proxy switch entity."""
        super().__init__(coordinator, entry)
        self.host = host
        self.name = "Proxy " + self.host["domain_names"][0].replace(".", " ").capitalize()
        self.entity_id = "switch."+slugify(f"{entry.title} {self.name}")
        self._attr_unique_id = f"{entry.entry_id} {self.name}"
        self.host_id = str(host["id"])
        self.host_type = "proxy-hosts"

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.enable_host(self.host_id, self.host_type)
        self.async_write_ha_state()
        self.host = await self.coordinator.api.get_host(self.host_id, self.host_type)

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.disable_host(self.host_id, self.host_type)
        self.async_write_ha_state()
        self.host = await self.coordinator.api.get_host(self.host_id, self.host_type)

    # @property
    # def name(self):
    #     """Return the name of the switch."""
    #     return "NPM " + self.host["domain_names"][0].replace(".", " ").capitalize()

    @property
    def icon(self):
        """Return the icon of this switch."""
        if self.coordinator.api.is_host_enabled(self.host_id, self.host_type):
            return "mdi:check-network"
        return "mdi:close-network"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.api.is_host_enabled(self.host_id, self.host_type)

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "id": self.host["id"],
            "domain_names": self.host["domain_names"],
        }

class NpmRedirBinarySwitch(NpmSwitchesEntity, SwitchEntity):
    """Switches to enable/disable the Redir Host Type in NPM"""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        host: dict,
    ) -> None:
        """Initialize redir switch entity."""
        super().__init__(coordinator, entry)
        self.host = host
        self.name = "Redirect " + self.host["domain_names"][0].replace(".", " ").capitalize()
        self.entity_id = "switch."+slugify(f"{entry.title} {self.name}")
        self._attr_unique_id = f"{entry.entry_id} {self.name}"
        self.host_type = "redirection-hosts"
        self.host_id = str(host["id"])

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.enable_host(self.host_id, self.host_type)
        self.async_write_ha_state()
        self.host = await self.coordinator.api.get_host(self.host_id, self.host_type)

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.disable_host(self.host_id, self.host_type)
        self.async_write_ha_state()
        self.host = await self.coordinator.api.get_host(self.host_id, self.host_type)

    @property
    def icon(self):
        """Return the icon of this switch."""
        if self.coordinator.api.is_host_enabled(self.host_id, self.host_type):
            return "mdi:check-network"
        return "mdi:close-network"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.api.is_host_enabled(self.host_id, self.host_type)

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "id": self.host["id"],
            "domain_names": self.host["domain_names"],
            # "forward_domain_name": self.host["forward_domain_names"],
        }

class NpmStreamBinarySwitch(NpmSwitchesEntity, SwitchEntity):
    """Switches to enable/disable the Redir Host Type in NPM"""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        host: dict,
    ) -> None:
        """Initialize steam switch entity."""
        super().__init__(coordinator, entry)
        self.host = host
        self.name = "Stream " + str(self.host["incoming_port"])
        self.entity_id = "switch."+slugify(f"{entry.title} {self.name}")
        self._attr_unique_id = f"{entry.entry_id} {self.name}"
        self.host_type = "streams"
        self.host_id = str(host["id"])

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.enable_host(self.host_id, self.host_type)
        self.async_write_ha_state()
        self.host = await self.coordinator.api.get_host(self.host_id, self.host_type)

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.disable_host(self.host_id, self.host_type)
        self.async_write_ha_state()
        self.host = await self.coordinator.api.get_host(self.host_id, self.host_type)

    @property
    def icon(self):
        """Return the icon of this switch."""
        if self.coordinator.api.is_host_enabled(self.host_id, self.host_type):
            return "mdi:check-network"
        return "mdi:close-network"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.api.is_host_enabled(self.host_id, self.host_type)

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "id": self.host["id"],
            "forwarding_host": self.host["forwarding_host"],
            "forwarding_port": self.host["forwarding_port"],
            # "forward_domain_name": self.host["forward_domain_names"],
        }

class NpmDeadBinarySwitch(NpmSwitchesEntity, SwitchEntity):
    """Switches to enable/disable the Dead Host Type in NPM"""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        host: dict,
    ) -> None:
        """Initialize redir switch entity."""
        super().__init__(coordinator, entry)
        self.host = host
        self.name = "404 " + self.host["domain_names"][0].replace(".", " ").capitalize()
        self.entity_id = "switch."+slugify(f"{entry.title} {self.name}")
        self._attr_unique_id = f"{entry.entry_id} {self.name}"
        self.host_type = "dead-hosts"
        self.host_id = str(host["id"])

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.enable_host(self.host_id, self.host_type)
        self.async_write_ha_state()
        self.host = await self.coordinator.api.get_host(self.host_id, self.host_type)

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.disable_host(self.host_id, self.host_type)
        self.async_write_ha_state()
        self.host = await self.coordinator.api.get_host(self.host_id, self.host_type)

    @property
    def icon(self):
        """Return the icon of this switch."""
        if self.coordinator.api.is_host_enabled(self.host_id, self.host_type):
            return "mdi:check-network"
        return "mdi:close-network"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.api.is_host_enabled(self.host_id, self.host_type)

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "id": self.host["id"],
            "domain_names": self.host["domain_names"],
            # "forward_domain_name": self.host["forward_domain_names"],
        }