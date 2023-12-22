import datetime
import strawberry
import asyncio
import uuid
from typing import List, Optional, Union, Annotated
import gql_ug.GraphTypeDefinitions
from .BaseGQLModel import BaseGQLModel, IDType
from ._GraphPermissions import RoleBasedPermission, OnlyForAuthentized
from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby
)

from gql_ug.Dataloaders import getLoadersFromInfo as getLoader

def getUser(info):
    return info.context["user"]


MembershipGQLModel = Annotated["MembershipGQLModel", strawberry.lazy(".membershipGQLModel")]
RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]
GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]


from ..GraphPermissions import UserGDPRPermission

@strawberry.federation.type(keys=["id"], description="""Entity representing a user""")
class UserGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).users

    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby

    @strawberry.field(
        description="""User's family name (like Obama)""",
        permission_classes=[OnlyForAuthentized()])
    def surname(self) -> Optional[str]:
        return self.surname

    @strawberry.field(
        description="""User's family name (like Obama)""",
        permission_classes=[OnlyForAuthentized()])
    def fullname(self) -> Optional[str]:
        return self.fullname

    @strawberry.field(
        description="""User's email""",
        permission_classes=[OnlyForAuthentized()])
    def email(self) -> Optional[str]:
        return self.email

    @strawberry.field(
        description="""User's validity (if their are member of institution)""",
        permission_classes=[OnlyForAuthentized()])
    def valid(self) -> Optional[bool]:
        return self.valid

    @strawberry.field(
        description="""GDPRInfo for permision test""", permission_classes=[UserGDPRPermission],
        permission_classes=[OnlyForAuthentized()])
    def GDPRInfo(self, info: strawberry.types.Info) -> Union[str, None]:
        actinguser = getUser(info)
        print(actinguser)
        return "GDPRInfo"

    @strawberry.field(
        description="""List of groups, where the user is member""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def membership(
        self, info: strawberry.types.Info
    ) -> List["MembershipGQLModel"]:
        loader = getLoader(info).memberships
        result = await loader.filter_by(user_id=self.id)
        return list(result)

    @strawberry.field(
        description="""List of roles, which the user has""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        loader = getLoader(info).roles
        result = await loader.filter_by(user_id=self.id)
        return result

    @strawberry.field(
        description="""List of groups given type, where the user is member""",
        permission_classes=[OnlyForAuthentized(isList=True)])
    async def member_of(
        self, grouptype_id: IDType, info: strawberry.types.Info
    ) -> List["GroupGQLModel"]:
        loader = getLoader(info).memberships
        rows = await loader.filter_by(user_id=self.id)# , grouptype_id=grouptype_id)
        results = (gql_ug.GraphTypeDefinitions.GroupGQLModel.resolve_reference(info, row.group_id) for row in rows)
        results = await asyncio.gather(*results)
        results = filter(lambda item: item.grouptype_id == grouptype_id, results)
        return results

#####################################################################
#
# Special fields for query
#
#####################################################################

from .utils import createInputs
from dataclasses import dataclass
#MembershipInputWhereFilter = Annotated["MembershipInputWhereFilter", strawberry.lazy(".membershipGQLModel")]

from ._GraphResolvers import createRootResolver_by_id
user_by_id = createRootResolver_by_id(
    scalarType=UserGQLModel, 
    description="Returns a list of users (paged)")

@createInputs
@dataclass
class UserInputWhereFilter:
    name: str
    surname: str
    email: str
    fullname: str
    valid: bool
    from .membershipGQLModel import MembershipInputWhereFilter
    memberships: MembershipInputWhereFilter

from ._GraphResolvers import createRootResolver_by_page
user_page = createRootResolver_by_page(
    scalarType=UserGQLModel,
    whereFilterType=UserInputWhereFilter,
    description="Returns a list of users (paged)",
    loaderLambda=lambda info: getLoader(info).users
)

# @strawberry.field(description="""Returns a list of users (paged)""")
# async def user_page(
#     self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
#     where: Optional[UserInputWhereFilter] = None,
#     order_by: Optional[str] = None,
#     desc: Optional[bool] = None
# ) -> List[UserGQLModel]:
#     wheredict = None if where is None else strawberry.asdict(where)
#     loader = getLoader(info).users
#     result = await loader.page(skip, limit, where=wheredict, orderby=order_by, desc=desc)
#     return result

# @strawberry.field(description="""Finds an user by their id""")
# async def user_by_id(
#     self, info: strawberry.types.Info, id: IDType
# ) -> Union[UserGQLModel, None]:
#     result = await UserGQLModel.resolve_reference(info=info, id=id)
#     return result

@strawberry.field(
    description="""Finds an user by letters in name and surname, letters should be atleast three""",
    permission_classes=[OnlyForAuthentized()])
async def user_by_letters(
    self,
    info: strawberry.types.Info,
    validity: Union[bool, None] = None,
    letters: str = "",
) -> List[UserGQLModel]:
    loader = getLoader(info).users

    if len(letters) < 3:
        return []
    stmt = loader.getSelectStatement()
    model = loader.getModel()
    stmt = stmt.where((model.name + " " + model.surname).like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    result = await loader.execute_select(stmt)
    return result

# from gql_ug.GraphResolvers import UserByRoleTypeAndGroupStatement

# @strawberry.field(description="""Finds users who plays in a group a roletype""")
# async def users_by_group_and_role_type(
#     self,
#     info: strawberry.types.Info,
#     group_id: IDType,
#     role_type_id: IDType,
# ) -> List[UserGQLModel]:
#     # result = await resolveUserByRoleTypeAndGroup(session,  group_id, role_type_id)
#     loader = getLoader(info).users
#     result = await loader.execute_select(UserByRoleTypeAndGroupStatement)
#     return result


#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input
class UserUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime  # razitko
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    valid: Optional[bool] = None

@strawberry.input
class UserInsertGQLModel:
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    valid: Optional[bool] = None

@strawberry.type
class UserResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of user operation""")
    async def user(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
        result = await UserGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(
    description="",
    permission_classes=[OnlyForAuthentized()])
async def user_update(self, info: strawberry.types.Info, user: UserUpdateGQLModel) -> UserResultGQLModel:
    #print("user_update", flush=True)
    #print(user, flush=True)
    loader = getLoader(info).users
    
    updatedrow = await loader.update(user)
    #print("user_update", updatedrow, flush=True)
    result = UserResultGQLModel()
    result.id = user.id

    result.msg = "fail" if updatedrow is None else "ok"
    # print("user_update", result.msg, flush=True)
    return result

@strawberry.mutation(
    description="",
    permission_classes=[OnlyForAuthentized()])
async def user_insert(self, info: strawberry.types.Info, user: UserInsertGQLModel) -> UserResultGQLModel:
    loader = getLoader(info).users
    
    row = await loader.insert(user)

    result = UserResultGQLModel()
    result.id = row.id
    result.msg = "ok"
    
    return result
