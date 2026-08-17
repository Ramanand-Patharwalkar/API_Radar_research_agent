import csv
import json
import os

from agent.researcher import research_app
from agent.verifier import (
    verify_app,
    sample_records,
    calculate_accuracy
)
from agent.analyzer import analyze


APPS_FILE = "data/apps.csv"

RESEARCH_FILE = (
    "data/research_results.json"
)

VERIFICATION_FILE = (
    "data/verification_results.json"
)

SAMPLE_FILE = (
    "data/verification_sample.json"
)


def load_apps():

    with open(
        APPS_FILE,
        newline="",
        encoding="utf-8"
    ) as f:

        return list(
            csv.DictReader(f)
        )


def research_all(apps):

    results = []

    for item in apps:

        try:

            result = research_app(
                item["app"],
                item["website"]
            )

            record = result.model_dump()

            record["id"] = item["id"]

            record["website"] = item["website"]

            results.append(record)

            with open(
                RESEARCH_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    results,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

        except Exception as exc:

            print(
                f"[ERROR] {item['app']}: {exc}"
            )

    return results


def verify_sample(results):

    sample = sample_records(
        results,
        size=15
    )

    verification = []

    for record in sample:

        try:

            result = verify_app(
                record
            )

            verification.append(result)

        except Exception as exc:

            verification.append({
                "app": record["app"],
                "overall": "unverifiable",
                "error": str(exc)
            })

    with open(
        SAMPLE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            verification,
            f,
            indent=2,
            ensure_ascii=False
        )

    return verification


def main():

    apps = load_apps()

    print(
        f"Loaded {len(apps)} applications."
    )

    if os.path.exists(
        RESEARCH_FILE
    ):

        print(
            "Existing research file found."
        )

        with open(
            RESEARCH_FILE,
            encoding="utf-8"
        ) as f:

            results = json.load(f)

    else:

        results = research_all(apps)

    print(
        f"Research complete: "
        f"{len(results)} apps"
    )

    verification = verify_sample(
        results
    )

    accuracy = calculate_accuracy(
        verification
    )

    print(
        f"Verification accuracy: "
        f"{accuracy}%"
    )

    analysis = analyze(
        results
    )

    print("\n========== ANALYSIS ==========")

    print(
        json.dumps(
            analysis,
            indent=2
        )
    )

    with open(
        "data/analysis.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "analysis": analysis,
                "verification_accuracy": accuracy
            },
            f,
            indent=2
        )


if __name__ == "__main__":
    main()