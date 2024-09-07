import aiohttp

async def authenticity(sch, usr, pwd):
    async with aiohttp.ClientSession(f"https://{sch}.getalma.com") as session:
        async with session.post("/login", data = {"username": usr, "password": pwd}) as resp:
            response_code = True if (resp.status == 200) else False
            return {"authentic": response_code}
