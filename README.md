# Luxor

## Asynchronous library to control FX Luminaire Luxor low voltage controllers.

Requires Python3, asyncio, and aiohttp

Async library to control an
[FX Luminaire Luxor ZD](http://www.fxl.com/product/power-and-control/luxor)
low voltage lighting controller.

This is an MVP, with a strong emphasis on *minimal*.

The initial use case is an API backend for
a [HomeAssistant](https://github.com/home-assistant/core) integration.
Homeassistant requires all API access to integrations happen via a PyPi module.
The client has the bare minimum functionality to support this use case.

Note:
[Luxor go library](https://github.com/scottlamb/luxor)
by Scott Lamb can be used as a reference for the Luxor protocol and for adding
additional support in the future.
