## Execution

```bash
pytest --cov-report term-missing --cov=gql_ug tests -x
```

```bash
uvicorn main:app --env-file environment.txt --port 8000 --reload
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

## Environment variables

### DB related variables
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=example
- POSTGRES_HOST=postgres:5432
- POSTGRES_DB=data

### Authorization related variables
- JWTPUBLICKEYURL=http://localhost:8000/oauth/publickey
- JWTRESOLVEUSERPATHURL=http://localhost:8000/oauth/userinfo
- ROLELISTURL=http://localhost:8088/gql/
- RBACURL=http://localhost:8088/gql

### 
- DEMO=true
