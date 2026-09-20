# SPDX-License-Identifier: MPL-2.0
"""An offline, synthetic SKILLING / BALANCING demonstration. Python 3.10+."""
import argparse
from collections import Counter
import json
from pathlib import Path

SIGNALS = ("Camera height", "Lens choice", "Subject separation", "Lighting")

def discover(events):
    """Group explicitly tagged judgments; no automatic skill inference is claimed."""
    eligible = []
    seen = set()
    for event in events:
        if event["id"] in seen:
            raise ValueError("Duplicate evidence id")
        seen.add(event["id"])
        if event["action"] not in {"Accept", "Reject", "Edit"}:
            raise ValueError("Unknown action")
        if event["outcome"] not in {"improved", "not_improved", "unknown"}:
            raise ValueError("Unknown outcome")
        if event["kind"] == "judgment" and event["skill"] == "Visual Composition":
            eligible.append(event)
    successful = sum(e["outcome"] == "improved" for e in eligible)
    counts = Counter(s for e in eligible for s in e["signals"])
    return {"skill": "Visual Composition", "evidence": len(eligible),
            "successful": successful,
            "confidence": round(100 * successful / len(eligible)) if eligible else None,
            "frequent_signals": dict(counts.most_common()), "status": "candidate"}

def decide(candidate, action):
    statuses = {"register": "registered", "observe": "observing", "reject": "rejected"}
    return {**candidate, "status": statuses[action]}

def balance(candidate, friction):
    """Illustrative rules, not ELFCORE's optimizer or a capability assessment."""
    if candidate["status"] != "registered":
        return {"human": "Confirm or continue observing the candidate", "ai": [],
                "behavior": "Do not assign roles from an unconfirmed candidate"}
    support = []
    if friction["task_frequency"] == "high" or friction["user_stress"] == "high":
        support.append("Batch repetitive layout variants")
    if friction["capability_gap"] == "verification":
        support.append("Run repeatable checks and collect comparison evidence")
    return {"human": "Visual direction and final composition judgment",
            "ai": support,
            "behavior": "Prepare reversible previews; ask before costly changes"
            if friction["failure_cost"] == "high" else "Offer small reversible iterations",
            "preference": friction["preference"],
            "team_coverage": "Conceptual objective only; not measured in this demo"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data/visual_composition.json")
    parser.add_argument("--decision", choices=["register", "observe", "reject"], default="observe")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.data.read_text())
        candidate = decide(discover(data["events"]), args.decision)
        roles = balance(candidate, data["friction"])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps({"candidate": candidate, "balancing": roles}, indent=2))
        return
    print("SKILLING | SYNTHETIC DEMO\n")
    print("SKILL CANDIDATE: " + candidate["skill"])
    for key in ("evidence", "successful", "confidence"):
        value = candidate[key]
        print(f"{key.title():<12} {value if value is not None else 'N/A'}" + ("%" if key == "confidence" and value is not None else ""))
    print("Confidence = observed success ratio, not calibrated skill certainty.")
    print("Frequent signals: " + " / ".join(candidate["frequent_signals"]))
    print("[Register]  [Keep Observing]  [Reject]")
    print("Decision: " + candidate["status"])
    print("\nBALANCING | Similarity -> Complementarity")
    print(json.dumps(roles, indent=2))

if __name__ == "__main__":
    main()
