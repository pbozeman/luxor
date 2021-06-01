#! /usr/bin/env python3

import aiohttp
import asyncio
import os
import sys

import luxor


async def main():
    host = os.environ.get("LUXOR_HOST")

    if not host:
        if len(sys.argv) != 2:
            print("usage: list_groups.py [host]")
            sys.exit(-1)
        host = sys.argv[1]

    async with aiohttp.ClientSession() as session:
        await run(session, host)


async def run(session, host):
    client = luxor.Client(host, session)

    data = await client.get_controller_name()
    print(
        f"Controller: {data['Controller']} ConnType: {data['ConnType']} RSSI: {data['RSSI']}"
    )

    groups = await client.get_groups()
    print("Groups:")
    for g in groups:
        print(
            f"  GroupId:    {g['Grp']}\n"
            f"  Name:       {g['Name']}\n"
            f"  Intensity:  {g['Inten']}\n"
            f"  Color:      {g['Colr']}\n"
        )

    themes = await client.get_themes()
    print("Themes:")
    for t in themes:
        print(
            f"  ThemeIndex: {t['ThemeIndex']}\n"
            f"  Name:       {t['Name']}\n"
            f"  OnOff:      {t['OnOff']}\n"
        )


asyncio.run(main())
