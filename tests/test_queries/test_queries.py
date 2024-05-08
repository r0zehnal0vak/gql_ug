from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery,
    createInsertQuery,
    createQueryTest
)

test_user_by_id = createByIdTest(tableName="users")
test_user_page = createPageTest(tableName="users")
test_user_insert = createInsertQuery(tableName="users", variables={"id": "4f7bfda9-c817-466f-8a0d-e51c2a4fa889", "name": "Peter"})
test_user_coverage = createQueryTest(tableName="users", queryName="coverage")
test_user_update = createUpdateQuery(tableName="users", variables={"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "name": "Peter"})

test_group_by_id = createByIdTest(tableName="groups")
test_group_page = createPageTest(tableName="groups")
test_group_insert = createInsertQuery(tableName="groups", variables={"id": "d9269e36-c2c8-4b01-aee9-a606c6e72db2", "name": "New Group", "grouptype_id": "cd49e152-610c-11ed-9f29-001a7dda7110"})
test_group_update = createUpdateQuery(tableName="groups")

test_membership_by_id = createByIdTest(tableName="memberships")
test_membership_page = createPageTest(tableName="memberships")
test_membership_update = createUpdateQuery(tableName="memberships")
test_membership_insert = createInsertQuery(tableName="memberships")

test_role_by_id = createByIdTest(tableName="roles")
test_role_page = createPageTest(tableName="roles")
test_role_coverage = createQueryTest(tableName="roles", queryName="coverage")
test_role_insert = createInsertQuery(tableName="roles")
test_role_update = createUpdateQuery(tableName="roles")

test_grouptype_by_id = createByIdTest(tableName="grouptypes")
test_grouptype_page = createPageTest(tableName="grouptypes")
test_grouptype_insert = createInsertQuery(tableName="grouptypes")
test_grouptype_coverage = createQueryTest(tableName="grouptypes", queryName="coverage")
test_grouptype_update = createUpdateQuery(tableName="grouptypes")

test_roletype_by_id = createByIdTest(tableName="roletypes")
test_roletype_page = createPageTest(tableName="roletypes")
test_roletype_insert = createInsertQuery(tableName="roletypes")
test_roletype_coverage = createQueryTest(tableName="roletypes", queryName="coverage")
test_roletype_update = createUpdateQuery(tableName="roletypes")

test_rolecategory_by_id = createByIdTest(tableName="rolecategories")
test_rolecategory_page = createPageTest(tableName="rolecategories")
test_rolecategory_insert = createInsertQuery(tableName="rolecategories")

