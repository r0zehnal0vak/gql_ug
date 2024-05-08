import pytest
import logging
import uuid
import sqlalchemy


async def getRow(async_session_maker, tableName, id):
    statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName} WHERE id=:id").bindparams(id=id)
    #statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName}")
    print("statement", statement, flush=True)
    async with async_session_maker() as session:
        rows = await session.execute(statement)
        row = rows.first()
    return row    
        

def createByIdTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Env_GQLUG_ENDPOINT_URL_8124):
        
        def testResult(resp):
            print("response", resp)
            errors = resp.get("errors", None)
            assert errors is None, f"response has errors {errors}"
            
            respdata = resp.get("data", None)
            assert respdata is not None, f"response {resp} has not data"
            
            respdata = respdata["result"]
            assert respdata is not None, f"response {resp} has not enitity"

            for att in attributeNames:
                assert respdata[att] == f'{datarow[att]}', f"attributes are different {att}"

        clientExecutor = ClientExecutorDemo
        schemaExecutor = SchemaExecutorDemo

        data = DemoData
        datarow = data[tableName][0]
        content = "{" + ", ".join(attributeNames) + "}"
        query = "query($id: UUID!){" f"result: {queryEndpoint}(id: $id)" f"{content}" "}"

        variable_values = {"id": f'{datarow["id"]}'}
        
        row = await getRow(SQLite, tableName=tableName, id=datarow["id"])
        assert row is not None, f"row with id={datarow['id']} not found in DB"

        # append(queryname=f"{queryEndpoint}_{tableName}", query=query, variables=variable_values)        
        logging.info(f"query for {query} with {variable_values}")

        resp = await schemaExecutor(query, variable_values)
        testResult(resp)
        # resp = await clientExecutor(query, variable_values)
        # testResult(resp)

    return result_test

def createPageTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo):

        def testResult(resp):
            errors = resp.get("errors", None)
            assert errors is None, f"resp has errors {errors}"
            respdata = resp.get("data", None)
            assert respdata is not None

            respdata = respdata.get(queryEndpoint, None)
            assert respdata is not None
            datarows = data[tableName]           

            for rowa, rowb in zip(respdata, datarows):
                for att in attributeNames:
                    assert rowa[att] == f'{rowb[att]}'            

        schemaExecutor = SchemaExecutorDemo
        clientExecutor = ClientExecutorDemo

        data = DemoData

        content = "{" + ", ".join(attributeNames) + "}"
        query = "query{" f"{queryEndpoint}" f"{content}" "}"

        # append(queryname=f"{queryEndpoint}_{tableName}", query=query)

        resp = await schemaExecutor(query)
        testResult(resp)
        # resp = await clientExecutor(query)
        # testResult(resp)
        
    return result_test

def createResolveReferenceTest(tableName, gqltype, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context, Env_GQLUG_ENDPOINT_URL_8124):

        def testResult(resp):
            print(resp)
            errors = resp.get("errors", None)
            assert errors is None, f" response has errors {errors}"
            respdata = resp.get("data", None)
            assert respdata is not None, f"missing data in response {resp}"

            logging.info(respdata)
            respdata = respdata.get('_entities', None)
            assert respdata is not None, f"missing _entities in response {resp}"

            assert len(respdata) == 1, f"_entities has not just one member {respdata}"
            respdata = respdata[0]
            assert respdata is not None, f"got None value for id {rowid}"
            assert respdata['id'] == rowid, f"different id {respdata['id']} in response, expected {rowid}"

        schemaExecutor = SchemaExecutorDemo
        clientExecutor = ClientExecutorDemo

        content = "{" + ", ".join(attributeNames) + "}"

        data = DemoData
        table = data[tableName]
        for row in table:
            rowid = f"{row['id']}"

            # query = (
            #     'query($id: UUID!) { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: $id' + 
            #     ' }])' +
            #     '{' +
            #     f'...on {gqltype}' + content +
            #     '}' + 
            #     '}')

            # variable_values = {"id": rowid}

            query = ("query($rep: [_Any!]!)" + 
                "{" +
                "_entities(representations: $rep)" +
                "{"+
                f"    ...on {gqltype} {content}"+
                "}"+
                "}"
            )
            
            variable_values = {"rep": [{"__typename": f"{gqltype}", "id": f"{rowid}"}]}

            logging.info(f"query representations {query} with {variable_values}")
            # resp = await clientExecutor(query, {**variable_values})
            # testResult(resp)
            resp = await schemaExecutor(query, {**variable_values})
            testResult(resp)

        # append(queryname=f"{gqltype}_representation", query=query)

    return result_test

