import datetime
import strawberry
import uuid
from typing import List, Optional, Union, Annotated
import src.GraphTypeDefinitions
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

from src.Dataloaders import (
    getLoadersFromInfo as getLoader,
    getUserFromInfo)

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".userGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class MembershipGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoader(info).memberships

    id = resolve_id
    changedby = resolve_changedby
    created = resolve_created
    lastchange = resolve_lastchange
    createdby = resolve_createdby

    @strawberry.field(
        description="""user""",
        permission_classes=[OnlyForAuthentized()])
    async def user(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        # return self.user
        result = await src.GraphTypeDefinitions.UserGQLModel.resolve_reference(info=info, id=self.user_id)
        return result

    @strawberry.field(
        description="""group""",
        permission_classes=[OnlyForAuthentized()])
    async def group(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        # return self.group
        result = await src.GraphTypeDefinitions.GroupGQLModel.resolve_reference(info=info, id=self.group_id)
        return result

    @strawberry.field(
        description="""is the membership is still valid""",
        permission_classes=[OnlyForAuthentized()])
    async def valid(self) -> Union[bool, None]:
        return self.valid

    @strawberry.field(
        description="""date when the membership begins""",
        permission_classes=[OnlyForAuthentized()])
    async def startdate(self) -> Union[datetime.datetime, None]:
        return self.startdate

    @strawberry.field(
        description="""date when the membership ends""",
        permission_classes=[OnlyForAuthentized()])
    async def enddate(self) -> Union[datetime.datetime, None]:
        return self.enddate

    RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]
    @strawberry.field(
        description="""""",
        permission_classes=[OnlyForAuthentized()])
    async def rbacobject(self, info: strawberry.types.Info) -> Optional[RBACObjectGQLModel]:
        from .RBACObjectGQLModel import RBACObjectGQLModel
        result = None if self.rbacobject is None else await RBACObjectGQLModel.resolve_reference(info, self.group_id)
        return result    

#####################################################################
#
# Special fields for query
#
#####################################################################
from .utils import createInputs
from dataclasses import dataclass
GroupInputWhereFilter = Annotated["GroupInputWhereFilter", strawberry.lazy(".groupGQLModel")]
UserInputWhereFilter = Annotated["UserInputWhereFilter", strawberry.lazy(".userGQLModel")]
@createInputs
@dataclass
class MembershipInputWhereFilter:
    valid: bool
    # from .userGQLModel import UserInputWhereFilter
    # from .groupGQLModel import GroupInputWhereFilter
    group: GroupInputWhereFilter
    user: UserInputWhereFilter

from ._GraphResolvers import asPage

@strawberry.field(
    description="Retrieves memberships",
    permission_classes=[OnlyForAuthentized(isList=True)])
@asPage
async def membership_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[MembershipInputWhereFilter]= None
    ) -> List[MembershipGQLModel]: 
    return getLoader(info).memberships

@strawberry.field(
    description="Retrieves the membership",
    permission_classes=[OnlyForAuthentized()])
async def membership_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> Optional[MembershipGQLModel]:
    return await MembershipGQLModel.resolve_reference(info, id)


#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input
class MembershipUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime   
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.input
class MembershipInsertGQLModel:
    user_id: IDType
    group_id: IDType
    id: Optional[uuid.UUID] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    createdby: strawberry.Private[uuid.UUID] = None

@strawberry.type
class MembershipResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of membership operation""")
    async def membership(self, info: strawberry.types.Info) -> Union[MembershipGQLModel, None]:
        result = await MembershipGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="""Update the membership, cannot update group / user""",
    permission_classes=[OnlyForAuthentized()])
async def membership_update(self, 
    info: strawberry.types.Info, 
    membership: "MembershipUpdateGQLModel"
) -> "MembershipResultGQLModel":
    user = getUserFromInfo(info)
    membership.changedby = user["id"]
    loader = getLoader(info).memberships
    updatedrow = await loader.update(membership)

    result = MembershipResultGQLModel()
    result.id = membership.id
    result.msg = "fail" if updatedrow is None else "ok"
    
    return result


@strawberry.mutation(
    description="""Inserts new membership""",
    permission_classes=[OnlyForAuthentized()])
async def membership_insert(self, 
    info: strawberry.types.Info, 
    membership: "MembershipInsertGQLModel"
) -> "MembershipResultGQLModel":
    user = getUserFromInfo(info)
    membership.createdby = user["id"]
    
    loader = getLoader(info).memberships
    row = await loader.insert(membership)

    result = MembershipResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    
    return result