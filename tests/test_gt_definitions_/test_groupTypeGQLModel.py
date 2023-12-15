from ..gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery
)

test_grouptype_by_id = createByIdTest(tableName="grouptypes", queryEndpoint="groupTypeById")
test_grouptype_page = createPageTest(tableName="grouptypes", queryEndpoint="groupTypePage")
test_user_reference = createResolveReferenceTest(tableName="grouptypes", gqltype="GroupTypeGQLModel")