def createFrontendQuery(query="{}", variables={}, asserts=[]):
    @pytest.mark.asyncio
    async def test_frontend_query(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context, Env_GQLUG_ENDPOINT_URL_8124):    
        logging.debug("createFrontendQuery")
        # async_session_maker = await prepare_in_memory_sqllite()
        # await prepare_demodata(async_session_maker)
        # context_value = createContext(async_session_maker)
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")

        # append(queryname=f"query", query=query, variables=variables)
        resp = await SchemaExecutorDemo(
            query=query, 
            variable_values=variables
        )
        # resp = await schema.execute(
        #     query=query, 
        #     variable_values=variables, 
        #     context_value=context_value
        # )

        assert resp.get("errors", None) is None, resp["errors"]
        respdata = resp.get("data", None)
        logging.info(f"query for \n{query} with \n{variables} got response: \n{respdata}")
        for a in asserts:
            a(respdata)
    return test_frontend_query


def createUpdateQuery(query="{}", variables={}, tableName=""):
    @pytest.mark.asyncio
    async def test_update(SQLite, DemoData, ClientExecutorDemo, SchemaExecutorDemo, Context, Env_GQLUG_ENDPOINT_URL_8124):
        logging.debug("test_update")
        assert variables.get("id", None) is not None, "variables has not id"
        variables["id"] = uuid.UUID(f"{variables['id']}")
        assert "$lastchange: DateTime!" in query, "query must have parameter $lastchange: DateTime!"
        assert "lastchange: $lastchange" in query, "query must use lastchange: $lastchange"
        assert tableName != "", "missing table name"

        async_session_maker = SQLite

        print("variables['id']", variables, flush=True)
        statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName} WHERE id=:id").bindparams(id=variables['id'])
        #statement = sqlalchemy.text(f"SELECT id, lastchange FROM {tableName}")
        print("statement", statement, flush=True)
        async with async_session_maker() as session:
            rows = await session.execute(statement)
            row = rows.first()
            
            print("row", row)
            id = row[0]
            lastchange = row[1]

            print(id, lastchange)

        variables["lastchange"] = lastchange
        variables["id"] = f'{variables["id"]}'
        
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")

        # append(queryname=f"query_{tableName}", mutation=query, variables=variables)
        resp = await SchemaExecutorDemo(
            query=query, 
            variable_values=variables
        )
        # resp = await schema.execute(
        #     query=query, 
        #     variable_values=variables, 
        #     context_value=context_value
        # )

        assert resp.get("errors", None) is None, resp["errors"]
        respdata = resp.get("data", None)
        assert respdata is not None, "GQL response is empty"
        print("respdata", respdata)
        keys = list(respdata.keys())
        assert len(keys) == 1, "expected update test has one result"
        key = keys[0]
        result = respdata.get(key, None)
        assert result is not None, f"{key} is None (test update) with {query}"
        entity = None
        for key, value in result.items():
            print(key, value, type(value))
            if isinstance(value, dict):
                entity = value
                break
        assert entity is not None, f"expected entity in response to {query}, got {resp}"

        for key in variables.keys():
            if key in ["id", "lastchange"]:
                continue
            value = entity[key]
            print("attribute check", type(key), f"[{key}] is {value} ?= {variables[key]}")
            assert value == variables[key], f"test on update failed {value} != {variables[key]}"

        

    return test_update