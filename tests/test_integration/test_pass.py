import pytest
import pytest_asyncio
import aiohttp
import logging
import jwt
import os

@pytest_asyncio.fixture(autouse=True)
async def AccessToken():
    pass

@pytest.fixture(autouse=True)
def OAuthServer():
    pass

@pytest.fixture(autouse=True)
def NoRole_UG_Server():
    pass

@pytest.fixture(autouse=True)
def AllRole_UG_Server():
    pass


@pytest.mark.asyncio
async def _test_token(AccessToken, Publickey):
    logging.info(f"AccessToken is {AccessToken}")
    logging.info(f"Publickey is {Publickey}")

    pkey = Publickey.replace('"', '').replace("\\n", "\n").encode()
    logging.info(f"Publickey is {pkey}")
    jwtdecoded = jwt.decode(jwt=AccessToken, key=pkey, algorithms=["RS256"])
    print(jwtdecoded)    
    logging.info(f"jwtdecoded is {jwtdecoded}")


    token2 = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYWNjZXNzX3Rva2VuIjoiQUNDVC0waDhHVHVXdGtrVEhydDBtRmcwbFc3dFR4Ym1ycHdyRiIsImV4cGlyZXNfaW4iOjM2MDAsInJlZnJlc2hfdG9rZW4iOiJSRUZULVRsWTkweG9udVYyQkZkYmxyOENNNEVaQjJRaUJMejhqIiwidXNlcl9pZCI6IjJkOWRjODY4LWE0YTItMTFlZC1iOWRmLTAyNDJhYzEyMDAwMyJ9.fKoidzs4SFWV1L4I5B4q_N0dx8CSHq3PHQnLuZeFmr5CS44ETeM7-0xhOGJdaTnQ3FzAqbAtvbwcZM5sSdrwy7AMkGXzOKK1D27iwxeIBkITWB6IJeDEFOJLz2QPEUJfSSEUE5BhkksUj-dMtdm6i6cqFv9aEj4WwcqgVSm8ATzOqtXG1vaTqcpeWaY1IGOHTVh2RBhZdHUOcQdSx-SA_ajHGPkdA8oat7iKu_NRVPfMnGoLnyF7hVfZYY5_wjYE6pAMMAH9homn3hMvp-y1K5vRSZ4hAdog8TDq6ujvl3JwGHM2tZmuRqXe9HIQxr_ISB0tBI9zgJ1k23wgifqXTA'    
    jwtdecoded = jwt.decode(jwt=token2, key=pkey, algorithms=["RS256"])
    print(jwtdecoded)    
    logging.info(f"jwtdecoded is {jwtdecoded}")
    pass


@pytest.mark.asyncio
async def test_result_test(AdminExecutor):
    import aiohttp    
    query = """query($where: ) {}"""   
    pass


async def run_the_test(
        DemoData,
        JWTPUBLICKEYURL,
        JWTRESOLVEUSERPATHURL
        ):

    JWTPUBLICKEYLOGIN = JWTPUBLICKEYURL.replace("publickey", "login3")
    print(f"JWTPUBLICKEYLOGIN = {JWTPUBLICKEYLOGIN}")
    print(f"JWTPUBLICKEYURL = {JWTPUBLICKEYURL}")
    print(f"JWTRESOLVEUSERPATHURL = {JWTRESOLVEUSERPATHURL}")
    
    logging.info(f"JWTPUBLICKEYLOGIN = {JWTPUBLICKEYLOGIN}")
    logging.info(f"JWTPUBLICKEYURL = {JWTPUBLICKEYURL}")
    logging.info(f"JWTRESOLVEUSERPATHURL = {JWTRESOLVEUSERPATHURL}")

    users = DemoData["users"]
    user0 = users[0]

    print(f"loging as {user0}")
    logging.info(f"loging as {user0}")
    async with aiohttp.ClientSession() as session:
        async with session.get(JWTPUBLICKEYLOGIN) as resp:
            assert resp.status == 200, resp
            accessjson = await resp.json()

        print(f"have key={accessjson}")
        logging.info(f"have key={accessjson}")
        payload = {
            "username": user0["email"],
            "password": user0["email"],
            **accessjson
        }
        
        async with session.post(JWTPUBLICKEYLOGIN, json=payload) as resp:
            assert resp.status == 200, resp
            tokendict = await resp.json()
    token = tokendict["token"] 
    print(f"have token {token}")
    logging.info(f"have token {token}")

    async with aiohttp.ClientSession() as session:
        async with session.get(JWTPUBLICKEYURL) as resp:
            assert resp.status == 200, resp
            pktext = await resp.text() 
    print(f"have pktext={pktext}")
    logging.info(f"have pktext={pktext}")
    pkey = pktext.replace('"', "").replace("\\n", "\n")
    jwtdecoded = jwt.decode(jwt=token, key=pkey, algorithms=["RS256"])
    print(f"jwtdecoded = {jwtdecoded}")
    logging.info(f"jwtdecoded = {jwtdecoded}")
    userid = jwtdecoded["user_id"]
    print(f"userid = {userid}")
    logging.info(f"userid = {userid}")
    print(f"SUCCESS")
    logging.info(f"SUCCESS")

    pass

@pytest.mark.asyncio
async def test_container(DemoData):
    # JWTPUBLICKEYURL=http://localhost:33001/oauth/publickey
    # JWTRESOLVEUSERPATHURL=http://localhost:33001/oauth/userinfo
    JWTPUBLICKEYURL = os.environ.get("JWTPUBLICKEYURL", None)
    assert JWTPUBLICKEYURL is not None, f"JWTPUBLICKEYURL = {JWTPUBLICKEYURL}"
    JWTRESOLVEUSERPATHURL = os.environ.get("JWTRESOLVEUSERPATHURL", None)
    assert JWTRESOLVEUSERPATHURL is not None, f"JWTRESOLVEUSERPATHURL = {JWTRESOLVEUSERPATHURL}"

    await run_the_test(DemoData, JWTPUBLICKEYURL, JWTRESOLVEUSERPATHURL)


@pytest.mark.asyncio
async def test_out_of_compose(DemoData):
    JWTPUBLICKEYURL = "http://localhost:33001/oauth/publickey"
    JWTRESOLVEUSERPATHURL = "http://localhost:33001/oauth/userinfo"
    # JWTPUBLICKEYURL = os.environ.get("JWTPUBLICKEYURL", None)
    assert JWTPUBLICKEYURL is not None, f"JWTPUBLICKEYURL = {JWTPUBLICKEYURL}"
    # JWTRESOLVEUSERPATHURL = os.environ.get("JWTRESOLVEUSERPATHURL", None)
    assert JWTRESOLVEUSERPATHURL is not None, f"JWTRESOLVEUSERPATHURL = {JWTRESOLVEUSERPATHURL}"

    await run_the_test(DemoData, JWTPUBLICKEYURL, JWTRESOLVEUSERPATHURL)