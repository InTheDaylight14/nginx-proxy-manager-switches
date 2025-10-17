"""Button platform for NPM Switches."""
from datetime import datetime

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import slugify, dt

from .const import DOMAIN
from .entity import NpmSwitchesEntity
from . import NpmSwitchesUpdateCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    api = hass.data[DOMAIN][entry.entry_id].api
    certificates = await api.get_certificates()
    entities = []

    if "include_certificate_sensors" in entry.data:
        if entry.data["include_certificate_sensors"]:
            for cert in certificates.values():
                entities.append(NpmSwitchesCertificateRenewButton(coordinator, entry, cert))

    async_add_entities(entities, True)

class NpmSwitchesCertificateRenewButton(NpmSwitchesEntity, ButtonEntity):
    """NPM Switches Certificate Renew Button Class."""

    def __init__(
        self,
        coordinator: NpmSwitchesUpdateCoordinator,
        entry: ConfigEntry,
        certificate: dict,
    ) -> None:
        """Initialize cert renew button."""
        super().__init__(coordinator, entry)
        self.cert_id = str(certificate["id"])
        self.name = "Renew Certificate " + certificate["domain_names"][0]
        self.entity_id = "button."+slugify(f"{entry.title}")+" Renew Cert "+str(self.cert_id)
        self._attr_unique_id = f"{entry.entry_id} {" Renew Cert "} {self.cert_id}"
        self._attr_icon = "mdi:refresh"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.api.renew_certificate(self.cert_id)