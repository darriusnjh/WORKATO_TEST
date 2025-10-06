# WORKATO_TEST

A test environment for workato MCP recipes

## Calculator API

A simple REST API that performs basic calculator operations: addition (+), subtraction (-), multiplication (*), and division (/), and provides current time information.

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

### Endpoints

#### 1. Calculator Operations

**POST /calculate**

Perform basic calculator operations.

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

Supported Operations:
- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division (returns error if dividing by zero)

#### 2. Current Time

**GET /current-time**

Get the current time in a specified timezone (defaults to UTC).

```bash
# Get current time in UTC (default)
curl "http://localhost:8000/current-time"

# Get current time in a specific timezone
curl "http://localhost:8000/current-time?timezone=Asia/Singapore"
```

Response:
```json
{
  "current_time": "2024-10-07 00:52:30 SGT",
  "timezone": "Asia/Singapore",
  "timestamp": 1728241950.123456
}
```

Supported timezones include:
- `UTC`
- `America/New_York`
- `Europe/London`
- `Asia/Tokyo`
- `Asia/Singapore`
- Any valid IANA timezone name

### Running Tests

```bash
pytest tests/
```
