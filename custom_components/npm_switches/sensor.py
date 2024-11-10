"""Sensor platform for integration_blueprint."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .entity import NpmSwitchesEntity
from . import NpmSwitchesUpdateCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    entities.append(NpmSwitchesProxySensor(coordinator, entry, "enabled"))
    entities.append(NpmSwitchesProxySensor(coordinator, entry, "disabled"))
    entities.append(NpmSwitchesRedirSensor(coordinator, entry, "enabled"))
    entities.append(NpmSwitchesRedirSensor(coordinator, entry, "disabled"))

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
        self._attr_icon = "mdi:steering"
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
        return self._attr_icon

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
        self._attr_icon = "mdi:steering"
        self.friendly_name = "NPM " + self.sensor_name.capitalize() + " Redirection Hosts"

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
        return self._attr_icon