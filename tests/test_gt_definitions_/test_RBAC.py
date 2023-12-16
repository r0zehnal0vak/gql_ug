from ..gqlshared import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery
)
test_rbac_by_id_user = createFrontendQuery(query="""
    query($id: UUID!) {
        rbacById(id: $id) {
                id
                roles { user { id } group { id }}
            }}
""", variables={"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"})

test_rbac_by_id_group = createFrontendQuery(query="""
    query($id: UUID!) {
        rbacById(id: $id) {
                id
                roles { user { id } group { id }}
            }}
""", variables={"id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003"})

test_rbac_resolve_reference = createFrontendQuery(query="""
    query($id: UUID!) {
        _entities(representations: [{__typename: "RBACObjectGQLModel", id: $id}]) {
            ...on RBACObjectGQLModel {
                id
            }}}
""", variables={"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"})
