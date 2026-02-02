#!/usr/bin/env python3
"""
Propose Revision - 提议修订
基于反馈生成 Skill 修订提案。
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, Any, List

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


@dataclass
class Revision:
    """修订提案"""
    skill_id: str
    revision_id: str
    timestamp: str
    revision_type: str  # instruction, script, reference, structure
    description: str
    changes: List[Dict[str, str]]  # {file, before, after}
    estimated_improvement: float
    risk_level: str  # low, medium, high


def generate_revision_id() -> str:
    """生成修订 ID"""
    import uuid
    return f"rev_{uuid.uuid4().hex[:8]}"


def propose_instruction_revision(skill_id: str, feedback: Dict[str, Any]) -> Revision:
    """提议指令修订"""
    suggestions = feedback.get("suggestions", [])
    priority_areas = feedback.get("priority_areas", [])

    changes = []

    # 根据反馈生成修改建议
    if "correctness" in priority_areas:
        changes.append({
            "file": "SKILL.md",
            "section": "执行流程",
            "change_type": "enhance",
            "description": "Add output validation step"
        })

    if "efficiency" in priority_areas:
        changes.append({
            "file": "SKILL.md",
            "section": "执行流程",
            "change_type": "optimize",
            "description": "Reduce context usage by summarizing intermediate outputs"
        })

    return Revision(
        skill_id=skill_id,
        revision_id=generate_revision_id(),
        timestamp=datetime.utcnow().isoformat() + "Z",
        revision_type="instruction",
        description=f"Instruction revision based on feedback: {', '.join(priority_areas)}",
        changes=changes,
        estimated_improvement=0.1,
        risk_level="low"
    )


def propose_script_revision(skill_id: str, feedback: Dict[str, Any]) -> Revision:
    """提议脚本修订"""
    changes = []

    if feedback.get("severity") == "high":
        changes.append({
            "file": "scripts/main.py",
            "section": "core_logic",
            "change_type": "refactor",
            "description": "Refactor core logic to handle edge cases"
        })

    return Revision(
        skill_id=skill_id,
        revision_id=generate_revision_id(),
        timestamp=datetime.utcnow().isoformat() + "Z",
        revision_type="script",
        description="Script revision for improved robustness",
        changes=changes,
        estimated_improvement=0.15,
        risk_level="medium"
    )


def propose_revision(skill_id: str, feedback: Dict[str, Any]) -> Revision:
    """
    根据反馈生成修订提案

    Args:
        skill_id: Skill ID
        feedback: 反馈数据

    Returns:
        Revision
    """
    severity = feedback.get("severity", "low")

    if severity == "high":
        # 高严重性：脚本修订
        return propose_script_revision(skill_id, feedback)
    else:
        # 低/中严重性：指令修订
        return propose_instruction_revision(skill_id, feedback)


def main():
    parser = argparse.ArgumentParser(description="Propose skill revision")
    parser.add_argument("--skill-id", required=True, help="Skill ID")
    parser.add_argument("--feedback", required=True, help="Path to feedback JSON")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    with open(args.feedback, "r", encoding="utf-8") as f:
        feedback = json.load(f)

    revision = propose_revision(args.skill_id, feedback)

    output = asdict(revision)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Revision proposal saved to {args.output}")
    elif args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("Revision Proposal")
        print("=" * 50)
        print(f"Skill: {revision.skill_id}")
        print(f"Revision ID: {revision.revision_id}")
        print(f"Type: {revision.revision_type}")
        print(f"Description: {revision.description}")
        print(f"Estimated Improvement: +{revision.estimated_improvement:.0%}")
        print(f"Risk Level: {revision.risk_level}")
        print(f"\nChanges:")
        for c in revision.changes:
            print(f"  - {c['file']}: {c['description']}")


if __name__ == "__main__":
    main()
