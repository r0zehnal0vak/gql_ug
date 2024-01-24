import pytest
import logging
import jwt

@pytest.mark.asyncio
async def test_token(AccessToken, Publickey):
    logging.info(f"AccessToken is {AccessToken}")
    logging.info(f"Publickey is {Publickey}")

    pkey = Publickey.replace('"', '').replace("\\n", "\n").encode()
    logging.info(f"Publickey is {pkey}")
    jwtdecoded = jwt.decode(jwt=AccessToken, key=pkey, algorithms=["RS256"])
    print(jwtdecoded)    
    logging.info(f"jwtdecoded is {jwtdecoded}")
    pass


@pytest.mark.asyncio
async def test_result_test(AdminExecutor):
    import aiohttp    
    query = """query($where: ) {}"""

    
    pass


