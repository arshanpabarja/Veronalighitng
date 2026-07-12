from pydantic import BaseModel


class ProductTranslation(BaseModel):
    name: str
    subtitle: str
    description: str
    full_description: str
    meta_title: str
    meta_description: str
    image1_alt: str
    image2_alt: str
    image3_alt: str
    image4_alt: str


class ProductTranslationList(BaseModel):
    products: list[ProductTranslation]