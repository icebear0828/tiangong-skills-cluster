#!/usr/bin/env python3
"""
Compare Skills - A/B 对比两个 Skills
在相同测试集上对比两个 Skill 的表现。
"""

import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import random

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


@dataclass
class CompareResult:
    """对比结果"""
    skill_a: str
    skill_b: str
    test_count: int
    wins_a: int
    wins_b: int
    ties: int
    avg_score_a: float
    avg_score_b: float
    effect_size: float  # Cohen's d
    conclusion: str


def cohens_d(mean1: float, mean2: float, std1: float, std2: float) -> float:
    """计算 Cohen's d 效应量"""
    pooled_std = ((std1 ** 2 + std2 ** 2) / 2) ** 0.5
    if pooled_std == 0:
        return 0.0
    return (mean1 - mean2) / pooled_std


def run_comparison(
    skill_a: str,
    skill_b: str,
    test_cases: List[Dict[str, Any]],
    rounds: int = 1
) -> CompareResult:
    """
    执行对比

    Args:
        skill_a: Skill A ID
        skill_b: Skill B ID
        test_cases: 测试用例列表
        rounds: 每个用例运行轮数

    Returns:
        CompareResult
    """
    scores_a = []
    scores_b = []
    wins_a = 0
    wins_b = 0
    ties = 0

    for test_case in test_cases:
        for _ in range(rounds):
            # 模拟评测（实际应调用 run_eval）
            # 这里简化为随机分数
            score_a = random.uniform(0.6, 1.0)
            score_b = random.uniform(0.6, 1.0)

            scores_a.append(score_a)
            scores_b.append(score_b)

            diff = score_a - score_b
            if abs(diff) < 0.05:  # 差异小于 0.05 视为平局
                ties += 1
            elif diff > 0:
                wins_a += 1
            else:
                wins_b += 1

    avg_a = sum(scores_a) / len(scores_a) if scores_a else 0
    avg_b = sum(scores_b) / len(scores_b) if scores_b else 0

    # 计算标准差
    std_a = (sum((s - avg_a) ** 2 for s in scores_a) / len(scores_a)) ** 0.5 if scores_a else 0
    std_b = (sum((s - avg_b) ** 2 for s in scores_b) / len(scores_b)) ** 0.5 if scores_b else 0

    effect = cohens_d(avg_a, avg_b, std_a, std_b)

    # 结论
    if abs(effect) < 0.2:
        conclusion = "No significant difference"
    elif effect > 0:
        if effect > 0.8:
            conclusion = f"{skill_a} is significantly better (large effect)"
        elif effect > 0.5:
            conclusion = f"{skill_a} is better (medium effect)"
        else:
            conclusion = f"{skill_a} is slightly better (small effect)"
    else:
        if effect < -0.8:
            conclusion = f"{skill_b} is significantly better (large effect)"
        elif effect < -0.5:
            conclusion = f"{skill_b} is better (medium effect)"
        else:
            conclusion = f"{skill_b} is slightly better (small effect)"

    return CompareResult(
        skill_a=skill_a,
        skill_b=skill_b,
        test_count=len(test_cases) * rounds,
        wins_a=wins_a,
        wins_b=wins_b,
        ties=ties,
        avg_score_a=round(avg_a, 3),
        avg_score_b=round(avg_b, 3),
        effect_size=round(effect, 3),
        conclusion=conclusion
    )


def main():
    parser = argparse.ArgumentParser(description="Compare two skills")
    parser.add_argument("--skill-a", required=True, help="First skill ID")
    parser.add_argument("--skill-b", required=True, help="Second skill ID")
    parser.add_argument("--test-suite", required=True, help="Path to test suite JSON")
    parser.add_argument("--rounds", type=int, default=1, help="Rounds per test case")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # 加载测试集
    with open(args.test_suite, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    if not isinstance(test_cases, list):
        test_cases = test_cases.get("cases", [])

    result = run_comparison(
        skill_a=args.skill_a,
        skill_b=args.skill_b,
        test_cases=test_cases,
        rounds=args.rounds
    )

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print("Comparison Result")
        print("=" * 50)
        print(f"Skill A: {result.skill_a}")
        print(f"Skill B: {result.skill_b}")
        print(f"\nTest Count: {result.test_count}")
        print(f"Wins A: {result.wins_a}")
        print(f"Wins B: {result.wins_b}")
        print(f"Ties: {result.ties}")
        print(f"\nAvg Score A: {result.avg_score_a}")
        print(f"Avg Score B: {result.avg_score_b}")
        print(f"Effect Size (Cohen's d): {result.effect_size}")
        print(f"\nConclusion: {result.conclusion}")


if __name__ == "__main__":
    main()
