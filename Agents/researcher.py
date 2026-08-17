import json
from openai import OpenAI

from .config import OPENAI_API_KEY, MODEL
from .models import AppResearch
from .prompts import SYSTEM_PROMPT, RESEARCH_PROMPT
from .web_researcher import gather_web_evidence
from .composio_checker import check_composio


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def build_evidence_text(evidence):

    output = []

    for index, item in enumerate(evidence):

        output.append(
            f"""
SOURCE {index + 1}

TITLE:
{item.get("title")}

URL:
{item.get("url")}

SEARCH SNIPPET:
{item.get("snippet")}

PAGE TEXT:
{item.get("page_text", "")[:10000]}
"""
        )

    return "\n".join(output)


def research_app(app: str, website: str):

    print(f"\n[RESEARCH] {app}")

    web_evidence = gather_web_evidence(app)

    composio_data = check_composio(app)

    evidence_text = build_evidence_text(
        web_evidence
    )

    prompt = RESEARCH_PROMPT.format(
        app=app,
        website=website
    )

    prompt += f"""

COMPOSIO CHECK:

{json.dumps(composio_data, indent=2)}

WEB EVIDENCE:

{evidence_text}
"""

    response = client.responses.parse(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        text_format=AppResearch
    )

    result = response.output_parsed

    # Override/add machine evidence for transparency.
    result.composio_available = composio_data["available"]

    result.composio_tool_count = (
        composio_data["tool_count"]
    )

    if composio_data["available"]:

        result.research_notes += (
            f"\nComposio toolkit detected: "
            f"{composio_data['toolkit']}"
        )

    return result