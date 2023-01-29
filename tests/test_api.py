"""Tests for integration_blueprint api."""
import asyncio
import pytest

import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt
from custom_components.npm_switches.api import NpmSwitchesApiClient

from .const import (
    MOCK_NPM_URL,
    MOCK_PROXY_HOSTS_LIST,
    MOCK_PROXY_HOSTS_DICT,
    MOCK_TOKEN,
)

pytestmark = pytest.mark.asyncio


async def test_api(hass, aioclient_mock, caplog):
    """Test API calls."""

    # To test the api submodule, we first create an instance of our API client
    api = NpmSwitchesApiClient(
        "test", "test", "http://test:81", async_get_clientsession(hass)
    )

    aioclient_mock.post(
        MOCK_NPM_URL + "/api/tokens",
        json=MOCK_TOKEN,
    )

    await api.async_get_new_token()
    assert api._token == MOCK_TOKEN["token"]
    assert api._token_expires == dt.parse_datetime(MOCK_TOKEN["expires"])

    aioclient_mock.get(
        MOCK_NPM_URL + "/api/nginx/proxy-hosts",
        json=MOCK_PROXY_HOSTS_LIST,
    )

    # print(await api.get_proxy_hosts())
    assert await api.get_proxy_hosts() == MOCK_PROXY_HOSTS_DICT

    assert api.get_npm_url == MOCK_NPM_URL

    # In order to get 100% coverage, we need to test `api_wrapper` to test the code
    # that isn't already called by `async_get_data` and `async_set_title`. Because the
    # only logic that lives inside `api_wrapper` that is not being handled by a third
    # party library (aiohttp) is the exception handling, we also want to simulate
    # raising the exceptions to ensure that the function handles them as expected.
    # The caplog fixture allows access to log messages in tests. This is particularly
    # useful during exception handling testing since often the only action as part of
    # exception handling is a logging statement
    caplog.clear()
    aioclient_mock.put(
        "https://jsonplaceholder.typicode.com/posts/1", exc=asyncio.TimeoutError
    )
    assert (
        await api.api_wrapper("put", "https://jsonplaceholder.typicode.com/posts/1")
        is None
    )
    assert (
        len(caplog.record_tuples) == 1
        and "Timeout error fetching information from" in caplog.record_tuples[0][2]
    )

    caplog.clear()
    aioclient_mock.post(
        "https://jsonplaceholder.typicode.com/posts/1", exc=aiohttp.ClientError
    )
    assert (
        await api.api_wrapper("post", "https://jsonplaceholder.typicode.com/posts/1")
        is None
    )
    assert (
        len(caplog.record_tuples) == 1
        and "Error fetching information from" in caplog.record_tuples[0][2]
    )

    caplog.clear()
    aioclient_mock.post("https://jsonplaceholder.typicode.com/posts/2", exc=Exception)
    assert (
        await api.api_wrapper("post", "https://jsonplaceholder.typicode.com/posts/2")
        is None
    )
    assert (
        len(caplog.record_tuples) == 1
        and "Something really wrong happened!" in caplog.record_tuples[0][2]
    )

    caplog.clear()
    aioclient_mock.post("https://jsonplaceholder.typicode.com/posts/3", exc=TypeError)
    assert (
        await api.api_wrapper("post", "https://jsonplaceholder.typicode.com/posts/3")
        is None
    )
    assert (
        len(caplog.record_tuples) == 1
        and "Error parsing information from" in caplog.record_tuples[0][2]
    )
