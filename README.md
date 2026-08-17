# API_Radar_research_agent


An AI-powered research agent that evaluates software applications for **API accessibility, authentication, developer access, MCP availability, and AI-agent buildability**.

The project was created as part of an AI Product Ops research assignment.

---

## Overview

The goal of this project is to research a large set of SaaS and developer applications without manually researching every application one by one.

The agent automatically:

1. Loads the application list.
2. Searches for relevant developer/API documentation.
3. Retrieves and analyzes documentation.
4. Identifies authentication methods.
5. Determines whether developer credentials are self-serve or gated.
6. Identifies REST, GraphQL, webhook and other API capabilities.
7. Checks for MCP availability.
8. Checks Composio toolkit availability.
9. Produces an AI-agent buildability verdict.
10. Stores evidence URLs for important findings.
11. Runs an independent verification pass on a sample.
12. Generates aggregate Product Ops insights.
13. Produces a self-contained HTML case study.

The emphasis is on **evidence and verification rather than simply generating descriptions with an LLM.**

---

## Research Questions

For each application, the agent attempts to determine:

* What category does the application belong to?
* What does it do?
* What authentication methods are supported?
* Can developers obtain credentials themselves?
* Is a paid plan required?
* Is admin approval required?
* Is partnership/contact-sales access required?
* Does it provide a public REST API?
* Does it provide GraphQL?
* Are webhooks available?
* How broad is the API surface?
* Is MCP available?
* Is a Composio toolkit available?
* Could the application be exposed as an AI-agent toolkit today?
* What is the main integration blocker?
* How confident is the finding?
* What documentation supports the finding?

---

## Architecture

```text
                    Application List
                           |
                           v
                 +-------------------+
                 | Research Planner  |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Web Research      |
                 | & Documentation   |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | LLM Extraction    |
                 | Structured Schema |
                 +---------+---------+
                           |
                           +---------> Composio Check
                           |
                           v
                    Research JSON
                           |
                           v
                 +-------------------+
                 | Verification      |
                 | Agent             |
                 +---------+---------+
                           |
                           v
                    Human Review
                           |
                           v
                  Final Dataset
                           |
                           v
                 +-------------------+
                 | Product Ops       |
                 | Analysis          |
                 +---------+---------+
                           |
                           v
                   HTML Case Study
```

---

## Repository Structure

```text
API_Radar_research_agent/
│
├── agent/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── prompts.py
│   ├── web_researcher.py
│   ├── researcher.py
│   ├── verifier.py
│   └── analyzer.py
│
├── data/
│   ├── apps.csv
│   
│
├── case-study/
│   ├── generate.py
│   
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Tech Stack

* **Python** — research pipeline
* **OpenAI API** — structured research and verification
* **Composio** — agent/toolkit integration research
* **BeautifulSoup** — documentation extraction
* **Requests** — web retrieval
* **Pydantic** — structured output validation
* **Pandas** — optional data analysis
* **Jinja2 / HTML** — case study generation

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ramanand-Patharwalkar/API_Radar_research_agent.git

cd ai_Radar_research_agen
```

---

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv

.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key
COMPOSIO_API_KEY=your_composio_api_key

MODEL=gpt-5.6
MAX_SEARCH_RESULTS=5
REQUEST_TIMEOUT=20
```

Never commit your real API keys to GitHub.

The repository includes `.env.example` as a template.

---

## Running the Research Agent

Run:

```bash
python main.py
```

The agent will:

```text
Load applications
      ↓
Research applications
      ↓
Collect documentation
      ↓
Extract structured information
      ↓
Check Composio
      ↓
Save research results
      ↓
Select verification sample
      ↓
Run independent verification
      ↓
Calculate verification accuracy
      ↓
