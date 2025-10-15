"""Sample API Client."""
import logging
import asyncio
import socket

# from typing import Optional
# from datetime import datetime
import aiohttp
import async_timeout

from homeassistant.util import dt

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class NpmSwitchesApiClient:
    """Handle api calls to NPM instance."""

    def __init__(
        self, username: str, password: str, npm_url: str, session: aiohttp.ClientSession
    ) -> None:
        """NPM API Client."""
        self._username = username
        self._password = password
        self._session = session
        self._npm_url = npm_url
        self._token = None
        self._token_expires = dt.utcnow()
        self._headers = None
        self.proxy_hosts_data = None
        self.redir_hosts_data = None
        self.stream_hosts_data = None
        self.dead_hosts_data = None
        self.certificates_data = None
        self.num_proxy_enabled = 0
        self.num_proxy_disabled = 0
        self.num_redir_enabled = 0
        self.num_redir_disabled = 0
        self.num_stream_enabled = 0
        self.num_stream_disabled = 0
        self.num_dead_enabled = 0
        self.num_dead_disabled = 0

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        url = "http://test:81"
        return await self.api_wrapper("get", url)

    # async def async_set_title(self, value: str) -> None:
    #     """Get data from the API."""
    #     url = "https://jsonplaceholder.typicode.com/posts/1"
    #     await self.api_wrapper("patch", url, data={"title": value}, headers=HEADERS)

    async def get_proxy_hosts(self) -> list():
        """Get a list of proxy-hosts."""
        self.num_proxy_enabled = 0
        self.num_proxy_disabled = 0

        if self._token is None:
            await self.async_get_new_token()
        url = self._npm_url + "/api/nginx/proxy-hosts"
        proxy_hosts_list = await self.api_wrapper("get", url, headers=self._headers)
        self.proxy_hosts_data = {}
        for proxy in proxy_hosts_list:
            self.proxy_hosts_data[str(proxy["id"])] = proxy
            if proxy["enabled"] == 1:
                self.num_proxy_enabled += 1
            else:
                self.num_proxy_disabled += 1

        return self.proxy_hosts_data

    async def get_redirection_hosts(self) -> list():
        """Get a list of redirection hosts."""
        self.num_redir_enabled = 0
        self.num_redir_disabled = 0

        if self._token is None:
            await self.async_get_new_token()
        url = self._npm_url + "/api/nginx/redirection-hosts"
        redirection_hosts_list = await self.api_wrapper("get", url, headers=self._headers)

        self.redir_hosts_data = {}
        for redirection in redirection_hosts_list:
            self.redir_hosts_data[str(redirection["id"])] = redirection
            if redirection["enabled"] == 1:
                self.num_redir_enabled += 1
            else:
                self.num_redir_disabled += 1
        return self.redir_hosts_data

    async def get_stream_hosts(self) -> list():
        """Get a list of stream hosts."""
        self.num_stream_enabled = 0
        self.num_stream_disabled = 0

        if self._token is None:
            await self.async_get_new_token()
        url = self._npm_url + "/api/nginx/streams"
        stream_hosts_list = await self.api_wrapper("get", url, headers=self._headers)

        self.stream_hosts_data = {}
        for stream in stream_hosts_list:
            self.stream_hosts_data[str(stream["id"])] = stream
            if stream["enabled"] == 1:
                self.num_stream_enabled += 1
            else:
                self.num_stream_disabled += 1
        return self.stream_hosts_data

    async def get_dead_hosts(self) -> list():
        """Get a list of stream hosts."""
        self.num_dead_enabled = 0
        self.num_dead_disabled = 0

        if self._token is None:
            await self.async_get_new_token()
        url = self._npm_url + "/api/nginx/dead-hosts"
        dead_hosts_list = await self.api_wrapper("get", url, headers=self._headers)

        self.dead_hosts_data = {}
        for dead in dead_hosts_list:
            self.dead_hosts_data[str(dead["id"])] = dead
            if dead["enabled"] == 1:
                self.num_dead_enabled += 1
            else:
                self.num_dead_disabled += 1
        return self.dead_hosts_data

    async def get_host(self, host_id: int, host_type: str) -> dict:
        """Get a host by id and type.
        Host Type: proxy-hosts, redirection-hosts, streams, dead-hosts"""
        if host_type == "proxy-hosts":
            return self.proxy_hosts_data[host_id]
        elif host_type == "redirection-hosts":
            return self.redir_hosts_data[host_id]
        elif host_type == "streams":
            return self.stream_hosts_data[host_id]
        elif host_type == "dead-hosts":
            return self.dead_hosts_data[host_id]
        else:
            return None

    async def async_get_new_token(self) -> None:
        """Get a new token."""
        url = self._npm_url + "/api/tokens"
        response = await self.api_wrapper(
            "token",
            url,
            data={
                "identity": self._username,
                "secret": self._password,
            },
        )

        self._token = response["token"]
        self._token_expires = dt.parse_datetime(response["expires"])
        self._headers = {
            "Authorization": "Bearer " + self._token,
        }

    async def async_check_token_expiration(self) -> None:
        """Check if token expired."""
        utcnow = dt.utcnow()

        if utcnow > self._token_expires:
            await self.async_get_new_token()

    async def enable_host(self, host_id: str, host_type: str) -> None:
        """Enable the passed host
           Host Type: proxy-hosts, redirection-hosts, streams, dead-hosts"""
        url = self._npm_url + "/api/nginx/" + host_type + "/" + host_id + "/enable"
        response = await self.api_wrapper("post", url, headers=self._headers)

        if response is True:
            if host_type == "proxy-hosts":
                self.proxy_hosts_data[host_id]["enabled"] = 1
            if host_type == "redirection-hosts":
                self.redir_hosts_data[host_id]["enabled"] = 1
            if host_type == "streams":
                self.stream_hosts_data[host_id]["enabled"] = 1
            if host_type == "dead-hosts":
                self.dead_hosts_data[host_id]["enabled"] = 1
        elif "error" in response.keys():
            _LOGGER.error(
                "Error enabling host type %s host id %s. Error message: '%s'",
                host_type,
                host_id,
                response["error"]["message"],
            )

    async def disable_host(self, host_id: str, host_type: str) -> None:
        """Disable the passed host.
           Host Type: proxy-hosts, redirection-hosts, streams, dead-hosts"""
        url = self._npm_url + "/api/nginx/" +host_type+ "/" + host_id + "/disable"

        response = await self.api_wrapper("post", url, headers=self._headers)
        if response is True:
            if host_type == "proxy-hosts":
                self.proxy_hosts_data[host_id]["enabled"] = 0
            if host_type == "redirection-hosts":
                self.redir_hosts_data[host_id]["enabled"] = 0
            if host_type == "streams":
                self.stream_hosts_data[host_id]["enabled"] = 0
            if host_type == "dead-hosts":
                self.dead_hosts_data[host_id]["enabled"] = 0
        elif "error" in response.keys():
            _LOGGER.error(
                "Error enabling host type %s host id %s. Error message: '%s'",
                host_type,
                host_id,
                response["error"]["message"],
            )

    def is_host_enabled(self, host_id: str, host_type: str) -> bool:
        """Return True if the proxy is enabled.
            Host Type: proxy-hosts, redirection-hosts, streams, dead-hosts"""
        if host_type == "proxy-hosts":
            if self.proxy_hosts_data[host_id]["enabled"] == 1:
                return True
            else:
                return False
        elif host_type == "redirection-hosts":
            if self.redir_hosts_data[host_id]["enabled"] == 1:
                return True
            else:
                return False
        elif host_type == "streams":
            if self.stream_hosts_data[host_id]["enabled"] == 1:
                return True
            else:
                return False
        elif host_type == "dead-hosts":
            if self.dead_hosts_data[host_id]["enabled"] == 1:
                return True
            else:
                return False
        else:
            return None

    async def get_certificates(self) -> list():
        """Get a list of cirtificates."""

        if self._token is None:
            await self.async_get_new_token()
        url = self._npm_url + "/api/nginx/certificates"
        certificate_list = await self.api_wrapper("get", url, headers=self._headers)

        self.certificates_data = {}
        for cert in certificate_list:
            self.certificates_data[str(cert["id"])] = cert

        return self.certificates_data

    def get_certificate(self, certificate_id: int) -> dict:
        """Get a single certificate"""
        return self.certificates_data[certificate_id]

    async def renew_certificate(self, certificate_id: int) -> None:
        """Renew the passed certificate"""
        url = self._npm_url + "/api/nginx/certificates/" + str(certificate_id) + "/renew"
        response = await self.api_wrapper("post", url, headers=self._headers)

        if response is True:
           await self.get_certificates()
        elif "error" in response.keys():
            _LOGGER.error(
                "Error enabling host type %s host id %s. Error message: '%s'",
                host_type,
                host_id,
                response["error"]["message"],
            )

    @property
    def get_num_proxy_enabled(self) -> int:
        """Return the num enabled proxy hosts."""
        return self.num_proxy_enabled

    @property
    def get_num_proxy_disabled(self) -> int:
        """Return the num disabled proxy hosts."""
        return self.num_proxy_disabled

    @property
    def get_npm_url(self) -> str:
        """Return the npm url."""
        return self._npm_url

    async def api_wrapper(
        self, method: str, url: str, data: dict = None, headers: dict = None
    ) -> dict:
        """Get information from the API."""
        if method != "token":
            await self.async_check_token_expiration()

        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                elif method == "put":
                    await self._session.put(url, headers=headers, json=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, json=data)

                elif method == "post" or method == "token":
                    response = await self._session.post(url, headers=headers, json=data)
                    return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
