import asyncio
import json
import aiohttp

TOKEN = ""
URL = "https://discordapp.com/api"
LAST_SEQUENCE = 0
CHANNELS = {}

async def api_call(path, method="GET", **kwargs):
    print(path)
    defaults = {
        "headers": {
            "Authorization": f"Bot {TOKEN}",
            "User-Agent": "Panda Keeper Test Bot"
        }
    }
    kwargs = dict(defaults, **kwargs)
    async with aiohttp.ClientSession() as session:
        async with session.request(method, f"{URL}{path}", **kwargs) as response:
            assert 200 == response.status, response.reason
            return await response.json()

async def main():
    response = await api_call("/gateway")
    await start(response["url"])

async def heartbeat(ws, interval):
    while True:
        await asyncio.sleep(interval / 1000)  # seconds
        await ws.send_json({
            "op": 1,
            "d": LAST_SEQUENCE
        })

async def parse_message(message):
    if message["content"] == "!test":
        await api_call("/channels/" + str(message["channel_id"]) + "/messages", "POST", json={"content":"Response"})

async def start(url):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"{url}?v=6&encoding=json") as ws:
            async for msg in ws:
                data = json.loads(msg.data)
                if data["op"] == 10:
                    asyncio.ensure_future(heartbeat(ws, data['d']['heartbeat_interval']))
                    await ws.send_json({
                        "op": 2,  # Identify
                        "d": {
                            "token": TOKEN,
                            "properties": {},
                            "compress": False,
                            "large_threshold": 250
                        }
                    })
                elif data["op"] == 11:
                    pass
                elif data["op"] == 0:
                    LAST_SEQUENCE = data["s"]
                    if data["t"] == "MESSAGE_CREATE":
                        await parse_message(data["d"])
                    if data["t"] == "TYPING_START" or data["t"] == "GUILD_CREATE":
                        pass
                    else:
                        print(data)

def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
