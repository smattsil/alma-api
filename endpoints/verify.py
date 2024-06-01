from httpx import AsyncClient


async def verify(school, username, password):

    payload = {
        'username': username,
        'password': password
    }

    async with AsyncClient(timeout=None) as client:
        # logging in
        resp = await client.post(f'https://{school}.getalma.com/login', data=payload)
        return {'authentic': resp.status_code}
