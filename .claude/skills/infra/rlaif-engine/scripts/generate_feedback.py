#!/usr/bin/env python3
"""
Generate Feedback - 生成反馈
分析 Skill 执行结果，生成结构化反馈。
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
class Feedback:
    """结构化反馈"""
    skill_id: str
    timestamp: str
    correctness_gap: str
    efficiency_gap: str
    patterns: List[str]
    suggestions: List[str]
    severity: str  # low, medium, high
    priority_areas: List[str]


def analyze_execution(
    skill_id: str,
    execution_log: Dict[str, Any],
    expected_output: str
) -> Feedback:
    """
    分析执行结果生成反馈

    Args:
        skill_id: Skill ID
        execution_log: 执行日志
        expected_output: 预期输出

    Returns:
        Feedback
    """
    actual_output = execution_log.get("output", "")
    metrics = execution_log.get("metrics", {})

    # 分析正确性差距
    correctness_issues = []
    if expected_output and actual_output:
        if expected_output not in actual_output:
            correctness_issues.append("Output doesn't match expected")
        if len(actual_output) < len(expected_output) * 0.5:
            correctness_issues.append("Output is significantly shorter than expected")

    correctness_gap = "; ".join(correctness_issues) if correctness_issues else "Meets expectations"

    # 分析效率差距
    tokens_used = metrics.get("tokens_used", 0)
    execution_time = metrics.get("execution_time_ms", 0)

    efficiency_issues = []
    if tokens_used > 5000:
        efficiency_issues.append(f"High token usage: {tokens_used}")
    if execution_time > 30000:
        efficiency_issues.append(f"Slow execution: {execution_time}ms")

    efficiency_gap = "; ".join(efficiency_issues) if efficiency_issues else "Efficient"

    # 识别模式
    patterns = []
    if "error" in actual_output.lower():
        patterns.append("Contains error messages")
    if "todo" in actual_output.lower():
        patterns.append("Contains TODO markers")
    if len(actual_output.split("\n")) > 100:
        patterns.append("Output is verbose")

    # 生成建议
    suggestions = []
    if correctness_issues:
        suggestions.append("Review output format and completeness")
        suggestions.append("Add validation for expected output structure")
    if efficiency_issues:
        suggestions.append("Optimize token usage with more concise prompts")
        suggestions.append("Consider caching or pre-computation")

    # 确定严重程度
    if correctness_issues:
        severity = "high"
    elif efficiency_issues:
        severity = "medium"
    else:
        severity = "low"

    # 优先改进领域
    priority_areas = []
    if correctness_issues:
        priority_areas.append("correctness")
    if efficiency_issues:
        priority_areas.append("efficiency")
    if patterns:
        priority_areas.append("output_quality")

    return Feedback(
        skill_id=skill_id,
        timestamp=datetime.utcnow().isoformat() + "Z",
        correctness_gap=correctness_gap,
        efficiency_gap=efficiency_gap,
        patterns=patterns,
        suggestions=suggestions,
        severity=severity,
        priority_areas=priority_areas or ["none"]
    )


def save_feedback(feedback: Feedback, log_path: Path = None):
    """保存反馈到日志"""
    if log_path is None:
        log_path = PROJECT_ROOT / ".tiangong" / "rlaif-log.jsonl"

    log_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": feedback.timestamp,
        "skill_id": feedback.skill_id,
        "mode": "feedback-driven",
        "action": "generate_feedback",
        "details": asdict(feedback)
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Generate feedback for skill execution")
    parser.add_argument("--skill-id", required=True, help="Skill ID")
    parser.add_argument("--execution-log", required=True, help="Path to execution log JSON")
    parser.add_argument("--expected-output", help="Path to expected output or string")
    parser.add_argument("--save", action="store_true", help="Save to RLAIF log")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # 加载执行日志
    with open(args.execution_log, "r", encoding="utf-8") as f:
        execution_log = json.load(f)

    # 加载预期输出
    expected_output = ""
    if args.expected_output:
        expected_path = Path(args.expected_output)
        if expected_path.exists():
            expected_output = expected_path.read_text(encoding="utf-8")
        else:
            expected_output = args.expected_output

    feedback = analyze_execution(args.skill_id, execution_log, expected_output)

    if args.save:
        save_feedback(feedback)

    if args.json:
        print(json.dumps(asdict(feedback), indent=2, ensure_ascii=False))
    else:
        print("Generated Feedback")
        print("=" * 50)
        print(f"Skill: {feedback.skill_id}")
        print(f"Severity: {feedback.severity}")
        print(f"\nCorrectness Gap: {feedback.correctness_gap}")
        print(f"Efficiency Gap: {feedback.efficiency_gap}")
        print(f"\nPatterns: {', '.join(feedback.patterns) or 'None'}")
        print(f"\nSuggestions:")
        for s in feedback.suggestions:
            print(f"  - {s}")
        print(f"\nPriority Areas: {', '.join(feedback.priority_areas)}")


if __name__ == "__main__":
    main()
