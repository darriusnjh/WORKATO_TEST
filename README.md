# WORKATO_TEST

A test environment for workato MCP recipes

## Calculator API

A simple REST API that performs basic calculator operations: addition (+), subtraction (-), multiplication (*), and division (/).

### Installation

```bash
pip install -r requirements.txt
```

### Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Usage Example

```bash
curl -X POST "http://localhost:8000/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "+",
    "num1": 10,
    "num2": 5
  }'
```

Response:
```json
{
  "operation": "+",
  "num1": 10,
  "num2": 5,
  "result": 15
}
```

### Supported Operations

- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division (returns error if dividing by zero)
