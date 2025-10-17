"""Constants for NPM Switches."""
# Base component constants
NAME = "NPM Switches"
DOMAIN = "npm_switches"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "2.1.0"
ATTRIBUTION = "Data provided by your NPM Instance"
ISSUE_URL = "https://github.com/InTheDaylight14/nginx-proxy-manager-switches/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
# BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
BUTTON = 'button'
PLATFORMS = [SENSOR, SWITCH, BUTTON]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_NPM_URL = "npm_url"
CONF_INDLUDE_PROXY = "include_proxy_hosts"
CONF_INCLUDE_REDIR = "include_redirection_hosts"
CONF_INCLUDE_STREAMS = "include_stream_hosts"
CONF_INCLUDE_DEAD = "include_dead_hosts"
CONF_INCLUDE_SENSORS = "include_enable_disable_count_sensors"
CONF_INCLUDE_CERTS = "include_certificate_sensors"
DEFAULT_ENABLED = ""
DEFAULT_USERNAME = ""
DEFAULT_PASSWORD = ""
DEFAULT_NPM_URL = "http://"
DEFAULT_INDLUDE_PROXY = True
DEFAULT_INCLUDE_REDIR = False
DEFAULT_INCLUDE_STREAMS = False
DEFAULT_INCLUDE_DEAD = False
DEFAULT_INCLUDE_SENSORS = True
DEFAULT_INCLUDE_CERTS = False

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
