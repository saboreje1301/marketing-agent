from pydantic import BaseModel, Field, HttpUrl


class SeoAuditRequest(BaseModel):
    url: HttpUrl
    keyword: str | None = None


class SeoAuditResponse(BaseModel):
    url: HttpUrl
    status_code: int
    title: str | None
    title_length: int
    meta_description: str | None
    meta_description_length: int
    h1_count: int
    h2_count: int
    word_count: int
    internal_links: int
    external_links: int
    canonical: str | None
    robots: str | None
    recommendations: list[str] = Field(default_factory=list)


class SeoAiAuditResponse(BaseModel):
    audit: SeoAuditResponse
    summary: str
    recommendations: list[str]
    suggested_title: str
    suggested_meta_description: str
    suggested_keywords: list[str]