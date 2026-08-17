import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

from .config import REQUEST_TIMEOUT, MAX_SEARCH_RESULTS


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; "
        "AI-Product-Ops-Research-Agent/1.0)"
    )
}


def search_web(query: str, limit: int = MAX_SEARCH_RESULTS):
    """
    Uses DuckDuckGo HTML search.
    This avoids requiring another paid search API for the MVP.
    """

    url = (
        "https://html.duckduckgo.com/html/"
        f"?q={quote(query)}"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for result in soup.select(".result")[:limit]:

        title = result.select_one(".result__title")
        link = result.select_one(".result__a")
        snippet = result.select_one(".result__snippet")

        if not link:
            continue

        results.append({
            "title": title.get_text(" ", strip=True) if title else "",
            "url": link.get("href"),
            "snippet": snippet.get_text(" ", strip=True)
            if snippet else ""
        })

    return results


def fetch_page(url: str):
    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for element in soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

        text = soup.get_text(
            "\n",
            strip=True
        )

        return text[:30000]

    except Exception as exc:

        return f"PAGE_FETCH_ERROR: {exc}"


def research_queries(app: str):

    return [

        f'"{app}" API documentation authentication',

        f'"{app}" developer API OAuth API key',

        f'"{app}" REST API GraphQL webhooks',

        f'"{app}" MCP Model Context Protocol',

        f'"{app}" API pricing developer access',

    ]


def gather_web_evidence(app: str):

    evidence = []

    seen = set()

    for query in research_queries(app):

        try:
            results = search_web(query)

            for result in results:

                url = result["url"]

                if url in seen:
                    continue

                seen.add(url)

                evidence.append({
                    **result,
                    "page_text": fetch_page(url)
                })

        except Exception as exc:

            evidence.append({
                "title": "SEARCH_ERROR",
                "url": "",
                "snippet": str(exc),
                "page_text": ""
            })

    return evidence