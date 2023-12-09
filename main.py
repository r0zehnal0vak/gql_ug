import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from gql_ug.DBDefinitions import startEngine, ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
from gql_ug.DBFeeder import initDB

connectionString = ComposeConnectionString()

appcontext = {}
@asynccontextmanager
async def initEngine(app: FastAPI):

    from gql_ug.DBDefinitions import startEngine, ComposeConnectionString

    connectionstring = ComposeConnectionString()

    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring,
        makeDrop=True,
        makeUp=True
    )

    appcontext["asyncSessionMaker"] = asyncSessionMaker

    logging.info("engine started")

    from gql_ug.DBFeeder import initDB
    await initDB(asyncSessionMaker)

    logging.info("data (if any) imported")
    yield


from gql_ug.GraphTypeDefinitions import schema

async def get_context():
    asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
    if asyncSessionMaker is None:
        async with initEngine(app) as cntx:
            pass
        
    from gql_ug.Dataloaders import createLoadersContext
    context = createLoadersContext(appcontext["asyncSessionMaker"])
    return {**context}


def createApp():
    app = FastAPI(lifespan=initEngine)



    graphql_app = GraphQLRouter(
        schema,
        context_getter=get_context
    )
    app.include_router(graphql_app, prefix="/gql")

    # voyager je na stejne ceste jako gql, proto musi byt v kodu drive
    from doc import attachVoyager
    # attachVoyager(app, path="/gql/doc")

    def introspection():
        introspectionQuery =  "query __ApolloGetServiceDefinition__ { _service { sdl } }"
        introspectionResult = schema.execute_sync(introspectionQuery, operation_name="__ApolloGetServiceDefinition__")
        assert introspectionResult.errors is None
        introspectionResult = {"data": introspectionResult.data}
        return JSONResponse(introspectionResult) 

    @app.post("/introspection")
    def i():
        return introspection()
    
    @app.get("/introspection")
    def i():
        return introspection()

    @app.post("/")
    def hello():
        return {"hello": "world"}
    
    return app

app = createApp()

print("All initialization is done")

import os
from uoishelpers.authenticationMiddleware import BasicAuthBackend, BasicAuthenticationMiddleware302

JWTPUBLICKEY = os.environ.get("JWTPUBLICKEY", "http://localhost:8000/oauth/publickey")
JWTRESOLVEUSERPATH = os.environ.get("JWTRESOLVEUSERPATH", "http://localhost:8000/oauth/userinfo")

# app.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY, JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))
