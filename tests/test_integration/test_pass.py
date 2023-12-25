import pytest
import logging

@pytest.mark.asyncio
async def test_token(AccessToken):
    logging.info(f"AccessToken is {AccessToken}")
    pass


@pytest.mark.asyncio
async def test_result_test(AdminExecutor):
    import aiohttp    
    query = """query($where: ) {}"""

    
    pass


