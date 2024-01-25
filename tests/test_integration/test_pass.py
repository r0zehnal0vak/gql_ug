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


