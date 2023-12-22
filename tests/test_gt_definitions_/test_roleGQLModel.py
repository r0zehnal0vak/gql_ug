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

# test_role_by_id = createByIdTest(tableName="roles", queryEndpoint="roleById")
# test_role_category_page = createPageTest(tableName="rolecategories", queryEndpoint="roleCategoryPage")
test_role_reference = createResolveReferenceTest(tableName="roles", gqltype="RoleGQLModel", attributeNames=["id"])

test_role_update = createUpdateQuery(tableName="roles", query="""mutation ($id: UUID!, $lastchange: DateTime!, $valid: Boolean!) {
  result: roleUpdate(role: {id: $id, lastchange: $lastchange, valid: $valid}) {
    id
    role {
      valid
      lastchange
    }
  }
}""", variables={"id": "564b62f4-29f6-48b2-8bc8-ff52c800732a", "valid": False})

test_role_insert = createFrontendQuery(query="""mutation($id: UUID!, $userId: UUID!, $groupId: UUID!, $roletypeId: UUID!) {
  roleInsert(role: {id:$id, userId: $userId, groupId: $groupId, roletypeId: $roletypeId}) {
    id
    msg
    role {
        id
        lastchange    
        startdate
        enddate
                                       
        roletype { id }
        user { id }
        group { id }
    }
  }
}""", variables={
    "id": "850b03cf-a69a-4a6c-b980-1afaf5be174b", 
    "userId": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", 
    "groupId": "2d9dcd22-a4a2-11ed-b9df-0242ac120003", 
    "roletypeId": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6"
    })

test_role_larger = createFrontendQuery(query="""query($user_id: UUID!){
  roleByUser(userId: $user_id) {
    id
    group {
      id
    }
    user {
      id
    }
    roletype { id }
  }
}""", variables={"user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"})

test_resolve_roles_on_user = createFrontendQuery(query="""query($user_id: UUID!){
  rolesOnUser(userId: $user_id) {
    id
    group {
      id
    }
    user {
      id
    }
    roletype { id }
    
  }
}""", variables={"user_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"})

test_resolve_roles_on_group = createFrontendQuery(query="""query($group_id: UUID!){
  rolesOnGroup(groupId: $group_id) {
    id
    group {
      id
    }
    user {
      id
    }
    roletype { id }
    
  }
}""", variables={"group_id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003"})

test_resolve_roles_on_group_subgroup = createFrontendQuery(query="""query($group_id: UUID!){
  rolesOnGroup(groupId: $group_id) {
    id
    group {
      id
    }
    user {
      id
    }
    roletype { id }
    
  }
}""", variables={"group_id": "2d9dd1c8-a4a2-11ed-b9df-0242ac120003"})

