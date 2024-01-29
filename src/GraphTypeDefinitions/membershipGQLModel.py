import datetime
import strawberry
import uuid
from typing import List, Optional, Union, Annotated
from uoishelpers.resolvers import createInputs

from .BaseGQLModel import BaseGQLModel, IDType
from ._GraphPermissions import (
    RoleBasedPermission, OnlyForAuthentized,
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
    encapsulateUpdate
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
        permission_classes=[OnlyForAuthentized])
    async def user(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .userGQLModel import UserGQLModel
        # return self.user
        result = await UserGQLModel.resolve_reference(info=info, id=self.user_id)
        return result

    @strawberry.field(
        description="""group""",
        permission_classes=[OnlyForAuthentized])
    async def group(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        from .groupGQLModel import GroupGQLModel
        # return self.group
        result = await GroupGQLModel.resolve_reference(info=info, id=self.group_id)
        return result

    @strawberry.field(
        description="""is the membership is still valid""",
        permission_classes=[OnlyForAuthentized])
    async def valid(self) -> Union[bool, None]:
        return self.valid

    @strawberry.field(
        description="""date when the membership begins""",
        permission_classes=[OnlyForAuthentized])
    async def startdate(self) -> Union[datetime.datetime, None]:
        return self.startdate

    @strawberry.field(
        description="""date when the membership ends""",
        permission_classes=[OnlyForAuthentized])
    async def enddate(self) -> Union[datetime.datetime, None]:
        return self.enddate

    RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".RBACObjectGQLModel")]
    @strawberry.field(
        description="""""",
        permission_classes=[OnlyForAuthentized])
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
    permission_classes=[OnlyForAuthentized])
@asPage
async def membership_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: Optional[MembershipInputWhereFilter]= None
    ) -> List[MembershipGQLModel]: 
    return getLoader(info).memberships

@strawberry.field(
    description="Retrieves the membership",
    permission_classes=[OnlyForAuthentized])
async def membership_by_id(
    self, info: strawberry.types.Info, id: IDType
) -> Optional[MembershipGQLModel]:
    return await MembershipGQLModel.resolve_reference(info, id)


#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input(description="")
class MembershipUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime   
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    changedby: strawberry.Private[IDType] = None

@strawberry.input(description="")
class MembershipInsertGQLModel:
    user_id: IDType
    group_id: IDType
    id: Optional[IDType] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    createdby: strawberry.Private[IDType] = None

@strawberry.type(description="")
class MembershipResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of membership operation""")
    async def membership(self, info: strawberry.types.Info) -> Union[MembershipGQLModel, None]:
        result = await MembershipGQLModel.resolve_reference(info, self.id)
        return result
    
class UpdateMembershipPermission(RBACPermission):
    message = "User is not allowed to change membership"
    async def has_permission(self, source, info: strawberry.types.Info, membership: "MembershipInsertGQLModel") -> bool:
        adminRoleNames = ["administrátor"]
        allowedRoleNames = ["garant"]
        role = await self.resolveUserRole(info, 
            rbacobject=membership.group_id,
            adminRoleNames=adminRoleNames, 
            allowedRoleNames=allowedRoleNames)
        
        if not role: return False
        # roleTypeName = role["type"]["name"]
        # if roleTypeName in allowedRoleNames:
        #     if group.mastergroup_id:
        #         raise self.error_class(f"{roleTypeName} cannot change mastergroup_id")
        #     if group.grouptype_id:
        #         raise self.error_class(f"{roleTypeName} cannot change grouptype_id")
        return True


@strawberry.mutation(
    description="""Update the membership, cannot update group / user""",
    permission_classes=[
        OnlyForAuthentized,
        UpdateMembershipPermission
    ])
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

class InsertMembershipPermission(RBACPermission):
    message = "User is not allowed create new membership"
    async def has_permission(self, source, info: strawberry.types.Info, membership: "MembershipInsertGQLModel") -> bool:
        adminRoleNames = ["administrátor"]
        allowedRoleNames = ["garant"]
        role = await self.resolveUserRole(info, 
            rbacobject=membership.group_id, 
            adminRoleNames=adminRoleNames, 
            allowedRoleNames=allowedRoleNames)
        
        if not role: return False
        return True

@strawberry.mutation(
    description="""Inserts new membership""",
    permission_classes=[
        OnlyForAuthentized,
        InsertMembershipPermission
    ])
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