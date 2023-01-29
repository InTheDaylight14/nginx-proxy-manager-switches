"""Test npm switches sensor."""
from unittest.mock import call, patch

from homeassistant.components.switch import SERVICE_TURN_OFF, SERVICE_TURN_ON
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry
from homeassistant.helpers import entity_registry as er

from custom_components.npm_switches import async_setup_entry
from custom_components.npm_switches.const import (
    DEFAULT_NAME,
    DOMAIN,
    SENSOR,
)

from .const import (
    MOCK_CONFIG,
    MOCK_PROXY_HOSTS_DICT,
    MOCK_PROXY_HOSTS_LIST,
    MOCK_NPM_URL,
)

import pytest

pytestmark = pytest.mark.asyncio


async def test_registry_entries(hass, aioclient_mock, bypass_new_token):
    """Tests sensors are registered in the entity registry."""
    entry_id = "test"
    config_entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, entry_id=entry_id, options=None
    )

    # Mock the api call to get proxy data, this allows setup to complete successfully.
    aioclient_mock.get(
        MOCK_NPM_URL + "/api/nginx/proxy-hosts",
        json=MOCK_PROXY_HOSTS_LIST,
    )

    assert await async_setup_entry(hass, config_entry)
    await hass.async_block_till_done()

    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("sensor.npm_enabled_proxy_hosts")
    assert entry.unique_id == entry_id + "_npm_enabled_proxy_hosts"

    entry = entity_registry.async_get("sensor.npm_disabled_proxy_hosts")
    assert entry.unique_id == entry_id + "_npm_disabled_proxy_hosts"


async def test_sensor_states(hass, aioclient_mock, bypass_new_token):
    """Test switch services."""
    # Create a mock entry so we don't have to go through config flow
    config_entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, entry_id="test", options=None
    )

    # Mock the api call to get proxy data, this allows setup to complete successfully.
    aioclient_mock.get(
        MOCK_NPM_URL + "/api/nginx/proxy-hosts",
        json=MOCK_PROXY_HOSTS_LIST,
    )

    assert await async_setup_entry(hass, config_entry)
    await hass.async_block_till_done()

    # Retrieve state of the enabled sesnor
    state = hass.states.get("sensor.npm_enabled_proxy_hosts")
    proxy_id = str(state.attributes["id"])

    assert state.state == "1"

    # Retrieve state of the disabled sesnor
    state = hass.states.get("sensor.npm_disabled_proxy_hosts")
    proxy_id = str(state.attributes["id"])

    assert state.state == "1"
