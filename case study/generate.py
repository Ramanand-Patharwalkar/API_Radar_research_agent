import json
from pathlib import Path


BASE = Path(__file__).parent.parent

with open(
    BASE / "data" / "research_results.json",
    encoding="utf-8"
) as f:

    results = json.load(f)


with open(
    BASE / "data" / "analysis.json",
    encoding="utf-8"
) as f:

    analysis_data = json.load(f)


analysis = analysis_data["analysis"]

accuracy = analysis_data[
    "verification_accuracy"
]


def esc(value):

    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


rows = ""

for r in results:

    rows += f"""
    <tr>
        <td>{esc(r['app'])}</td>
        <td>{esc(r['category'])}</td>
        <td>{esc(', '.join(r['auth_methods']))}</td>
        <td>{esc(r['self_serve_status'])}</td>
        <td>{esc(', '.join(r['api_type']))}</td>
        <td>{esc(str(r['mcp_available']))}</td>
        <td>{esc(r['agent_ready'])}</td>
        <td>{esc(r['main_blocker'])}</td>
        <td>
            <a href="{esc(r['evidence'][0]['url'] if r['evidence'] else r.get('website', '#'))}"
               target="_blank">
               Evidence
            </a>
        </td>
    </tr>
    """


html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
AI Product Ops Research Agent
</title>

<style>

body {{
    margin: 0;
    font-family:
        Inter,
        system-ui,
        -apple-system,
        sans-serif;
    background: #f6f7f9;
    color: #15171a;
}}

.container {{
    max-width: 1400px;
    margin: auto;
    padding: 40px 24px;
}}

.hero {{
    background: #111827;
    color: white;
    padding: 60px 50px;
    border-radius: 24px;
    margin-bottom: 30px;
}}

.hero h1 {{
    font-size: 46px;
    margin-bottom: 15px;
}}

.hero p {{
    color: #d1d5db;
    font-size: 19px;
    max-width: 800px;
}}

.grid {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 30px;
}}

.card {{
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
}}

.number {{
    font-size: 35px;
    font-weight: 700;
}}

.label {{
    color: #6b7280;
}}

section {{
    background: white;
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
}}

h2 {{
    font-size: 28px;
}}

.pipeline {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}}

.step {{
    background: #eef2ff;
    padding: 15px 20px;
    border-radius: 12px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}}

th {{
    background: #111827;
    color: white;
    padding: 12px;
    text-align: left;
}}

td {{
    padding: 12px;
    border-bottom: 1px solid #e5e7eb;
}}

.table-wrap {{
    overflow-x: auto;
}}

.verdict {{
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    background: #eef2ff;
}}

footer {{
    text-align: center;
    color: #6b7280;
    padding: 40px;
}}

</style>

</head>


<body>

<div class="container">


<div class="hero">

<h1>
AI Product Ops Research Agent
</h1>

<p>
An agent-driven study of API accessibility,
authentication, MCP readiness and agent
buildability across {len(results)} applications.
</p>

</div>


<div class="grid">

<div class="card">

<div class="number">
{len(results)}
</div>

<div class="label">
Apps researched
</div>

</div>


<div class="card">

<div class="number">
{analysis['mcp_percentage']}%
</div>

<div class="label">
MCP availability
</div>

</div>


<div class="card">

<div class="number">
{analysis['self_serve_percentage']}%
</div>

<div class="label">
Self-serve
</div>

</div>


<div class="card">

<div class="number">
{accuracy}%
</div>

<div class="label">
Verification sample accuracy
</div>

</div>

</div>


<section>

<h2>
The headline
</h2>

<p>
The research agent turns unstructured developer
documentation into a structured assessment of
whether an application can become an AI agent
toolkit. The strongest candidates combine
documented APIs, self-serve credentials,
broad functionality and low integration friction.
</p>

</section>


<section>

<h2>
Research agent
</h2>

<div class="pipeline">

<div class="step">
1. App list
</div>

<div class="step">
2. Web search
</div>

<div class="step">
3. Official docs
</div>

<div class="step">
4. Composio check
</div>

<div class="step">
5. Structured extraction
</div>

<div class="step">
6. Confidence scoring
</div>

<div class="step">
7. Verification
</div>

<div class="step">
8. Human review
</div>

</div>

<p>
The agent prioritizes official documentation,
keeps evidence URLs, separates uncertainty
from confirmed findings, and performs a second
verification pass on a sample.
</p>

</section>


<section>

<h2>
Buildability distribution
</h2>

<div class="grid">

{''.join(
f'''
<div class="card">
<div class="number">
{count}
</div>
<div class="label">
{esc(label)}
</div>
</div>
'''
for label, count
in analysis["verdict"].items()
)}

</div>

</section>


<section>

<h2>
Authentication patterns
</h2>

<div class="grid">

{''.join(
f'''
<div class="card">
<div class="number">
{count}
</div>
<div class="label">
{esc(label)}
</div>
</div>
'''
for label, count
in analysis["auth"].items()
)}

</div>

</section>


<section>

<h2>
Research matrix
</h2>

<div class="table-wrap">

<table>

<thead>

<tr>

<th>App</th>
<th>Category</th>
<th>Auth</th>
<th>Access</th>
<th>API</th>
<th>MCP</th>
<th>Verdict</th>
<th>Blocker</th>
<th>Evidence</th>

</tr>

</thead>

<tbody>

{rows}

</tbody>

</table>

</div>

</section>


<section>

<h2>
Verification
</h2>

<p>
A separate verification agent re-researched a
sample of applications using fresh evidence.
The verification result was {accuracy}% on the
sample.
</p>

<p>
Human review should focus on low-confidence
records, conflicting documentation, gated
credential flows, and ambiguous MCP claims.
</p>

</section>


<section>

<h2>
Limitations & honesty
</h2>

<p>
API availability does not automatically mean
easy agent integration. Enterprise approval,
rate limits, restricted scopes, poor documentation,
complex OAuth flows and partnership requirements
can still create significant implementation work.
</p>

<p>
Composio availability is treated as an additional
integration signal, not proof of an application's
underlying API accessibility.
</p>

</section>


<footer>

AI Product Ops Research Agent · Built as an
agent-driven research and verification workflow

</footer>


</div>

</body>

</html>
"""


with open(
    BASE / "case-study" / "index.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(html)


print(
    "Case study generated successfully."
)