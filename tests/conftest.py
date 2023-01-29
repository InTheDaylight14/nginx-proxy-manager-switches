"""Global fixtures for integration_blueprint integration."""
# Fixtures allow you to replace functions with a Mock object. You can perform
# many options via the Mock to reflect a particular behavior from the original
# function that you want to see without going through the function's actual logic.
# Fixtures can either be passed into tests as parameters, or if autouse=True, they
# will automatically be used across all tests.
#
# Fixtures that are defined in conftest.py are available across all tests. You can also
# define fixtures within a particular test file to scope them locally.
#
# pytest_homeassistant_custom_component provides some fixtures that are provided by
# Home Assistant core. You can find those fixture definitions here:
# https://github.com/MatthewFlamm/pytest-homeassistant-custom-component/blob/master/pytest_homeassistant_custom_component/common.py
#
# See here for more info: https://docs.pytest.org/en/latest/fixture.html (note that
# pytest includes fixtures OOB which you can use as defined on this page)
from unittest.mock import patch

from .const import MOCK_PROXY_HOSTS_DICT, MOCK_TOKEN

import pytest

pytest_plugins = "pytest_homeassistant_custom_component"


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


# This fixture, when used, will result in calls to get_proxy_hosts to return None. To have the call
# return a value, we would add the `return_value=<VALUE_TO_RETURN>` parameter to the patch call.
@pytest.fixture(name="bypass_get_data")
def bypass_get_data_fixture():
    """Skip calls to get data from API."""
    with patch(
        "custom_components.npm_switches.NpmSwitchesApiClient.get_proxy_hosts",
        return_value=MOCK_PROXY_HOSTS_DICT,
    ):
        yield


@pytest.fixture(name="bypass_get_data_api")
def bypass_get_data_api_fixture():
    """Skip calls to get data from API."""
    with patch(
        "custom_components.npm_switches.NpmSwitchesApiClient.get_proxy_hosts",
        return_value=MOCK_PROXY_HOSTS_DICT,
    ):
        yield


@pytest.fixture(name="bypass_new_token")
def bypass_get_new_token_fixture():
    """Skip calls to get data from API."""
    with patch(
        "custom_components.npm_switches.NpmSwitchesApiClient.async_get_new_token",
        return_value=MOCK_TOKEN,
    ):
        yield


# @pytest.fixture(name="bypass_get_data")
# def bypass_get_data_fixture():
#     """Skip calls to get data from API."""
#     with patch("custom_components.npm_switches.NpmSwitchesApiClient.get_proxy_hosts"):
#         yield

##I don't know if we need this long-term???
# @pytest.fixture(name="bypass_check_token_expiration")
# def bypass_check_token_expiration():
#     """Skip calls to check token expiration."""
#     with patch(
#         "custom_components.npm_switches.NpmSwitchesApiClient.async_check_token_expiration"
#     ):
#         yield


# In this fixture, we are forcing calls to async_get_data to raise an Exception. This is useful
# for exception handling.
@pytest.fixture(name="error_on_get_data")
def error_get_data_fixture():
    """Simulate error when retrieving data from API."""
    with patch(
        "custom_components.npm_switches.NpmSwitchesApiClient.async_get_data",
        side_effect=Exception,
    ):
        yield


@pytest.fixture(name="error_on_get_new_token")
def error_get_new_token_fixture():
    """Simulate error when retrieving data from API."""
    with patch(
        "custom_components.npm_switches.NpmSwitchesApiClient.async_get_data",
        side_effect=Exception,
    ):
        yield
