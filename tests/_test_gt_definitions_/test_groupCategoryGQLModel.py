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

tableName = "groupcategories"
queryEndpointPrefix = "groupCategory"

test_groupcategory_by_id = createByIdTest(tableName=tableName, queryEndpoint=f"{queryEndpointPrefix}ById")
test_groupcategory_page = createPageTest(tableName=tableName, queryEndpoint=f"{queryEndpointPrefix}Page")
test_groupcategory_reference = createResolveReferenceTest(tableName=tableName, gqltype="GroupCategoryGQLModel")

test_group_category_update = createUpdateQuery(tableName=tableName, query="""mutation ($id: UUID!, $lastchange: DateTime!, $name: String!) {
  result: groupCategoryUpdate(groupType: {id: $id, lastchange: $lastchange, name: $name}) {
    id
    groupCategory {
      name
      lastchange
      rbacobject { id }
    }
  }
}""", variables={"id": "be2b2dcc-4bfe-4035-99e8-dd6d6f01562e", "name": "newname"})

test_group_category_insert = createFrontendQuery(query="""mutation ($id: UUID!, $name: String!) {
  result: groupCategoryInsert(groupType: {id: $id, name: $name}) {
    id
    groupCategory {
      name
      lastchange
      
    }
  }
}""", variables={"id": "91e52e78-a707-4c3d-880a-1f414d8da72e", "name": "newname"})