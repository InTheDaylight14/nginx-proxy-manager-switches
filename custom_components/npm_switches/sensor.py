"""Sensor platform for NPM Switches."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .entity import NpmSwitchesEntity
from . import NpmSwitchesUpdateCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    if entry.data["include_enable_disable_count_sensors"]:
        if entry.data["include_proxy_hosts"]:
            entities.append(NpmSwitchesProxySensor(coordinator, entry, "enabled"))
            entities.append(NpmSwitchesProxySensor(coordinator, entry, "disabled"))
        if entry.data["include_redirection_hosts"]:
            entities.append(NpmSwitchesRedirSensor(coordinator, entry, "enabled"))
            entities.append(NpmSwitchesRedirSensor(coordinator, entry, "disabled"))
        # if entry.data["include_stream_hosts"]:
        #     entities.append(NpmSwitchesStreamSensor(coordinator, entry, "enabled"))
        #     entities.append(NpmSwitchesStreamSensor(coordinator, entry, "disabled"))
        # if entry.data["include_dead_hosts"]:
        #     entities.append(NpmSwitchesDeadSensor(coordinator, entry, "enabled"))
        #     entities.append(NpmSwitchesDeadSensor(coordinator, entry, "disabled"))

    async_add_entities(entities, True)


class NpmSwitchesProxySensor(NpmSwitchesEntity, SensorEntity):
    """NPM Switches Proxy Sensor class."""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        name: str,
    ) -> None:
        """Initialize proxy switch entity."""
        super().__init__(coordinator, entry)
        self.proxy_id = name  # Unique ID relies on self.proxy_id
        self.sensor_name = self.proxy_id
        self.friendly_name = "NPM " + self.sensor_name.capitalize() + " Proxy Hosts"

    # @property
    # def name(self):
    #     """Return the name of the sensor."""
    #     return "npm_" + self.sensor_name + "_proxy_hosts"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if self.sensor_name == "enabled":
            return self.coordinator.api.num_proxy_enabled
        return self.coordinator.api.num_proxy_disabled

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:counter"

class NpmSwitchesRedirSensor(NpmSwitchesEntity, SensorEntity):
    """NPM Switches Redir Sensor class."""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        name: str,
    ) -> None:
        """Initialize proxy switch entity."""
        super().__init__(coordinator, entry)
        self.redir_id = name  # Unique ID relies on self.redir_id
        self.sensor_name = self.redir_id
        self.friendly_name = "NPM Redirection Hosts " + self.sensor_name.capitalize()

    # @property
    # def name(self):
    #     """Return the name of the sensor."""
    #     return "npm_" + self.sensor_name + "_proxy_hosts"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if self.sensor_name == "enabled":
            return self.coordinator.api.num_redir_enabled
        return self.coordinator.api.num_redir_disabled

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:counter"