from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Literal
from datetime import datetime
import pytz
from pathlib import Path

app = FastAPI(title="Calculator API", version="1.0.0")

# Setup templates directory
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))


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


@app.get("/clock", response_class=HTMLResponse)
async def digital_clock(request: Request, timezone: str = "UTC"):
    """
    Display a digital clock with real-time updates.
    Supports multiple timezones via the timezone query parameter.

    Examples:
    - /clock (displays UTC time)
    - /clock?timezone=America/New_York
    - /clock?timezone=Asia/Singapore
    """
    try:
        # Validate timezone
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)

        return templates.TemplateResponse(
            "clock.html",
            {
                "request": request,
                "timezone": timezone,
                "current_time": current_time.strftime("%H:%M:%S"),
                "current_date": current_time.strftime("%A, %B %d, %Y"),
            }
        )
    except pytz.exceptions.UnknownTimeZoneError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid timezone: {timezone}. Please use a valid IANA timezone name."
        )

