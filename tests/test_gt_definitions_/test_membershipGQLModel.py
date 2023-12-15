from ..gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery
)

# test_membership_by_id = createByIdTest(tableName="memberships", queryEndpoint="membershipById")
# test_user_page = createPageTest(tableName="groups", queryEndpoint="groupPage")
test_membership_reference = createResolveReferenceTest(tableName="memberships", gqltype="MembershipGQLModel", attributeNames=["id"])