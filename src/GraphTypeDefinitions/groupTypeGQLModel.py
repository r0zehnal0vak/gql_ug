import datetime
import strawberry
import uuid
from typing import List, Optional, Union, Annotated, ForwardRef
from uoishelpers.resolvers import createInputs

from .BaseGQLModel import BaseGQLModel, IDType
from ._GraphPermissions import (
    RoleBasedPermission, 
    OnlyForAuthentized,
    RBACPermission,
    OnlyForAdmins
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
    encapsulateUpdate    
)

from src.Dataloaders import (
    getLoadersFromInfo as getLoader,
    getUserFromInfo)
from src.DBResolvers import DBResolvers

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
GroupCategoryGQLModel = Annotated["GroupCategoryGQLModel", strawberry.lazy(".groupCategoryGQLModel")]
RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]

# GroupTypeGQLModelResolvers = DBResolvers.GroupTypeModel(ForwardRef("GroupTypeGQLModel"))

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a group type (like Faculty)"""
)
class GroupTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        # return getLoader(info).grouptypes
        return getLoader(info).GroupTypeModel
        
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby

    groups = strawberry.field(
        description="""Groups which has this type""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DBResolvers.GroupTypeModel.groups(GroupGQLModel)
    )

    category = strawberry.field(
        description="""Group category which this type belongs to""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=DBResolvers.GroupTypeModel.category(GroupCategoryGQLModel)
    )

    @strawberry.field(
        description="""""",
        permission_classes=[
            OnlyForAuthentized
        ])
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
# MembershipInputWhereFilter = Annotated["MembershipInputWhereFilter", strawberry.lazy(".membershipGQLModel")]
@createInputs
@dataclass
class GroupTypeInputWhereFilter:
    id: IDType
    name: str
    category_id: IDType
    # from .membershipGQLModel import MembershipInputWhereFilter
    # memberships: MembershipInputWhereFilter

# from ._GraphResolvers import asPage


group_type_page = strawberry.field(
    description="""Returns a list of groups types (paged)""",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.GroupTypeModel.resolve_page(GroupTypeGQLModel, WhereFilterModel=GroupTypeInputWhereFilter)
)

group_type_by_id = strawberry.field(
    description="""Finds a group type by its id""",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.GroupTypeModel.resolve_by_id(GroupTypeGQLModel)
)

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="")
class GroupTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None

@strawberry.input(description="")
class GroupTypeInsertGQLModel:
    id: Optional[IDType] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    createdby: strawberry.Private[IDType] = None

@strawberry.type(description="")
class GroupTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of grouptype operation""")
    async def group_type(self, info: strawberry.types.Info) -> Union[GroupTypeGQLModel, None]:
        result = await GroupTypeGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="""Allows a update of group, also it allows to change the mastergroup of the group""",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def group_type_update(self, info: strawberry.types.Info, group_type: GroupTypeUpdateGQLModel) -> GroupTypeResultGQLModel:
    return await encapsulateUpdate(info, GroupTypeGQLModel.getLoader(info), group_type, GroupTypeResultGQLModel(id=group_type.id, msg="ok"))

@strawberry.mutation(
    description="""Inserts a group""",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def group_type_insert(self, info: strawberry.types.Info, group_type: GroupTypeInsertGQLModel) -> GroupTypeResultGQLModel:
    return await encapsulateInsert(info, GroupTypeGQLModel.getLoader(info), group_type, GroupTypeResultGQLModel(id=None, msg="ok"))
