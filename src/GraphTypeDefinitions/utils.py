import typing
import sys
import strawberry
from dataclasses import dataclass
import datetime
import logging
from uoishelpers.resolvers import createInputs


from .BaseGQLModel import IDType


inputTypeGQLMapper = {}


@strawberry.input(description="Str filter methods, only one constrain allowed")
class StrFilter:
    _eq: typing.Optional[str] = strawberry.field(name="_eq", description="operation for select.filter() method", default=None)
    _le: typing.Optional[str] = strawberry.field(name="_le", description="operation for select.filter() method", default=None)
    _lt: typing.Optional[str] = strawberry.field(name="_lt", description="operation for select.filter() method", default=None)
    _ge: typing.Optional[str] = strawberry.field(name="_ge", description="operation for select.filter() method", default=None)
    _gt: typing.Optional[str] = strawberry.field(name="_gt", description="operation for select.filter() method", default=None)
    _like: typing.Optional[str] = strawberry.field(name="_like", description="operation for select.filter() method", default=None)
    _ilike: typing.Optional[str] = strawberry.field(name="_ilike", description="operation for select.filter() method", default=None)
    _startswith: typing.Optional[str] = strawberry.field(name="_startswith", description="operation for select.filter() method", default=None)
    _endswith: typing.Optional[str] = strawberry.field(name="_endswith", description="operation for select.filter() method", default=None)

@strawberry.input(description="Datetime filter methods, only one constrain allowed")
class DatetimeFilter:
    _eq: typing.Optional[datetime.datetime] = strawberry.field(name="_eq", description="operation for select.filter() method", default=None)
    _le: typing.Optional[datetime.datetime] = strawberry.field(name="_le", description="operation for select.filter() method", default=None)
    _lt: typing.Optional[datetime.datetime] = strawberry.field(name="_lt", description="operation for select.filter() method", default=None)
    _ge: typing.Optional[datetime.datetime] = strawberry.field(name="_ge", description="operation for select.filter() method", default=None)
    _gt: typing.Optional[datetime.datetime] = strawberry.field(name="_gt", description="operation for select.filter() method", default=None)

@strawberry.input(description="Integer filter methods, only one constrain allowed")
class IntFilter:
    _eq: typing.Optional[int] = strawberry.field(name="_eq", description="operation for select.filter() method", default=None)
    _le: typing.Optional[int] = strawberry.field(name="_le", description="operation for select.filter() method", default=None)
    _lt: typing.Optional[int] = strawberry.field(name="_lt", description="operation for select.filter() method", default=None)
    _ge: typing.Optional[int] = strawberry.field(name="_ge", description="operation for select.filter() method", default=None)
    _gt: typing.Optional[int] = strawberry.field(name="_gt", description="operation for select.filter() method", default=None)
    _in: typing.Optional[typing.List[int]] = strawberry.field(name="_in", description="operation for select.filter() method", default=None)

@strawberry.input(description="Integer filter methods, only one constrain allowed")
class BoolFilter:
    _eq: typing.Optional[bool] = strawberry.field(name="_eq", description="operation for select.filter() method", default=None)

import uuid

@strawberry.input(description="Integer filter methods, only one constrain allowed")
class UuidFilter:
    _eq: typing.Optional[IDType] = strawberry.field(name="_eq", description="operation for select.filter() method", default=None)
    _in: typing.Optional[typing.List[IDType]] = strawberry.field(name="_in", description="operation for select.filter() method", default=None)

inputTypeGQLMapper[IDType] = UuidFilter
inputTypeGQLMapper[int] = IntFilter
inputTypeGQLMapper[str] = StrFilter
inputTypeGQLMapper[datetime.datetime] = DatetimeFilter
inputTypeGQLMapper[bool] = BoolFilter


# from graphql.language import DirectiveLocation
# @strawberry.input
# class ReduceInput:
#     id: IDType

# @strawberry.directive(
#     locations=[DirectiveLocation.FIELD], description="returns just first"
# )
# def reduce(value, param: ReduceInput) -> IDType :
#     # values = [v for v in value]
#     first = next(value, None)
#     return [] if first is None else [first]
# schema = strawberryA.federation.Schema(query=Query, types=(RBACObjectGQLModel, IDType), mutation=Mutation, directives=[reduce])