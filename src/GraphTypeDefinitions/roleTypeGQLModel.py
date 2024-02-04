import datetime
import strawberry
from typing import List, Optional, Union, Annotated
from uoishelpers.resolvers import createInputs


from .BaseGQLModel import BaseGQLModel, IDType
from ._GraphPermissions import (
    RoleBasedPermission, 
    OnlyForAuthentized,
    OnlyForAdmins,
    RBACPermission
)
from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,

    encapsulateInsert,
    encapsulateUpdate,
    encapsulateDelete
)

from src.Dataloaders import (
    getLoadersFromInfo as getLoader,
    getUserFromInfo)
from src.DBResolvers import DBResolvers

RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]
RoleInputWhereFilter = Annotated["RoleInputWhereFilter", strawberry.lazy(".roleGQLModel")]
RoleCategoryGQLModel = Annotated["RoleCategoryGQLModel", strawberry.lazy(".roleCategoryGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a role type (like Dean)"""
)
class RoleTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).RoleTypeModel

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby

    roles = strawberry.field(
        description="""List of roles with this type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DBResolvers.RoleTypeModel.roles(RoleGQLModel, WhereFilterModel=RoleInputWhereFilter)
    )

    category = strawberry.field(
        description="""Get role category of this role type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DBResolvers.RoleTypeModel.category(RoleCategoryGQLModel)
    )

    RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]
    @strawberry.field(
        description="""""",
        permission_classes=[OnlyForAuthentized])
    async def rbacobject(self, info: strawberry.types.Info) -> Optional[RBACObjectGQLModel]:
        from .RBACObjectGQLModel import RBACObjectGQLModel
        result = None if self.createdby is None else await RBACObjectGQLModel.resolve_reference(info, self.createdby)
        return result    
#####################################################################
#
# Special fields for query
#
#####################################################################
from .utils import createInputs
from dataclasses import dataclass

@createInputs
@dataclass
class RoleTypeInputWhereFilter:
    id: IDType
    name: str
    from .roleGQLModel import RoleInputWhereFilter
    roles: RoleInputWhereFilter

role_type_by_id = strawberry.field(
    description="""Finds a role type by its id""",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.RoleTypeModel.resolve_by_id(RoleTypeGQLModel)
)

role_type_page = strawberry.field(
    description="""Finds all role types paged""",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.RoleTypeModel.resolve_page(RoleTypeGQLModel, WhereFilterModel=RoleTypeInputWhereFilter)
)

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime
@strawberry.input(description="")
class RoleTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None

@strawberry.input(description="")
class RoleTypeInsertGQLModel:
    category_id: IDType = None
    id: Optional[IDType] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    createdby: strawberry.Private[IDType] = None
   

@strawberry.type(description="")
class RoleTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of role type operation""")
    async def role_type(self, info: strawberry.types.Info) -> Union[RoleTypeGQLModel, None]:
        result = await RoleTypeGQLModel.resolve_reference(info, self.id)
        return result
    
# class UpdateRoleTypePermission(RBACPermission):
#     message = "User is not allowed create new membership"
#     async def has_permission(self, source, info: strawberry.types.Info, role_type: RoleTypeUpdateGQLModel) -> bool:
#         adminRoleNames = ["administrátor"]
#         allowedRoleNames = []
#         role = await self.resolveUserRole(info, 
#             rbacobject=role_type.id, 
#             adminRoleNames=adminRoleNames, 
#             allowedRoleNames=allowedRoleNames)
        
#         if not role: return False
#         return True

@strawberry.mutation(
    description="""Updates existing roleType record""",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
        # UpdateRoleTypePermission
    ])
async def role_type_update(self, 
    info: strawberry.types.Info, 
    role_type: RoleTypeUpdateGQLModel

) -> RoleTypeResultGQLModel:
    result = await encapsulateUpdate(info, RoleTypeGQLModel.getLoader(info), role_type, RoleTypeResultGQLModel(msg="ok", id=role_type.id))   
    return result

# class InsertRoleTypePermission(RBACPermission):
#     message = "User is not allowed create new membership"
#     async def has_permission(self, source, info: strawberry.types.Info, role_type: RoleTypeInsertGQLModel) -> bool:
#         adminRoleNames = ["administrátor"]
#         allowedRoleNames = []
#         role = await self.resolveUserRole(info, 
#             rbacobject=role_type.id, 
#             adminRoleNames=adminRoleNames, 
#             allowedRoleNames=allowedRoleNames)
        
#         if not role: return False
#         return True

@strawberry.mutation(
    description="""Inserts a new roleType record""",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
        # InsertRoleTypePermission
    ])
async def role_type_insert(self, 
    info: strawberry.types.Info, 
    role_type: RoleTypeInsertGQLModel

) -> RoleTypeResultGQLModel:
    #print("role_type_update", role_type, flush=True)
    return await encapsulateInsert(info, RoleTypeGQLModel.getLoader(info), role_type, RoleTypeResultGQLModel(msg="ok", id=None)) 

@strawberry.mutation(
    description="Deletes the roleType",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def role_type_delete(self, info: strawberry.types.Info, id: IDType) -> RoleTypeResultGQLModel:
    return await encapsulateDelete(info, RoleTypeGQLModel.getLoader(info), id, RoleTypeResultGQLModel(msg="ok", id=None))

