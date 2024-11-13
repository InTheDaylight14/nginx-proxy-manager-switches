"""Sensor platform for NPM Switches."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import slugify

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
        if entry.data["include_stream_hosts"]:
            entities.append(NpmSwitchesStreamSensor(coordinator, entry, "enabled"))
            entities.append(NpmSwitchesStreamSensor(coordinator, entry, "disabled"))
        if entry.data["include_dead_hosts"]:
            entities.append(NpmSwitchesDeadSensor(coordinator, entry, "enabled"))
            entities.append(NpmSwitchesDeadSensor(coordinator, entry, "disabled"))

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
        self.host_id = name
        self.sensor_name = self.host_id
        self.name = "Proxy Hosts " + self.sensor_name.capitalize()
        self.entity_id = "sensor."+slugify(f"{entry.title} {self.name}")
        self._attr_unique_id = f"{entry.entry_id} {self.name}"

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
        self.host_id = name
        self.sensor_name = self.host_id
        self.name = "Redirection Hosts " + self.sensor_name.capitalize()
        self.entity_id = "sensor." + slugify(f"{entry.title} {self.name}")
        self._attr_unique_id = f"{entry.entry_id} {self.name}"

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

class NpmSwitchesStreamSensor(NpmSwitchesEntity, SensorEntity):
    """NPM Switches Stream Sensor class."""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        name: str,
    ) -> None:
        """Initialize proxy switch entity."""
        super().__init__(coordinator, entry)
        self.host_id = name
        self.sensor_name = self.host_id
        self.name = "Stream Hosts " + self.sensor_name.capitalize()
        self.entity_id = "sensor."+slugify(f"{entry.title} {self.name}")
        self._attr_unique_id = f"{entry.entry_id} {self.name}"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if self.sensor_name == "enabled":
            return self.coordinator.api.num_stream_enabled
        return self.coordinator.api.num_stream_disabled

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:counter"

class NpmSwitchesDeadSensor(NpmSwitchesEntity, SensorEntity):
    """NPM Switches Deam Sensor class."""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        name: str,
    ) -> None:
        """Initialize proxy switch entity."""
        super().__init__(coordinator, entry)
        self.host_id = name
        self.sensor_name = self.host_id
        self.name = "404 Hosts " + self.sensor_name.capitalize()
        self.entity_id = "sensor."+slugify(f"{entry.title} {self.name}")
        self._attr_unique_id = f"{entry.entry_id} {self.name}"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if self.sensor_name == "enabled":
            return self.coordinator.api.num_dead_enabled
        return self.coordinator.api.num_dead_disabled

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:counter"