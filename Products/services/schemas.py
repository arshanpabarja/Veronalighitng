from pydantic import BaseModel, Field

class FamilySEO(BaseModel):
    meta_title_en: str
    meta_description_en: str

    meta_title_fa: str
    meta_description_fa: str

    icon_alt_en: str
    icon_alt_fa: str