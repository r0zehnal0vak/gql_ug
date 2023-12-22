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

test_grouptype_by_id = createByIdTest(tableName="grouptypes", queryEndpoint="groupTypeById")
test_grouptype_page = createPageTest(tableName="grouptypes", queryEndpoint="groupTypePage")
test_user_reference = createResolveReferenceTest(tableName="grouptypes", gqltype="GroupTypeGQLModel")

test_group_type_update = createUpdateQuery(tableName="grouptypes", query="""mutation ($id: UUID!, $lastchange: DateTime!, $name: String!) {
  result: groupTypeUpdate(groupType: {id: $id, lastchange: $lastchange, name: $name}) {
    id
    groupType {
      name
      lastchange
    }
  }
}""", variables={"id": "cd49e152-610c-11ed-9f29-001a7dda7110", "name": "newname"})

test_group_type_insert = createFrontendQuery(query="""mutation ($id: UUID!, $name: String!) {
  result: groupTypeInsert(groupType: {id: $id, name: $name}) {
    id
    groupType {
      name
      lastchange
      groups { id }
    }
  }
}""", variables={"id": "850b03cf-a69a-4a6c-b980-1afaf5be174b", "name": "newname"})