from ..gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery
)

test_group_by_id = createByIdTest(tableName="groups", queryEndpoint="groupById")
test_group_page = createPageTest(tableName="groups", queryEndpoint="groupPage")
test_group_reference = createResolveReferenceTest(tableName="groups", gqltype="GroupGQLModel")