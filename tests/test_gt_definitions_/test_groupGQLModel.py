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

test_group_by_id = createByIdTest(tableName="groups", queryEndpoint="groupById")
test_group_page = createPageTest(tableName="groups", queryEndpoint="groupPage")
test_group_reference = createResolveReferenceTest(tableName="groups", gqltype="GroupGQLModel")

test_group_update = createUpdateQuery(tableName="groups", query="""mutation ($id: UUID!, $lastchange: DateTime!, $name: String!) {
  result: groupUpdate(group: {id: $id, lastchange: $lastchange, name: $name}) {
    id
    group {
      name
      lastchange
    }
  }
}""", variables={"id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003", "name": "newname"})

test_group_insert = createFrontendQuery(query="""mutation ($id: UUID!, $name: String!) {
  result: groupInsert(group: {id: $id, name: $name}) {
    id
    group {
      name
      lastchange
      valid
    }
  }
}""", variables={"id": "850b03cf-a69a-4a6c-b980-1afaf5be174b", "name": "newname"})

test_group_larger = createFrontendQuery(query="""query($id: UUID!){
  groupById(id: $id) {
    id
    name
    memberships {
      id
      valid
    }
    valid
    roles {
      id
    }
    grouptype { id }
    subgroups { id }
    mastergroup { id }
  }
}""", variables={"id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003"})