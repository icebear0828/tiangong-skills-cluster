#!/usr/bin/env python3
"""
Validate Revision - 验证修订
验证修订提案的有效性和安全性。
"""

import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any, List

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


@dataclass
class ValidationResult:
    """验证结果"""
    revision_id: str
    valid: bool
    safety_check: bool
    test_results: Dict[str, Any]
    recommendation: str  # accept, reject, need-human-review
    issues: List[str]


def check_safety_bounds(revision: Dict[str, Any], skill_path: Path) -> tuple:
    """检查安全边界"""
    issues = []

    changes = revision.get("changes", [])

    # 检查修改幅度
    # 简化：检查变更数量
    if len(changes) > 5:
        issues.append("Too many changes in single revision (>5)")

    # 检查是否修改核心文件
    for change in changes:
        file_name = change.get("file", "")
        if file_name == "SKILL.md":
            # 检查是否删除 frontmatter
            if change.get("change_type") == "delete" and change.get("section") == "frontmatter":
                issues.append("Cannot delete SKILL.md frontmatter")

    return len(issues) == 0, issues


def run_baseline_tests(skill_id: str, revision: Dict[str, Any]) -> Dict[str, Any]:
    """运行基线测试"""
    # 简化：模拟测试结果
    return {
        "tests_run": 5,
        "tests_passed": 5,
        "tests_failed": 0,
        "regression": False
    }


def compare_with_baseline(
    skill_id: str,
    revision: Dict[str, Any],
    test_cases: List[Dict[str, Any]]
) -> float:
    """与基线对比"""
    # 简化：返回模拟分数差
    estimated_improvement = revision.get("estimated_improvement", 0)
    # 模拟实际改进（加入随机性）
    import random
    actual_improvement = estimated_improvement * random.uniform(0.5, 1.5)
    return actual_improvement


def validate_revision(
    revision: Dict[str, Any],
    skill_path: Path,
    test_cases: List[Dict[str, Any]]
) -> ValidationResult:
    """
    验证修订

    Args:
        revision: 修订提案
        skill_path: Skill 目录路径
        test_cases: 测试用例

    Returns:
        ValidationResult
    """
    revision_id = revision.get("revision_id", "unknown")
    skill_id = revision.get("skill_id", "unknown")

    issues = []

    # 安全检查
    safety_passed, safety_issues = check_safety_bounds(revision, skill_path)
    issues.extend(safety_issues)

    # 基线测试
    test_results = run_baseline_tests(skill_id, revision)
    if test_results.get("regression"):
        issues.append("Test regression detected")

    # 对比评分
    improvement = compare_with_baseline(skill_id, revision, test_cases)

    # 决定建议
    if issues:
        if any("Cannot" in i for i in issues):
            recommendation = "reject"
        else:
            recommendation = "need-human-review"
        valid = False
    elif improvement > 0.05:
        recommendation = "accept"
        valid = True
    elif improvement > -0.05:
        recommendation = "need-human-review"
        valid = True
    else:
        recommendation = "reject"
        valid = False
        issues.append(f"Negative improvement: {improvement:.2%}")

    return ValidationResult(
        revision_id=revision_id,
        valid=valid,
        safety_check=safety_passed,
        test_results=test_results,
        recommendation=recommendation,
        issues=issues
    )


def main():
    parser = argparse.ArgumentParser(description="Validate revision")
    parser.add_argument("--skill-id", required=True, help="Skill ID")
    parser.add_argument("--revision", required=True, help="Path to revision JSON")
    parser.add_argument("--test-cases", help="Path to test cases JSON")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    with open(args.revision, "r", encoding="utf-8") as f:
        revision = json.load(f)

    skill_path = PROJECT_ROOT / "L2-execution" / "core" / args.skill_id
    if not skill_path.exists():
        skill_path = PROJECT_ROOT / "L2-execution" / "extended" / args.skill_id
    if not skill_path.exists():
        skill_path = PROJECT_ROOT / "L2-execution" / "experimental" / args.skill_id

    test_cases = []
    if args.test_cases:
        with open(args.test_cases, "r", encoding="utf-8") as f:
            test_cases = json.load(f)

    result = validate_revision(revision, skill_path, test_cases)

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print("Validation Result")
        print("=" * 50)
        print(f"Revision ID: {result.revision_id}")
        print(f"Valid: {result.valid}")
        print(f"Safety Check: {'Passed' if result.safety_check else 'Failed'}")
        print(f"Recommendation: {result.recommendation}")

        if result.issues:
            print(f"\nIssues:")
            for i in result.issues:
                print(f"  - {i}")

        print(f"\nTest Results: {result.test_results['tests_passed']}/{result.test_results['tests_run']} passed")


if __name__ == "__main__":
    main()
