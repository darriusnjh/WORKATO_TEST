# WORKATO_TEST
A test environment for workato MCP recipes

## Run the calculator API

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

3. Try it

```bash
curl -s -X POST http://localhost:8000/calculate \
  -H 'Content-Type: application/json' \
  -d '{"a": 10, "b": 5, "operator": "/"}'
```

## Tests

```bash
pytest -q
```