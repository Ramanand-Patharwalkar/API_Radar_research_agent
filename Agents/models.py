from typing import List, Optional
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    url: str
    title: Optional[str] = None
    claim_supported: str


class AppResearch(BaseModel):

    app: str

    category: str

    description: str = Field(
        description="One-line description of what the app does."
    )

    auth_methods: List[str] = []

    self_serve_status: str = Field(
        description=(
            "One of: self-serve, trial/self-serve, paid-required, "
            "admin-required, partnership/contact-sales, unclear"
        )
    )

    credential_notes: str = ""

    api_type: List[str] = []

    api_breadth: str = Field(
        description="One of: broad, moderate, narrow, unclear"
    )

    graphql_available: bool = False

    webhooks_available: bool = False

    mcp_available: bool = False

    mcp_notes: str = ""

    composio_available: bool = False

    composio_tool_count: Optional[int] = None

    agent_ready: str = Field(
        description="One of: easy-win, buildable, engineering-heavy, outreach-required"
    )

    agent_score: int = Field(ge=0, le=10)

    main_blocker: str = ""

    confidence: str = Field(
        description="One of: high, medium, low"
    )

    needs_human_review: bool = False

    evidence: List[Evidence] = []

    research_notes: str = ""