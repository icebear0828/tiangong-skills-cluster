#!/usr/bin/env python3
"""
Run Eval - 执行评测
对 Skill 的执行结果进行评测。
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


@dataclass
class EvalResult:
    """评测结果"""
    timestamp: str
    skill_id: str
    eval_type: str
    task_type: str
    scores: Dict[str, float]
    fitness: float
    details: Dict[str, Any]


# 评测维度权重
WEIGHTS = {
    "code": {
        "correctness": 0.4,
        "quality": 0.25,
        "architecture": 0.2,
        "efficiency": 0.15
    },
    "doc": {
        "completeness": 0.35,
        "accuracy": 0.30,
        "readability": 0.20,
        "format": 0.15
    },
    "general": {
        "correctness": 0.4,
        "quality": 0.3,
        "efficiency": 0.3
    }
}


def calculate_fitness(scores: Dict[str, float], task_type: str) -> float:
    """计算适应度分数"""
    weights = WEIGHTS.get(task_type, WEIGHTS["general"])

    total_weight = 0
    weighted_sum = 0

    for dimension, weight in weights.items():
        if dimension in scores:
            weighted_sum += scores[dimension] * weight
            total_weight += weight

    if total_weight == 0:
        return 0.0

    return round(weighted_sum / total_weight, 3)


def evaluate_code_output(output: str, expected: Optional[str], criteria: Dict[str, Any]) -> Dict[str, float]:
    """评估代码类输出"""
    scores = {}

    # 正确性：简化评估
    if expected:
        # 检查关键元素是否存在
        keywords = criteria.get("required_keywords", [])
        found = sum(1 for kw in keywords if kw.lower() in output.lower())
        scores["correctness"] = found / len(keywords) if keywords else 0.5
    else:
        scores["correctness"] = 0.7  # 无预期时给默认分

    # 质量：简化评估（检查基本要素）
    quality_indicators = [
        "def " in output or "function " in output or "class " in output,
        len(output) > 50,
        "#" in output or "//" in output or '"""' in output,  # 注释
    ]
    scores["quality"] = sum(quality_indicators) / len(quality_indicators)

    # 架构：简化评估
    scores["architecture"] = 0.7  # 默认

    # 效率：简化评估
    scores["efficiency"] = 0.7  # 默认

    return scores


def evaluate_doc_output(output: str, expected: Optional[str], criteria: Dict[str, Any]) -> Dict[str, float]:
    """评估文档类输出"""
    scores = {}

    # 完整性
    required_sections = criteria.get("required_sections", [])
    if required_sections:
        found = sum(1 for sec in required_sections if sec.lower() in output.lower())
        scores["completeness"] = found / len(required_sections)
    else:
        scores["completeness"] = 0.7

    # 准确性：简化
    scores["accuracy"] = 0.7

    # 可读性
    # 简单指标：段落长度、结构
    lines = output.split("\n")
    has_structure = any(line.startswith("#") or line.startswith("-") for line in lines)
    scores["readability"] = 0.8 if has_structure else 0.5

    # 格式
    scores["format"] = 0.8 if output.strip() else 0.0

    return scores


def run_evaluation(
    skill_id: str,
    task_type: str,
    output: str,
    expected: Optional[str] = None,
    criteria: Optional[Dict[str, Any]] = None
) -> EvalResult:
    """
    执行评测

    Args:
        skill_id: Skill ID
        task_type: 任务类型 (code, doc, general)
        output: Skill 输出
        expected: 预期输出
        criteria: 评测标准

    Returns:
        EvalResult
    """
    criteria = criteria or {}

    if task_type == "code":
        scores = evaluate_code_output(output, expected, criteria)
    elif task_type == "doc":
        scores = evaluate_doc_output(output, expected, criteria)
    else:
        scores = {
            "correctness": 0.7,
            "quality": 0.7,
            "efficiency": 0.7
        }

    fitness = calculate_fitness(scores, task_type)

    return EvalResult(
        timestamp=datetime.utcnow().isoformat() + "Z",
        skill_id=skill_id,
        eval_type="single",
        task_type=task_type,
        scores=scores,
        fitness=fitness,
        details={
            "output_length": len(output),
            "has_expected": expected is not None,
            "criteria_used": list(criteria.keys())
        }
    )


def save_eval_result(result: EvalResult, history_path: Optional[Path] = None):
    """保存评测结果到历史"""
    if history_path is None:
        history_path = PROJECT_ROOT / ".tiangong" / "eval-history.jsonl"

    history_path.parent.mkdir(parents=True, exist_ok=True)

    with open(history_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(result), ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Run evaluation")
    parser.add_argument("--skill-id", required=True, help="Skill ID")
    parser.add_argument("--task-type", required=True, choices=["code", "doc", "data", "general"])
    parser.add_argument("--output", required=True, help="Path to output file or output string")
    parser.add_argument("--expected", help="Path to expected output or expected string")
    parser.add_argument("--criteria", help="Path to criteria JSON")
    parser.add_argument("--save", action="store_true", help="Save to history")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # 读取输出
    output_path = Path(args.output)
    if output_path.exists():
        output = output_path.read_text(encoding="utf-8")
    else:
        output = args.output

    # 读取预期
    expected = None
    if args.expected:
        expected_path = Path(args.expected)
        if expected_path.exists():
            expected = expected_path.read_text(encoding="utf-8")
        else:
            expected = args.expected

    # 读取标准
    criteria = {}
    if args.criteria:
        with open(args.criteria, "r", encoding="utf-8") as f:
            criteria = json.load(f)

    # 执行评测
    result = run_evaluation(
        skill_id=args.skill_id,
        task_type=args.task_type,
        output=output,
        expected=expected,
        criteria=criteria
    )

    # 保存
    if args.save:
        save_eval_result(result)

    # 输出
    if args.json:
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    else:
        print("Evaluation Result")
        print("=" * 40)
        print(f"Skill: {result.skill_id}")
        print(f"Type: {result.task_type}")
        print(f"Fitness: {result.fitness}")
        print("\nScores:")
        for dim, score in result.scores.items():
            print(f"  {dim}: {score:.2f}")


if __name__ == "__main__":
    main()
