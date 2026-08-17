import json
import random

from openai import OpenAI

from .config import OPENAI_API_KEY, MODEL
from .prompts import VERIFICATION_PROMPT
from .web_researcher import gather_web_evidence


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def verify_app(record):

    print(
        f"[VERIFY] {record['app']}"
    )

    evidence = gather_web_evidence(
        record["app"]
    )

    evidence_text = "\n\n".join(

        f"""
TITLE: {x.get('title')}
URL: {x.get('url')}
SNIPPET: {x.get('snippet')}
PAGE: {x.get('page_text', '')[:8000]}
"""
        for x in evidence
    )

    prompt = VERIFICATION_PROMPT

    prompt += f"""

ORIGINAL RECORD:

{json.dumps(record, indent=2)}

FRESH EVIDENCE:

{evidence_text}

Return JSON:

{{
  "app": "...",
  "overall": "correct|partially_correct|incorrect|unverifiable",
  "field_results": {{
      "auth_methods": {{
          "status": "...",
          "reason": "..."
      }},
      "self_serve_status": {{
          "status": "...",
          "reason": "..."
      }},
      "api_type": {{
          "status": "...",
          "reason": "..."
      }},
      "mcp_available": {{
          "status": "...",
          "reason": "..."
      }},
      "agent_ready": {{
          "status": "...",
          "reason": "..."
      }}
  }},
  "corrections": [],
  "verified_sources": []
}}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    text = response.output_text

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        return {
            "app": record["app"],
            "overall": "unverifiable",
            "raw_response": text,
            "field_results": {},
            "corrections": [],
            "verified_sources": []
        }


def calculate_accuracy(results):

    if not results:
        return 0

    correct = sum(
        1
        for x in results
        if x.get("overall") == "correct"
    )

    return round(
        correct / len(results) * 100,
        2
    )


def sample_records(records, size=15):

    if len(records) <= size:
        return records

    return random.sample(
        records,
        size
    )