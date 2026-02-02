#!/usr/bin/env python3
"""
Tournament - 锦标赛选拔
使用 Swiss 制锦标赛对多个 Skills 进行排名。
"""

import json
import sys
import argparse
import random
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


@dataclass
class TournamentResult:
    """锦标赛结果"""
    participants: List[str]
    rounds: int
    final_ranking: List[Dict[str, any]]
    match_history: List[Dict[str, any]]


def simulate_match(skill_a: str, skill_b: str, test_cases: list) -> Tuple[str, float, float]:
    """模拟一场比赛"""
    # 简化：随机生成分数
    score_a = random.uniform(0.6, 1.0)
    score_b = random.uniform(0.6, 1.0)

    if abs(score_a - score_b) < 0.05:
        winner = "tie"
    elif score_a > score_b:
        winner = skill_a
    else:
        winner = skill_b

    return winner, score_a, score_b


def run_tournament(
    skill_ids: List[str],
    test_cases: list,
    rounds: int
) -> TournamentResult:
    """
    执行锦标赛

    Args:
        skill_ids: 参赛 Skill ID 列表
        test_cases: 测试用例
        rounds: 轮数

    Returns:
        TournamentResult
    """
    # 初始化积分
    points = {sid: 0 for sid in skill_ids}
    total_scores = {sid: [] for sid in skill_ids}
    match_history = []

    for round_num in range(1, rounds + 1):
        # Swiss 制：按积分排序，相邻配对
        sorted_skills = sorted(skill_ids, key=lambda x: points[x], reverse=True)

        # 配对
        pairs = []
        used = set()
        for i in range(0, len(sorted_skills) - 1, 2):
            if sorted_skills[i] not in used and sorted_skills[i+1] not in used:
                pairs.append((sorted_skills[i], sorted_skills[i+1]))
                used.add(sorted_skills[i])
                used.add(sorted_skills[i+1])

        # 如果有奇数个，最后一个轮空
        bye_skill = None
        for sid in sorted_skills:
            if sid not in used:
                bye_skill = sid
                points[sid] += 0.5  # 轮空得半分
                break

        # 执行比赛
        for skill_a, skill_b in pairs:
            winner, score_a, score_b = simulate_match(skill_a, skill_b, test_cases)

            total_scores[skill_a].append(score_a)
            total_scores[skill_b].append(score_b)

            if winner == "tie":
                points[skill_a] += 0.5
                points[skill_b] += 0.5
            elif winner == skill_a:
                points[skill_a] += 1
            else:
                points[skill_b] += 1

            match_history.append({
                "round": round_num,
                "skill_a": skill_a,
                "skill_b": skill_b,
                "score_a": round(score_a, 3),
                "score_b": round(score_b, 3),
                "winner": winner
            })

    # 最终排名
    final_ranking = []
    for sid in skill_ids:
        avg_score = sum(total_scores[sid]) / len(total_scores[sid]) if total_scores[sid] else 0
        final_ranking.append({
            "skill_id": sid,
            "points": points[sid],
            "avg_score": round(avg_score, 3),
            "matches": len(total_scores[sid])
        })

    final_ranking.sort(key=lambda x: (x["points"], x["avg_score"]), reverse=True)

    # 添加排名
    for i, entry in enumerate(final_ranking):
        entry["rank"] = i + 1

    return TournamentResult(
        participants=skill_ids,
        rounds=rounds,
        final_ranking=final_ranking,
        match_history=match_history
    )


def main():
    parser = argparse.ArgumentParser(description="Run tournament")
    parser.add_argument("--skill-ids", required=True, help="Comma-separated skill IDs")
    parser.add_argument("--test-suite", required=True, help="Path to test suite JSON")
    parser.add_argument("--rounds", type=int, default=3, help="Number of rounds")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    skill_ids = [s.strip() for s in args.skill_ids.split(",")]

    if len(skill_ids) < 2:
        print("Error: Need at least 2 skills for tournament")
        sys.exit(1)

    # 加载测试集
    with open(args.test_suite, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
        if not isinstance(test_cases, list):
            test_cases = test_cases.get("cases", [])

    result = run_tournament(skill_ids, test_cases, args.rounds)

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print("Tournament Results")
        print("=" * 50)
        print(f"Participants: {len(result.participants)}")
        print(f"Rounds: {result.rounds}")

        print("\nFinal Ranking:")
        print("-" * 40)
        for entry in result.final_ranking:
            print(f"  #{entry['rank']} {entry['skill_id']}: {entry['points']} pts (avg: {entry['avg_score']})")

        print("\nMatch History:")
        print("-" * 40)
        for match in result.match_history:
            print(f"  Round {match['round']}: {match['skill_a']} vs {match['skill_b']} -> {match['winner']}")


if __name__ == "__main__":
    main()
