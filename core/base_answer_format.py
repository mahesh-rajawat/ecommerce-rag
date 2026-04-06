from pydantic import BaseModel, Field

class BaseAnswerFormat(BaseModel):
    reasoning: str = Field(description="Internal logic and comparison of numbers.")
    final_answer: str = Field(description="The clean, polite response to show the customer.")
    sources_used: list = Field(description="The IDs of the context chunks used to answer.")