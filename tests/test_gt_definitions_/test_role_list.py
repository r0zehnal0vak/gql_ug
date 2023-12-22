from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_role_type_list_add = createFrontendQuery(query="""mutation ($role_type_list_id: UUID!, $role_type_id: UUID!) {
  list: roleTypeListAddRole(roleTypeListId: $role_type_list_id, roleTypeId: $role_type_id) {
    id
    roleTypes {
      id
      name
    }
    
  }
}""", variables={"role_type_list_id": "014aadd0-25e7-4a25-a05a-e5cc30b1aea1", "role_type_id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6"})

