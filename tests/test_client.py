import aiohttp
from aiohttp import web

import luxor


async def controller_name_handler(request: web.Request) -> web.Response:
    return web.json_response({"Status": 0, "ControllerName": "Foo"})


async def group_list_handler(request: web.Request) -> web.Response:
    # client isn't parsing the contents of the list
    return web.json_response({"Status": 0, "GroupList": ["groups not parsed"]})


async def theme_list_handler(request: web.Request) -> web.Response:
    # client isn't parsing the contents of the list
    return web.json_response(
        {"Status": 0, "Restricted": 0, "ThemeList": ["themes not parsed"]}
    )


async def illuminate_theme_handler(request: web.Request) -> web.Response:
    # client isn't parsing the contents of the list
    req = await request.json()
    assert req["ThemeIndex"] == 20
    assert req["OnOff"] == 1
    return web.json_response({"Status": 0})


async def illuminate_group_handler(request: web.Request) -> web.Response:
    # client isn't parsing the contents of the list
    req = await request.json()
    assert req["GroupNumber"] == 42
    assert req["Intensity"] == 97
    return web.json_response({"Status": 0})


async def create_server(aiohttp_server):
    app = web.Application()
    app.router.add_post("/ControllerName.json", controller_name_handler)
    app.router.add_post("/GroupListGet.json", group_list_handler)
    app.router.add_post("/ThemeListGet.json", theme_list_handler)
    app.router.add_post("/IlluminateTheme.json", illuminate_theme_handler)
    app.router.add_post("/IlluminateGroup.json", illuminate_group_handler)
    return await aiohttp_server(app)


async def theme_list_handler_restricted(request: web.Request) -> web.Response:
    # client isn't parsing the contents of the list
    return web.json_response(
        {"Status": 0, "Restricted": 1, "ThemeList": ["themes not parsed"]}
    )


async def create_server_restricted_themes(aiohttp_server):
    app = web.Application()
    app.router.add_post("/ThemeListGet.json", theme_list_handler_restricted)
    return await aiohttp_server(app)


async def test_get_controller_name(aiohttp_server, loop):
    server = await create_server(aiohttp_server)
    async with aiohttp.ClientSession() as session:
        client = luxor.Client(server.host, session, port=server.port)
        resp = await client.get_controller_name()
        assert resp["ControllerName"] == "Foo"


async def test_get_themes(aiohttp_server, loop):
    server = await create_server(aiohttp_server)
    async with aiohttp.ClientSession() as session:
        client = luxor.Client(server.host, session, port=server.port)
        resp = await client.get_themes()
        assert resp == ["themes not parsed"]


async def test_get_themes_restricted(aiohttp_server, loop):
    server = await create_server_restricted_themes(aiohttp_server)
    async with aiohttp.ClientSession() as session:
        client = luxor.Client(server.host, session, port=server.port)
        resp = await client.get_themes()
        assert resp == []


async def test_illuminate_theme(aiohttp_server, loop):
    server = await create_server(aiohttp_server)
    async with aiohttp.ClientSession() as session:
        client = luxor.Client(server.host, session, port=server.port)
        await client.illuminate_theme(20, 1)


async def test_illuminate_group(aiohttp_server, loop):
    server = await create_server(aiohttp_server)
    async with aiohttp.ClientSession() as session:
        client = luxor.Client(server.host, session, port=server.port)
        await client.illuminate_group(42, 97)
