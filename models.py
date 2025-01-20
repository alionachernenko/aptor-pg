from pydantic import BaseModel, Field

class Interaction(BaseModel):
    user_id: str | int = Field(alias="userId")
    item_id: str | int = Field(alias="itemId")
    interaction_type: str = Field(alias="interactionType")
