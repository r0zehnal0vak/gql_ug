import pytest_asyncio
import pytest
import logging

serversTestscope = "function"

@pytest.fixture
def FrontEndPort():
    return 33001
    # return 7999

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
            **userDict,
            **accessjson,
            "username": userDict["email"],
            # "password": "IDontCare",
            "password": userDict["email"],
        }
        async with session.post(loginurl, json=payload) as resp:
            assert resp.status == 200, resp
            tokendict = await resp.json()
    logging.info(f"have tokendict {tokendict}")
    token = tokendict["token"] 
    logging.info(f"have token {token}")
    yield token
    # yield ""
    logging.info(f"expiring token {token} ")

@pytest_asyncio.fixture(autouse=True, scope=serversTestscope)
async def Publickey(FrontEndPort):
    import aiohttp 
    userDict = AdminUser
    keyurl = f"http://localhost:{FrontEndPort}/oauth/publickey"
    # loginurl = f"http://localhost:{FrontEndPort}/oauth/login3"
    async with aiohttp.ClientSession() as session:
        async with session.get(keyurl) as resp:
            assert resp.status == 200, resp
            publickey = await resp.text()
    logging.info(f"have publickey {publickey}")
    yield publickey


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
