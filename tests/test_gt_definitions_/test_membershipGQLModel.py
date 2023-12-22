# from ..gqlshared import (
#     createByIdTest,
#     createPageTest,
#     createResolveReferenceTest,
#     createFrontendQuery,
#     createUpdateQuery
# )
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_membership_by_id = createByIdTest(tableName="memberships", queryEndpoint="membershipById", attributeNames=["id"])
# test_user_page = createPageTest(tableName="groups", queryEndpoint="groupPage")
test_membership_reference = createResolveReferenceTest(tableName="memberships", gqltype="MembershipGQLModel", attributeNames=["id"])

test_membership_larger = createFrontendQuery(query="""query($id: UUID!){
  userById(id: $id) {
    id
    membership {
      id
      valid
      user { id }   
      group { id }
      startdate
      enddate
    }
  }
}""", variables={"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"})

test_membership_insert = createFrontendQuery(query="""mutation($user_id: UUID!, $group_id: UUID!) {
  membershipInsert(membership: {userId: $user_id, groupId: $group_id}) {
    id
    msg
    membership {
      id
      lastchange
    }
  }
}""", variables={
    "id": "850b03cf-a69a-4a6c-b980-1afaf5be174b", 
    "user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", 
    "group_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003", 
    "roletypeId": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6"})

test_membership_update = createUpdateQuery(
    tableName="memberships", 
    query="""mutation($id: UUID!, $valid: Boolean!, $lastchange: DateTime!) {
  membershipUpdate(membership: {id: $id, valid: $valid, lastchange: $lastchange}) {
    id
    msg
    membership {
      id
      lastchange
    }
  }
}""",
    variables={"id": "7cea8596-a4a2-11ed-b9df-0242ac120003", "valid": False})