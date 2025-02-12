from typing import Any, Dict, List
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")
    recommendations: List[str] = Field(description="recommendations about them")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "facts": self.facts,
            "recommendations": self.recommendations,
        }


summary_parser = PydanticOutputParser(pydantic_object=Summary)
