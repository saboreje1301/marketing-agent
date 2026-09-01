from datetime import date, timedelta
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import httpx

from app.ai.search_console_agent import analyze_search_console
from app.schemas.search_console import SearchConsoleRequest
from app.schemas.seo import SeoAuditRequest, SeoAuditResponse


class _PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.meta_description: str | None = None
        self.canonical: str | None = None
        self.robots: str | None = None
        self.headings: dict[str, int] = {"h1": 0, "h2": 0}
        self.words: list[str] = []
        self.links: list[str] = []
        self._capture_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "title":
            self._capture_title = True
        if tag in self.headings:
            self.headings[tag] += 1
        if tag == "meta" and attributes.get("name", "").lower() == "description":
            self.meta_description = attributes.get("content")
        if tag == "meta" and attributes.get("name", "").lower() == "robots":
            self.robots = attributes.get("content")
        if tag == "link" and attributes.get("rel", "").lower() == "canonical":
            self.canonical = attributes.get("href")
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._capture_title = False

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self.title += data.strip()
        self.words.extend(data.split())


async def audit_url(request: SeoAuditRequest) -> SeoAuditResponse:
    url = str(request.url)
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=15,
        headers={"User-Agent": "MarketingAI SEO Agent/1.0"},
    ) as client:
        response = await client.get(url)

    parser = _PageParser()
    parser.feed(response.text)
    page_host = urlparse(str(response.url)).netloc
    internal_links = sum(urlparse(urljoin(url, link)).netloc == page_host for link in parser.links)
    external_links = len(parser.links) - internal_links
    recommendations: list[str] = []

    if not parser.title:
        recommendations.append("Añade un título SEO.")
    elif not 30 <= len(parser.title) <= 60:
        recommendations.append("Ajusta el título SEO a entre 30 y 60 caracteres.")
    if not parser.meta_description:
        recommendations.append("Añade una meta descripción.")
    elif not 120 <= len(parser.meta_description) <= 160:
        recommendations.append("Ajusta la meta descripción a entre 120 y 160 caracteres.")
    if parser.headings["h1"] != 1:
        recommendations.append("Usa exactamente un encabezado H1.")
    if request.keyword and request.keyword.lower() not in response.text.lower():
        recommendations.append("Incluye la keyword objetivo en el contenido.")

    return SeoAuditResponse(
        url=request.url,
        status_code=response.status_code,
        title=parser.title or None,
        title_length=len(parser.title),
        meta_description=parser.meta_description,
        meta_description_length=len(parser.meta_description or ""),
        h1_count=parser.headings["h1"],
        h2_count=parser.headings["h2"],
        word_count=len(parser.words),
        internal_links=internal_links,
        external_links=external_links,
        canonical=parser.canonical,
        robots=parser.robots,
        recommendations=recommendations,
    )


async def audit_url_with_ai(request: SeoAuditRequest):
    from app.infrastructure.ai.gemini_client import generate_seo_strategy
    from app.schemas.seo import SeoAiAuditResponse

    audit = await audit_url(request)
    context = audit.model_dump(mode="json")

    try:
        search_console = await analyze_search_console(
            SearchConsoleRequest(
                site_url=None,
                start_date=date.today() - timedelta(days=30),
                end_date=date.today(),
                row_limit=10,
            )
        )
        context["search_console_data"] = search_console.model_dump(mode="json")
    except (ValueError, OSError, httpx.HTTPError, KeyError):
        context["search_console_data"] = {
            "site_url": None,
            "start_date": (date.today() - timedelta(days=30)).isoformat(),
            "end_date": date.today().isoformat(),
            "rows": [],
        }

    strategy = await generate_seo_strategy(context)
    return SeoAiAuditResponse(audit=audit, **strategy)