"""BlueprintEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.util import slugify

from .const import DOMAIN, NAME, VERSION, ATTRIBUTION


class NpmSwitchesEntity(CoordinatorEntity):
    """Init NPM user device."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.host = None
        self.name = None
        self.entity_id = None
        self.config_entry = config_entry
        self.host_id = None
        self.coordinator = coordinator
        self._attr_unique_id = None
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
            name=self.config_entry.title,
        )
