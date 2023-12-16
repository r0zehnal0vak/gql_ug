from ..gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery
)

test_roleType_by_id = createByIdTest(tableName="roletypes", queryEndpoint="roleTypeById")
test_role_type_page = createPageTest(tableName="roletypes", queryEndpoint="roleTypePage")
test_role_type_reference = createResolveReferenceTest(tableName="roletypes", gqltype="RoleTypeGQLModel")

test_role_type_update = createUpdateQuery(tableName="roletypes", query="""mutation ($id: UUID!, $lastchange: DateTime!, $name: String!) {
  result: roleTypeUpdate(roleType: {id: $id, lastchange: $lastchange, name: $name}) {
    id
    roleType {
      name
      lastchange
    }
  }
}""", variables={"id": "05a3e0f5-f71e-4caa-8012-229d868aa8ca", "name": "newname"})

test_role_type_insert = createFrontendQuery(query="""mutation ($id: UUID!, $name: String!) {
  result: roleTypeInsert(roleType: {id: $id, name: $name}) {
    id
    roleType {
      name
      nameEn
      lastchange
      roles { id }
    }
  }
}""", variables={"id": "850b03cf-a69a-4a6c-b980-1afaf5be174b", "name": "newname"})