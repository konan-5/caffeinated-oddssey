from typing import Optional
from pydantic import BaseModel, Field


class Order(BaseModel):
    id: Optional[int] = None
    client_id: str
    status: str
