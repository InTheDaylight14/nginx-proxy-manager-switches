# NPM Switches Custom Integration

[![GitHub Release][releases-shield]][releases]
![GitHub all releases][download-all]
![GitHub release (latest by SemVer)][download-latest]
[![GitHub Activity][commits-shield]][commits]

[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]



## Installation

### Recomended via HACs

1. Use [HACS](https://hacs.xyz/docs/setup/download), in `HACS > Integrations > Explore & Add Repositories` search for "NPM Switches".
2. Restart Home Assistant.
3. [![Add Integration][add-integration-badge]][add-integration] or in the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Tesla Custom Integration".

### Manual Download
1. Use the tool of choice to open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
3. If you do not have a `custom_components` directory (folder) there, you need to create it.
4. Download this repository's files.
5. Move or Copy the the entire `npm_switches/` directory (folder) in your HA `custom_components` directory (folder). End result should look like `custom_components/npm_switches/`.
6. Restart Home Assistant.
7. [![Add Integration][add-integration-badge]][add-integration] or in the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Tesla Custom Integration".

## Usage

'NPM Switches' offers integration with a local Nginx Proxy Manager server/instance. It will login into and retrieve a token from the NPM server every 24 hours. This token is used to querry the state of each proxy host every 60 seconds. It is also used to enable or disable a proxy host via local api call to the NPM server.

This integration provides the following entities:
- Switches - One switch for every proxy host that is configured
- Sensors - Number of enabled proxy hosts, number of disabled proxy hosts

Future features could include redirection host switches and 404 host switches.

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

_Component built with [integration_blueprint][integration_blueprint]._

***

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[commits-shield]: https://img.shields.io/github/commit-activity/w/InTheDaylight14/nginx-proxy-manager-switches?style=for-the-badge
[commits]: https://github.com/InTheDaylight14/nginx-proxy-manager-switches/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
<!-- [exampleimg]: example.png -->
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: LICENSE
[license-shield]: https://img.shields.io/github/license/InTheDaylight14/nginx-proxy-manager-switches?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-@InTheDaylight14-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/InTheDaylight14/nginx-proxy-manager-switches?style=for-the-badge
[releases]: https://github.com/InTheDaylight14/nginx-proxy-manager-switches/releases
[add-integration]: https://my.home-assistant.io/redirect/config_flow_start?domain=npm_switches
[add-integration-badge]: https://my.home-assistant.io/badges/config_flow_start.svg
[download-all]: https://img.shields.io/github/downloads/InTheDaylight14/nginx-proxy-manager-switches/total?style=for-the-badge
[download-latest]: https://img.shields.io/github/downloads/InTheDaylight14/nginx-proxy-manager-switches/latest/total?style=for-the-badge
