import datetime
import strawberry
import uuid
from typing import List, Optional, Union, Annotated
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
    encapsulateUpdate,
    encapsulateDelete
)

from src.Dataloaders import (
    getLoadersFromInfo as getLoader,
    getUserFromInfo)
from src.DBResolvers import DBResolvers

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a group type (like Faculty)"""
)
class GroupCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).GroupCategoryModel
        
    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby

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
# MembershipInputWhereFilter = Annotated["MembershipInputWhereFilter", strawberry.lazy(".membershipGQLModel")]
@createInputs
@dataclass
class GroupCategoryInputWhereFilter:
    id: IDType
    name: str
    # valid: bool
    # from .membershipGQLModel import MembershipInputWhereFilter
    # memberships: MembershipInputWhereFilter

# @strawberry.field(
#     description="""Returns a list of groups types (paged)""",
#     permission_classes=[OnlyForAuthentized])
# async def group_type_page(
#     self, info: strawberry.types.Info, skip: int = 0, limit: int = 20,
#     where: Optional[GroupCategoryInputWhereFilter] = None
# ) -> List[GroupCategoryGQLModel]:
#     wheredict = None if where is None else strawberry.asdict(where)
#     loader = getLoader(info).groupcategorys
#     result = await loader.page(skip, limit, where=wheredict)
#     return result

# from ._GraphResolvers import asPage

# @strawberry.field(
#     description="""Returns a list of groups categories (paged)""",
#     permission_classes=[OnlyForAuthentized])
# @asPage
# async def group_category_page(
#     self, info: strawberry.types.Info, skip: int = 0, limit: int = 20,
#     where: Optional[GroupCategoryInputWhereFilter] = None
# ) -> List[GroupCategoryGQLModel]:
#     loader = GroupCategoryGQLModel.getLoader(info)
#     return loader


group_category_page = strawberry.field(
    description="""Returns a list of groups categories (paged)""",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.GroupCategoryModel.resolve_page(GroupCategoryGQLModel, GroupCategoryInputWhereFilter)
)

# @strawberry.field(
#     description="""Finds a group category by its id""",
#     permission_classes=[OnlyForAuthentized])
# async def group_category_by_id(
#     self, info: strawberry.types.Info, id: IDType
# ) -> Union[GroupCategoryGQLModel, None]:
#     # result = await resolveGroupCategoryById(session,  id)
#     result = await GroupCategoryGQLModel.resolve_reference(info, id)
#     return result


group_category_by_id = strawberry.field(
    description="""Finds a group category by its id""",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.GroupCategoryModel.resolve_by_id(GroupCategoryGQLModel)
)

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="")
class GroupCategoryUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None

@strawberry.input(description="")
class GroupCategoryInsertGQLModel:
    id: Optional[IDType] = None
    name: Optional[str] = None
    name_en: Optional[str] = None
    createdby: strawberry.Private[IDType] = None

@strawberry.type(description="")
class GroupCategoryResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of groupcategory operation""")
    async def group_category(self, info: strawberry.types.Info) -> Union[GroupCategoryGQLModel, None]:
        result = await GroupCategoryGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="""Allows an update of group category""",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def group_category_update(self, info: strawberry.types.Info, group_type: GroupCategoryUpdateGQLModel) -> GroupCategoryResultGQLModel:
    return await encapsulateUpdate(info, GroupCategoryGQLModel.getLoader(info), group_type, GroupCategoryResultGQLModel(id=group_type.id, msg="ok"))

@strawberry.mutation(
    description="""Inserts a group category""",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def group_category_insert(self, info: strawberry.types.Info, group_type: GroupCategoryInsertGQLModel) -> GroupCategoryResultGQLModel:
    return await encapsulateInsert(info, GroupCategoryGQLModel.getLoader(info), group_type, GroupCategoryResultGQLModel(id=None, msg="ok"))

@strawberry.mutation(
    description="Deletes the group category",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def group_type_delete(self, info: strawberry.types.Info, id: IDType) -> GroupCategoryResultGQLModel:
    return await encapsulateDelete(info, GroupCategoryGQLModel.getLoader(info), id, GroupCategoryResultGQLModel(msg="ok", id=None))

