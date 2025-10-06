from typing import Literal
from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")
    operator: Literal['+', '-', '*', '/'] = Field(..., description="Operation to perform")


class CalculateResponse(BaseModel):
    result: float


