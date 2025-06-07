from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., description="Unique identifier for the user")
    busy: List[Tuple[str, str]] = Field(
        default_factory=list, description="List of busy time ranges for the user"
    )



class SlotRequest(BaseModel):
    users: List[User]

class BookRequest(BaseModel):
    participants: Optional[List[int]] = Field(..., description="List of user IDs who are booking the slot")
    interval: tuple[str, str] = Field(..., description="List of time intervals in 'HH:MM' format to book slots")
