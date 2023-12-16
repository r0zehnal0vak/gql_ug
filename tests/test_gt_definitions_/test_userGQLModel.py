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


test_user_update = createUpdateQuery(tableName="users", query="""mutation ($id: UUID!, $lastchange: DateTime!, $name: String!) {
  result: userUpdate(user: {id: $id, lastchange: $lastchange, name: $name}) {
    id
    user {
      name
      lastchange
    }
  }
}""", variables={"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "name": "newname"})

test_user_insert = createFrontendQuery(query="""mutation ($id: UUID!, $name: String!, $surname: String!, $email: String!) {
  result: userInsert(user: {id: $id, name: $name, surname: $surname, email: $email}) {
    id
    user {
      name
      surname
      email
      lastchange
    }
  }
}""", variables={"id": "850b03cf-a69a-4a6c-b980-1afaf5be174b", "name": "newname", "surname": "surname", "email": "email"})

test_user_larger = createFrontendQuery(query="""query($id: UUID!){
  userById(id: $id) {
    id
    name
    surname
    fullname
    email
    membership {
      id
      valid
    }
    valid
    roles {
      id
    }
    createdby { id }
    changedby { id }
  }
}""", variables={"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"})