from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from datetime import datetime
import pytz

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


class CurrentTimeResponse(BaseModel):
    current_time: str
    timezone: str
    timestamp: float


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


@app.get("/current-time", response_model=CurrentTimeResponse)
def get_current_time(timezone: str = "UTC"):
    """
    Get the current time in the specified timezone.
    Default timezone is UTC if not specified.
    
    Examples of valid timezones:
    - UTC
    - America/New_York
    - Europe/London
    - Asia/Tokyo
    - Asia/Singapore
    """
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        
        return CurrentTimeResponse(
            current_time=current_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
            timezone=timezone,
            timestamp=current_time.timestamp()
        )
    except pytz.exceptions.UnknownTimeZoneError:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid timezone: {timezone}. Please use a valid IANA timezone name."
        )

