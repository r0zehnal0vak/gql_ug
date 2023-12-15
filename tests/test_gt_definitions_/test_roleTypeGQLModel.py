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