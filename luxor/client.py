import asyncio
import aiohttp


class LuxorError(Exception):
    pass


class LuxorErrorUnknownMethod(LuxorError):
    pass


class LuxorErrorUnexpectedStatus(LuxorError):
    pass


def raise_for_status(data: dict) -> None:
    status = data["Status"]
    if status == 0:
        return
    # Using a dict is overkill for now, but ultimately this will have
    # more errors added
    raise {1: LuxorErrorUnknownMethod}.get(status, LuxorErrorUnexpectedStatus)


class Client:
    """Control an FX Luminaire Luxor controller."""

    def __init__(self, host: str, session: aiohttp.ClientSession, port: int = 80):
        self.host = host
        self.port = port
        self.session = session
        self.sem = asyncio.Semaphore(1)

    async def get_controller_name(self):
        data = await self.post("ControllerName")
        return data

    async def get_groups(self):
        data = await self.post("GroupListGet")
        return data["GroupList"]

    async def illuminate_group(self, group_number: int, intensity=100):
        json = {"GroupNumber": group_number, "Intensity": intensity}
        return await self.post("IlluminateGroup", json=json)

    async def get_themes(self):
        data = await self.post("ThemeListGet")
        if data["Restricted"]:
            return []
        else:
            return data["ThemeList"]

    async def illuminate_theme(self, theme_index: int, on_off: int):
        json = {"ThemeIndex": theme_index, "OnOff": on_off}
        return await self.post("IlluminateTheme", json=json)

    async def post(self, method: str, json=None):
        # The luxor controller can only handle 1 request at a time, hence the semaphore.
        # Sending a second request in parallel results in a connection refused.
        url = f"http://{self.host}:{self.port}/{method}.json"
        async with self.sem:
            async with self.session.post(url, json=json, ssl=False) as res:
                res.raise_for_status()
                data = await res.json()
                raise_for_status(data)
                return data
