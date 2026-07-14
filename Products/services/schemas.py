from typing import List

from pydantic import BaseModel, Field


class FamilyTranslation(BaseModel):

    name: str = Field(
        description="Persian family or series name"
    )

    subtitle: str = Field(
        description="Short Persian family subtitle"
    )

    meta_title: str = Field(
        description="SEO title in Persian"
    )

    meta_description: str = Field(
        description="SEO meta description in Persian"
    )