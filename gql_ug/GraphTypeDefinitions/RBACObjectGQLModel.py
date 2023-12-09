import strawberry
import uuid
import asyncio
from typing import List, Annotated, Optional
from .BaseGQLModel import BaseGQLModel, IDType
from ._GraphResolvers import resolve_id

from gql_ug.Dataloaders import getLoadersFromInfo as getLoader

RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]

#@strawberry.federation.type(extend=False, keys=["id"])
@strawberry.federation.type(keys=["id"])
class RBACObjectGQLModel:

    id = resolve_id
    asUser: strawberry.Private[bool] = False
    asGroup: strawberry.Private[bool] = False

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: IDType):
        if id is None:
            return None
        if isinstance(id, str): id = uuid.UUID(id)

        loaderU = getLoader(info).users
        loaderG = getLoader(info).groups
        futures = [loaderU.load(id), loaderG.load(id)]
        rows = await asyncio.gather(*futures)

        asUser = False
        asGroup = False
        if rows[0] is not None:
            asUser = True
        if rows[1] is not None:
            asGroup = True

        if asUser is None and asGroup is None:
            return None
        
        result = RBACObjectGQLModel(asGroup=asGroup, asUser=asUser)
        result.id = id
        return result

    @strawberry.field()
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        from .roleGQLModel import resolve_roles_on_user, resolve_roles_on_group
        result = []
        if self.asUser:
            result = await resolve_roles_on_user(self, info, user_id=self.id)
        if self.asGroup:
            result = await resolve_roles_on_group(self, info, group_id=self.id)
        return result
    
@strawberry.field(description="""Finds an user by their id""")
async def rbac_by_id(
    self, info: strawberry.types.Info, id: IDType
) -> Optional["RBACObjectGQLModel"]:
    result = await RBACObjectGQLModel.resolve_reference(info=info, id=id)
    return result
