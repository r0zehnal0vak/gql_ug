from ..gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery
)

# test_role_by_id = createByIdTest(tableName="roles", queryEndpoint="roleById")
# test_role_category_page = createPageTest(tableName="rolecategories", queryEndpoint="roleCategoryPage")
test_role_reference = createResolveReferenceTest(tableName="roles", gqltype="RoleGQLModel", attributeNames=["id"])