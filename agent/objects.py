from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer: str = Field(
        description="The answer that should be shown to the user."
    )

    conversation: bool = Field(
        default=True,
        description=(
            "True if the conversation needs to continue. "
            "False when the refund decision is final."
        ),
    )


class PurchaseItem(BaseModel):
    name: str = Field(
        description="Name of the item purchased."
    )