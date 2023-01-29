"""Test integration_blueprint switch."""
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
    SWITCH,
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
    """Tests devices are registered in the entity registry."""
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

    entry = entity_registry.async_get("switch.npm_my_domain_com")
    assert entry.unique_id == entry_id + "_npm_my_domain_com"

    entry = entity_registry.async_get("switch.npm_other_domain_com")
    assert entry.unique_id == entry_id + "_npm_other_domain_com"


async def test_switch_services(hass, aioclient_mock, bypass_new_token):
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

    # Retrieve state of switch entity to test
    state = hass.states.get("switch.npm_my_domain_com")
    proxy_id = str(state.attributes["id"])

    # Mock enable and diable api calls for this entity, make them return True for a successful api call.
    aioclient_mock.post(
        MOCK_NPM_URL + "/api/nginx/proxy-hosts/" + proxy_id + "/disable",
        json=True,
    )

    aioclient_mock.post(
        MOCK_NPM_URL + "/api/nginx/proxy-hosts/" + proxy_id + "/enable",
        json=True,
    )

    # Ensure the enable/disable functions are called when turning the switch on/off
    with patch(
        "custom_components.npm_switches.NpmSwitchesApiClient.enable_proxy"
    ) as enable_proxy:
        await hass.services.async_call(
            SWITCH,
            SERVICE_TURN_ON,
            service_data={ATTR_ENTITY_ID: "switch.npm_my_domain_com"},
            blocking=True,
        )
        assert enable_proxy.called
        assert enable_proxy.call_args == call(
            str(MOCK_PROXY_HOSTS_DICT[proxy_id]["id"])
        )

    with patch(
        "custom_components.npm_switches.NpmSwitchesApiClient.disable_proxy"
    ) as disable_proxy:
        await hass.services.async_call(
            SWITCH,
            SERVICE_TURN_OFF,
            service_data={ATTR_ENTITY_ID: "switch.npm_my_domain_com"},
            blocking=True,
        )
        assert disable_proxy.called
        assert disable_proxy.call_args == call(
            str(MOCK_PROXY_HOSTS_DICT[proxy_id]["id"])
        )


async def test_switch_states(hass, aioclient_mock, bypass_new_token):
    """Test switch states."""
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

    for proxy_host in MOCK_PROXY_HOSTS_LIST:
        entity_id = "switch.npm_" + proxy_host["domain_names"][0].replace(".", "_")
        state = hass.states.get(entity_id)

        if proxy_host["enabled"] == 1:
            expected_state = "on"
        else:
            expected_state = "off"

        assert state.state == expected_state
        assert state.attributes["id"] == proxy_host["id"]
        assert state.attributes["domain_names"] == proxy_host["domain_names"]
