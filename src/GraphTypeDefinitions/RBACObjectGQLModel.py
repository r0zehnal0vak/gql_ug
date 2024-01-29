import strawberry
import uuid
import asyncio
from typing import List, Annotated, Optional
from .BaseGQLModel import BaseGQLModel, IDType
from uoishelpers.resolvers import createInputs

from ._GraphResolvers import resolve_id
from ._GraphPermissions import RoleBasedPermission, OnlyForAuthentized
from src.Dataloaders import getLoadersFromInfo as getLoader

RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]

#@strawberry.federation.type(extend=False, keys=["id"])
@strawberry.federation.type(keys=["id"])
class RBACObjectGQLModel:

    id = resolve_id
    asUser: strawberry.Private[bool] = False
    asGroup: strawberry.Private[bool] = False
    
    @classmethod
    async def resolve_roles(info: strawberry.types.Info, id: IDType):
        from .roleGQLModel import resolve_roles_on_user, resolve_roles_on_group
        from ._GraphPermissions import RBACPermission
        awaitableresult0 = resolve_roles_on_user(None, info, user_id=id)
        awaitableresult1 = resolve_roles_on_group(None, info, group_id=id)
        result0, result1 = await asyncio.gather(awaitableresult0, awaitableresult1)
        roles = [*result0, *result1]
        allRoleTypes = RBACPermission.getAllRoles()
        index = {roleType["id"]: roleType for roleType in allRoleTypes}
        extresult = [
            {
                "id": r.id,
                "user_id": r.user_id,
                "group_id": r.group_id,
                "roletype_id": r.roletype_id,
                "type": index[r.roletype_id]
            } for r in roles
        ]
        return extresult

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: IDType):
        from .groupGQLModel import GroupGQLModel
        from .userGQLModel import UserGQLModel
        if id is None: return None
                
        if isinstance(id, str): id = IDType(id)

        loaderU = UserGQLModel.getLoader(info)
        loaderG = GroupGQLModel.getLoader(info)
        futures = [loaderU.load(id), loaderG.load(id)]
        rows = await asyncio.gather(*futures)

        asUser = rows[0] is not None
        asGroup = rows[1] is not None

        if asUser is None and asGroup is None: return None
        
        result = RBACObjectGQLModel(asGroup=asGroup, asUser=asUser)
        result.id = id
        return result

    @strawberry.field(
        description="Roles associated with this RBAC",
        permission_classes=[OnlyForAuthentized])
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        from .roleGQLModel import resolve_roles_on_user, resolve_roles_on_group
        result = []
        if self.asUser:
            result = await resolve_roles_on_user(self, info, user_id=self.id)
        if self.asGroup:
            result = await resolve_roles_on_group(self, info, group_id=self.id)
        return result
    
@strawberry.field(
    description="""Finds a rbasobject by its id""",
    permission_classes=[OnlyForAuthentized])
async def rbac_by_id(
    self, info: strawberry.types.Info, id: IDType
) -> Optional["RBACObjectGQLModel"]:
    result = await RBACObjectGQLModel.resolve_reference(info=info, id=id)
    return result
