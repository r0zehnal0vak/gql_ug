import pytest_asyncio
import pytest
import logging

serversTestscope = "function"

@pytest.fixture
def FrontEndPort():
    return 33001

@pytest.fixture
def AdminUser():
    return {"email": "john.newbie@world.com", "password": "IDontCare"}

@pytest_asyncio.fixture(autouse=True, scope=serversTestscope)
async def AccessToken(FrontEndPort, AdminUser):
    import aiohttp 
    userDict = AdminUser
    # keyurl = f"http://localhost:{FrontEndPort}/publickey"
    loginurl = f"http://localhost:{FrontEndPort}/oauth/login3"
    async with aiohttp.ClientSession() as session:
        async with session.get(loginurl) as resp:
            assert resp.status == 200, resp
            accessjson = await resp.json()
        payload = {
            "username": userDict["email"],
            "password": "IDontCare",
            **userDict,
            **accessjson
        }
        async with session.post(loginurl, json=payload) as resp:
            assert resp.status == 200, resp
            tokendict = await resp.json()
    token = tokendict["token"] 
    logging.info(f"have token {token}")
    yield token
    logging.info(f"expiring token {token} ")



@pytest_asyncio.fixture(autouse=True, scope=serversTestscope)
async def AdminExecutor(FrontEndPort, AccessToken):
    import aiohttp
    gqlrl = f"http://localhost:{FrontEndPort}/gql"
    async def Executor(query, variable_values):
        payload = {
            "query": query,
            "variables": variable_values
        }
        headers = {"headers": f"Bearer {AccessToken}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(gqlrl, json=payload, headers=headers) as resp:
                assert resp.status == 200, resp
                jsonresponse = await resp.json()
        return jsonresponse   

    yield Executor
