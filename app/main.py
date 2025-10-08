from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

app = FastAPI(title="Calculator API", version="1.0.0")


class CalculatorRequest(BaseModel):
    operation: Literal["+", "-", "*", "/"]
    num1: float
    num2: float


class CalculatorResponse(BaseModel):
    operation: str
    num1: float
    num2: float
    result: float


@app.get("/")
def read_root():
    return {"message": "Calculator API is running. Use /calculate endpoint for operations."}


@app.post("/calculate", response_model=CalculatorResponse)
def calculate(request: CalculatorRequest):
    """
    Perform calculator operations: addition (+), subtraction (-), multiplication (*), division (/)
    """
    num1 = request.num1
    num2 = request.num2
    operation = request.operation
    
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = num1 / num2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")
    
    return CalculatorResponse(
        operation=operation,
        num1=num1,
        num2=num2,
        result=result
    )

