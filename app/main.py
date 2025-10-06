from fastapi import FastAPI, HTTPException

from .schemas import CalculateRequest, CalculateResponse


app = FastAPI(title="WORKATO_TEST Calculator API")


@app.post("/calculate", response_model=CalculateResponse)
def calculate(payload: CalculateRequest) -> CalculateResponse:
    a = payload.a
    b = payload.b
    op = payload.operator

    if op == '+':
        return CalculateResponse(result=a + b)
    if op == '-':
        return CalculateResponse(result=a - b)
    if op == '*':
        return CalculateResponse(result=a * b)
    if op == '/':
        if b == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed")
        return CalculateResponse(result=a / b)

    # This should be unreachable due to Pydantic validation
    raise HTTPException(status_code=400, detail="Unsupported operator")


