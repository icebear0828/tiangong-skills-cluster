#!/usr/bin/env python3
"""
Score Skill - 计算 Skill 适应度分数
根据评测结果计算综合适应度。
"""

import json
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import update_skill, get_skill


def calculate_aggregated_fitness(eval_results: list) -> float:
    """聚合多次评测结果"""
    if not eval_results:
        return 0.0

    # 使用指数加权，最近的评测权重更高
    weights = []
    weight = 1.0
    for _ in eval_results:
        weights.append(weight)
        weight *= 0.9  # 衰减因子

    weights.reverse()  # 最新的权重最高
    total_weight = sum(weights)

    weighted_sum = sum(r.get("fitness", 0) * w for r, w in zip(eval_results, weights))

    return round(weighted_sum / total_weight, 3) if total_weight > 0 else 0.0


def load_eval_history(skill_id: str, limit: int = 10) -> list:
    """加载 Skill 的评测历史"""
    history_path = PROJECT_ROOT / ".tiangong" / "eval-history.jsonl"

    if not history_path.exists():
        return []

    results = []
    with open(history_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                if record.get("skill_id") == skill_id:
                    results.append(record)

    # 返回最近的记录
    return results[-limit:]


def main():
    parser = argparse.ArgumentParser(description="Calculate skill fitness score")
    parser.add_argument("--skill-id", required=True, help="Skill ID")
    parser.add_argument("--eval-results", help="Path to eval results JSON")
    parser.add_argument("--update-registry", action="store_true", help="Update registry with new score")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # 加载评测结果
    if args.eval_results:
        with open(args.eval_results, "r", encoding="utf-8") as f:
            eval_results = json.load(f)
            if not isinstance(eval_results, list):
                eval_results = [eval_results]
    else:
        eval_results = load_eval_history(args.skill_id)

    if not eval_results:
        print(f"No evaluation results found for skill: {args.skill_id}")
        sys.exit(1)

    # 计算适应度
    fitness = calculate_aggregated_fitness(eval_results)

    # 更新注册表
    if args.update_registry:
        try:
            update_skill(args.skill_id, {"fitness_score": fitness})
            print(f"Updated registry with fitness score: {fitness}")
        except Exception as e:
            print(f"Warning: Could not update registry: {e}")

    # 输出
    if args.json:
        result = {
            "skill_id": args.skill_id,
            "fitness_score": fitness,
            "eval_count": len(eval_results),
            "latest_scores": [r.get("fitness") for r in eval_results[-5:]]
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"Skill: {args.skill_id}")
        print(f"Aggregated Fitness: {fitness}")
        print(f"Based on {len(eval_results)} evaluation(s)")


if __name__ == "__main__":
    main()
