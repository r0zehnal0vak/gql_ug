import logging
import datetime
import pytest_asyncio
import uuid

@pytest_asyncio.fixture
async def GQLInsertQueries():
    result = {
        "forms": {
            "create": """
mutation ($id: UUID!, $name: String!, $type_id: UUID!, $name_en: String!) {
  formInsert(
    form: {id: $id, name: $name, typeId: $type_id, nameEn: $name_en}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: formById(id: $id) { id }}""",
},
        "formsections": {"create": """
mutation ($id: UUID!, $name: String!, $order: Int!, $name_en: String!, $form_id: UUID!) {
  formSectionInsert(
    section: {id: $id, name: $name, order: $order, nameEn: $name_en, formId: $form_id}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: formSectionById(id: $id) { id }}""",
},
        "formparts":{"create": """
mutation ($id: UUID!, $name: String!, $order: Int!, $name_en: String!, $section_id: UUID!) {
  formPartInsert(
    part: {id: $id, name: $name, order: $order, nameEn: $name_en, sectionId: $section_id}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: formPartById(id: $id) { id }}""",
},
        "formitems": {"create": """
mutation ($id: UUID!, $name: String!, $order: Int!, $name_en: String!, $part_id: UUID!) {
  formItemInsert(
    item: {id: $id, name: $name, order: $order, nameEn: $name_en, partId: $part_id}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: formItemById(id: $id) { id }}""",
},
        "formrequests": {"create": """
mutation ($id: UUID!, $name: String!) {
  formRequestInsert(
    request: {id: $id, name:$name }
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: requestById(id: $id) { id }}""",
},
        "formhistories": {"create": """
mutation ($id: UUID!, $name: String!, $form_id: UUID!, $request_id: UUID!) {
  formHistoryInsert(
    history: {id: $id, name:$name, requestId: $request_id, formId: $form_id}
  ) {
    id
    msg
  }
}""",
            "read": """query($id: UUID!){ result: formHistoryById(id: $id) { id }}""",
},

    }
    
    return result


@pytest_asyncio.fixture
async def FillDataViaGQL(DemoData, GQLInsertQueries, ClientExecutorAdmin):
    types = [type(""), type(datetime.datetime.now()), type(uuid.uuid1())]
    for tablename, queryset in GQLInsertQueries.items():
        table = DemoData.get(tablename, None)
        assert table is not None, f"{tablename} is missing in DemoData"

        for row in table:
            variable_values = {}
            for key, value in row.items():
                variable_values[key] = value
                if isinstance(value, datetime.datetime):
                    variable_values[key] = value.isoformat()
                elif type(value) in types:
                    variable_values[key] = f"{value}"

            readResponse = await ClientExecutorAdmin(query=queryset["read"], variable_values=variable_values)
            if readResponse["data"]["result"] is not None:
                logging.info(f"row with id `{variable_values['id']}` already exists in `{tablename}`")
                continue
            insertResponse = await ClientExecutorAdmin(query=queryset["create"], variable_values=variable_values)
            assert insertResponse.get("errors", None) is None, insertResponse
        logging.info(f"{tablename} initialized via gql query")
    logging.info(f"All WANTED tables are initialized")