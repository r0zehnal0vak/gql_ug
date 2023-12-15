from ..gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery
)

test_user_by_id = createByIdTest(tableName="users", queryEndpoint="userById", attributeNames=["id", "name", "surname", "email"])
test_user_page = createPageTest(tableName="users", queryEndpoint="userPage")
test_user_reference = createResolveReferenceTest(tableName="users", gqltype="UserGQLModel")

test_user_larger = createFrontendQuery(query="""query($id: UUID!){
  userById(id: $id) {
    id
    name
    surname
    email
    membership {
      id
      valid
    }
    valid
    roles {
      id
    }
    
  }
}""", variables={"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"})