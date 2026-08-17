from collections import Counter


def percentage(counter, total):

    if total == 0:
        return 0

    return round(
        counter / total * 100,
        1
    )


def analyze(records):

    total = len(records)

    auth = Counter()
    self_serve = Counter()
    api = Counter()
    mcp = Counter()
    verdict = Counter()
    categories = Counter()

    for r in records:

        categories[
            r.get("category", "Unknown")
        ] += 1

        for method in r.get(
            "auth_methods", []
        ):
            auth[method] += 1

        self_serve[
            r.get(
                "self_serve_status",
                "unclear"
            )
        ] += 1

        for api_type in r.get(
            "api_type", []
        ):
            api[api_type] += 1

        mcp[
            str(
                r.get(
                    "mcp_available",
                    False
                )
            )
        ] += 1

        verdict[
            r.get(
                "agent_ready",
                "unknown"
            )
        ] += 1

    return {

        "total_apps": total,

        "auth": dict(auth),

        "self_serve": dict(self_serve),

        "api": dict(api),

        "mcp": dict(mcp),

        "verdict": dict(verdict),

        "categories": dict(categories),

        "mcp_percentage": percentage(
            mcp.get("True", 0),
            total
        ),

        "self_serve_percentage": percentage(
            self_serve.get("self-serve", 0),
            total
        )
    }