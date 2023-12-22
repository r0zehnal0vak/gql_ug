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

test_role_category_by_id = createByIdTest(tableName="rolecategories", queryEndpoint="roleCategoryById")
test_role_category_page = createPageTest(tableName="rolecategories", queryEndpoint="roleCategoryPage")
test_role_category_reference = createResolveReferenceTest(tableName="rolecategories", gqltype="RoleCategoryGQLModel")

test_role_category_update = createUpdateQuery(tableName="rolecategories", query="""mutation ($id: UUID!, $lastchange: DateTime!, $name: String!) {
  result: roleCategoryUpdate(roleCategory: {id: $id, lastchange: $lastchange, name: $name}) {
    id
    roleCategory {
      name
      lastchange
    }
  }
}""", variables={"id": "fd73596b-1043-46f0-837a-baa0734d64df", "name": "newname"})

test_role_category_insert = createFrontendQuery(query="""mutation ($id: UUID!, $name: String!) {
  result: roleCategoryInsert(roleCategory: {id: $id, name: $name}) {
    id
    roleCategory {
      name
      lastchange
      roleTypes { id }
    }
  }
}""", variables={"id": "aba66774-b7c3-4f13-adf9-7ee89d5986a7", "name": "newname"})