Generate Product Ops analysis
```

---

## Output

The research pipeline produces:

### `data/research_results.json`

Contains the structured research results for each application.

Example:

```json
{
  "app": "Example App",
  "category": "CRM",
  "description": "Customer relationship management platform.",
  "auth_methods": [
    "OAuth2"
  ],
  "self_serve_status": "self-serve",
  "api_type": [
    "REST"
  ],
  "api_breadth": "broad",
  "graphql_available": false,
  "webhooks_available": true,
  "mcp_available": false,
  "composio_available": true,
  "agent_ready": "easy-win",
  "agent_score": 8,
  "main_blocker": "",
  "confidence": "high"
}
```

---

### `data/verification_sample.json`

Contains the independent verification results.

The verification process checks important fields such as:

* Authentication
* Credential access
* API type
* MCP availability
* Agent-readiness verdict

Each field is classified as:

```text
correct
partially_correct
incorrect
unverifiable
```

---

### `data/analysis.json`

Contains aggregate findings such as:

* Authentication distribution
* Self-serve vs gated access
* API types
* MCP availability
* Agent-readiness distribution
* Category distribution
* Verification accuracy

---

## Agent Buildability Model

The research uses an agent-readiness classification rather than treating every API as equally easy to integrate.

### Easy Win

Typically includes:

* Public documented API
* Self-serve credentials
* Standard authentication
* Broad API surface
* Good documentation
* Low integration friction

### Buildable

The application has a usable API but has some limitations such as:

* Restricted functionality
* Complex permissions
* Rate limits
* Limited documentation

### Engineering Heavy

The integration is technically possible but requires significant engineering effort.

Potential reasons include:

* Complex authentication
* Enterprise permissions
* Multiple API systems
* Poor documentation
* Significant setup requirements

### Outreach Required

The integration is blocked or heavily restricted by:

* Contact-sales requirements
* Enterprise-only access
* Partnership requirements
* No self-serve credentials

---

## Agent Scoring

The project uses a simple readiness score to make comparisons easier.

Example factors include:

| Capability              | Score |
| ----------------------- | ----: |
| Public documented API   |    +2 |
| Self-serve credentials  |    +2 |
| Standard authentication |    +1 |
| Broad API surface       |    +2 |
| Webhooks                |    +1 |
| MCP availability        |    +1 |
| Composio toolkit        |    +1 |

The score is used as a supporting signal, not as the sole decision criterion.

Commercial gating and other hard blockers can override a high technical score.

---

## Evidence & Accuracy

The agent is instructed to prefer **official developer documentation**.

Evidence is retained for important findings so that the reviewer can inspect the source behind an answer.

The verification workflow deliberately performs an independent second research pass rather than trusting the first AI-generated answer.

The project reports:

```text
Initial research
      ↓
Independent verification
      ↓
Field-level comparison
      ↓
Corrections
      ↓
Final accuracy
```

The verification results are stored in the repository so that the accuracy claim can be inspected.

**Accuracy numbers shown in the case study are generated from the actual verification run and are not hard-coded.**

---

## Human Verification

AI research can misinterpret:

* Enterprise vs self-serve access
* OAuth requirements
* API availability
* Third-party MCP servers
* Deprecated APIs
* Pricing restrictions
* Documentation that describes a product feature rather than an API capability

Therefore, uncertain or conflicting findings are flagged for human review.

Human review focuses particularly on:

* Low-confidence records
* Conflicting documentation
* Gated APIs
* MCP claims
* Unusual authentication flows
* Ambiguous agent-readiness decisions

---

## Important Research Principle

A Composio integration is **not automatically treated as proof that an application has a publicly accessible API**.

The project treats Composio availability as an additional signal.

The underlying application's own developer documentation remains the primary evidence for:

* API availability
* Authentication
* Credential access
* API capabilities
* Commercial restrictions

---

## Generating the Case Study

After completing the research:

```bash
python case-study/generate.py
```

This generates:

```text
case-study/index.html
```

The HTML page contains:

* Research headline
* Key metrics
* Agent workflow
* Buildability distribution
* Authentication patterns
* Application matrix
* Evidence links
* Verification results
* Limitations
* Research methodology

The page is designed to be understandable without additional narration.

---

## Deploying the Case Study

The `case-study/index.html` file is a static HTML page and can be deployed using GitHub Pages or another static hosting provider.

For GitHub Pages:

1. Push the repository to GitHub.
2. Open repository **Settings**.
3. Select **Pages**.
4. Select the branch containing the case study.
5. Configure the publishing directory.
6. Save the configuration.
7. GitHub will provide the public deployment URL.

---

## Example Final Submission

**Live Case Study**

```text
https://Ramanand-Patharwalkar.github.io/API_Radar_research_agent/
```

**Source Repository**

```text
https://github.com/Ramanand-Patharwalkar/API_Radar_research_agent
```

Replace these placeholders with the actual deployed links after publishing.

---

## Limitations

This project is an automated research system and is not intended to guarantee perfect factual accuracy.

Documentation changes over time, APIs are deprecated, pricing and developer access can change, and some capabilities may require account-specific permissions.

For this reason, the system uses:

* Evidence URLs
* Structured outputs
* Confidence levels
* Independent verification
* Human review of ambiguous findings

The goal is not to claim that an LLM is always correct.

The goal is to build a **repeatable research process that makes errors visible, measurable, and correctable.**

---

## Current Dataset

The initial dataset contains the applications provided for the assignment.

The assignment description refers to 100 applications. If additional applications are provided, they can be added to:

```text
data/apps.csv
```

The pipeline is designed to process the expanded dataset without changing the research logic.

---

## Future Improvements

Potential improvements include:

* Browser automation for JavaScript-heavy documentation
* Better official-domain detection
* API documentation classification
* Automatic detection of deprecated APIs
* More detailed MCP verification
* Field-level accuracy metrics
* Human review dashboard
* Parallel research workers
* Retry and rate-limit handling
* Search-source ranking
* Automatic change detection when API documentation changes

---

## Author

**Ramanand Patharwalkar**

AI Product Ops Research Agent
2026
