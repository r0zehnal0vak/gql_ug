from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

from gql_ug.DBDefinitions import (
    UserModel,
    MembershipModel,
    GroupModel,
    GroupTypeModel,
    RoleModel,
    RoleTypeModel,
    RoleCategoryModel
)

def createIdLoader(asyncSessionMaker, dbModel) :

    mainstmt = select(dbModel)
    filtermethod = dbModel.id.in_
    class Loader(DataLoader):
        async def batch_load_fn(self, keys):
            #print('batch_load_fn', keys, flush=True)
            async with asyncSessionMaker() as session:
                statement = mainstmt.filter(filtermethod(keys))
                rows = await session.execute(statement)
                rows = rows.scalars()
                #return rows
                datamap = {}
                for row in rows:
                    datamap[row.id] = row
                result = [datamap.get(id, None) for id in keys]
                return result

        async def insert(self, entity, extraAttributes={}):
            newdbrow = dbModel()
            newdbrow = update(newdbrow, entity, extraAttributes)
            async with asyncSessionMaker() as session:
                session.add(newdbrow)
                await session.commit()
            return newdbrow

        async def update(self, entity, extraValues={}):
            async with asyncSessionMaker() as session:
                statement = mainstmt.filter_by(id=entity.id)
                rows = await session.execute(statement)
                rows = rows.scalars()
                rowToUpdate = next(rows, None)

                if rowToUpdate is None:
                    return None

                dochecks = hasattr(rowToUpdate, 'lastchange')             
                checkpassed = True  
                if (dochecks):
                    if (entity.lastchange != rowToUpdate.lastchange):
                        result = None
                        checkpassed = False                        
                    else:
                        entity.lastchange = datetime.datetime.now()
                if checkpassed:
                    rowToUpdate = update(rowToUpdate, entity, extraValues=extraValues)
                    await session.commit()
                    result = rowToUpdate
                    self.registerResult(result)               
            return result

        async def delete(self, id):
            statement = delete(dbModel).where(dbModel.id==id)
            async with asyncSessionMaker() as session:
                result = await session.execute(statement)
                await session.commit()
                self.clear(id)
                return result

        def registerResult(self, result):
            self.clear(result.id)
            self.prime(result.id, result)
            return result

        def getSelectStatement(self):
            return select(dbModel)
        
        def getModel(self):
            return dbModel
        
        def getAsyncSessionMaker(self):
            return asyncSessionMaker
        
        async def execute_select(self, statement):
            async with asyncSessionMaker() as session:
                rows = await session.execute(statement)
                return (
                    self.registerResult(row)
                    for row in rows.scalars()
                )
            
        async def filter_by(self, **filters):
            statement = mainstmt.filter_by(**filters)
            return await self.execute_select(statement)

        async def page(self, skip=0, limit=10, where=None, extendedfilter=None):
            statement = mainstmt
            if where is not None:
                statement = prepareSelect(dbModel, where)
            statement = statement.offset(skip).limit(limit)
            if extendedfilter is not None:
                statement = statement.filter_by(**extendedfilter)
            logging.info(f"loader.page statement {statement}")
            return await self.execute_select(statement)
            
        def set_cache(self, cache_object):
            self.cache = True
            self._cache = cache_object

    return Loader(cache=True)

class Loaders:
    users = None
    groups = None
    memberships = None
    grouptypes = None
    roles = None
    roletypes = None
    rolecategories = None
    pass

async def _createLoaders(
    asyncSessionMaker,
    DBModels=[
        UserModel,
        MembershipModel,
        GroupModel,
        GroupTypeModel,
        RoleModel,
        RoleTypeModel,
        RoleCategoryModel,
    ],
):

    modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in DBModels)

    result = {}
    for tableName, DBModel in modelIndex.items():  # iterate over all models
        result[tableName] = createIdLoader(asyncSessionMaker, DBModel)
    # result['memberships'].max_batch_size = 20
    return result

dbmodels = {
    "users": UserModel,
    "memberships": MembershipModel,
    "groups": GroupModel,
    "grouptypes": GroupTypeModel,
    "roles": RoleModel,
    "roletypes": RoleTypeModel,
    "rolecategories": RoleCategoryModel,
}

async def createLoaders(asyncSessionMaker, models=dbmodels) -> Loaders:
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

from functools import cache

# async def createLoaders_2(
#     asyncSessionMaker,
#     DBModels = [UserModel, MembershipModel, GroupModel, GroupTypeModel, RoleModel, RoleTypeModel],
#     FKeyedDBModels = {}
#     ):

#     def IdLoader(DBModel):
#         @property
#         @cache
#         def getIt(self):
#             return createIdLoader(asyncSessionMaker, DBModel)

#     def keyedLoader(DBModel, foreignKeyName):
#         @property
#         @cache
#         def getIt(self):
#             return createFkeyLoader(asyncSessionMaker, DBModel, foreignKeyName=foreignKeyName)


#     modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in DBModels)
#     revIndex = dict((DBModel, DBModel.__tablename__) for DBModel in DBModels)

#     attrs = {}
#     for tableName, DBModel in modelIndex.items():  # iterate over all models
#         attrs[tableName] = IdLoader(DBModel)

#     for DBModel, fkeyNames in FKeyedDBModels.items():
#         tableName = revIndex[DBModel]
#         for fkeyName in fkeyNames:
#             name = tableName + '_' + fkeyName
#             attrs[name] = keyedLoader(DBModel, fkeyName)

#     result = type("loaders", (object, ), attrs)
#     #result = type("resolvers", (object, ), {'experiment': experiment, 'loader_a': experiment})
#     return result()


async def createLoaders_3(asyncSessionMaker):
    class Loaders:
        @property
        @cache
        def users(self):
            return createIdLoader(asyncSessionMaker, UserModel)

        @property
        @cache
        def groups(self):
            return createIdLoader(asyncSessionMaker, GroupModel)

        @property
        @cache
        def roles(self):
            return createIdLoader(asyncSessionMaker, RoleModel)

        @property
        @cache
        def roles_for_user_id(self):
            return createFkeyLoader(asyncSessionMaker, RoleModel, foreignKeyName="user_id")

        @property
        @cache
        def roletypes(self):
            return createIdLoader(asyncSessionMaker, RoleTypeModel)

        @property
        @cache
        def grouptypes(self):
            return createIdLoader(asyncSessionMaker, GroupTypeModel)

        @property
        @cache
        def memberships(self):
            return createIdLoader(asyncSessionMaker, MembershipModel)

        @property
        @cache
        def memberships_user_id(self):
            return createFkeyLoader(
                asyncSessionMaker, MembershipModel, foreignKeyName="user_id"
            )

        @property
        @cache
        def memberships_group_id(self):
            return createFkeyLoader(
                asyncSessionMaker, MembershipModel, foreignKeyName="group_id"
            )

        @property
        @cache
        def groups_mastergroup_id(self):
            return createFkeyLoader(
                asyncSessionMaker, GroupModel, foreignKeyName="mastergroup_id"
            )

    return Loaders()
