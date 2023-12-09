

```
pytest --cov-report term-missing --cov=gql_ug tests -x
```

```
uvicorn main:app --env-file environment.txt --port 8001 --reload
```

```gql
query {
	userPage(where: {fullname: {_ilike: "%newbie%"}}, orderBy: "email", desc: true) {
    id
    name
    email
    surname
  }
}
```