from ..gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery
)

test_role_category_by_id = createByIdTest(tableName="rolecategories", queryEndpoint="roleCategoryById")
test_role_category_page = createPageTest(tableName="rolecategories", queryEndpoint="roleCategoryPage")
test_role_category_reference = createResolveReferenceTest(tableName="rolecategories", gqltype="RoleCategoryGQLModel")