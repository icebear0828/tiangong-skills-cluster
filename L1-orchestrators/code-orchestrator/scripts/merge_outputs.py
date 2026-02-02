#!/usr/bin/env python3
"""
Merge Outputs - 合并多个 Skill 的输出
将编排过程中各个 skill 的输出合并为统一的结果。
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime


@dataclass
class SkillOutput:
    """单个 Skill 的输出"""
    step_id: str
    skill_id: str
    status: str  # completed / failed / skipped
    output_files: List[str]
    output_summary: str
    quality_score: float
    execution_time_ms: int
    error_message: Optional[str] = None


@dataclass
class MergedOutput:
    """合并后的输出"""
    task_id: str
    status: str  # completed / partial / failed
    pattern: str
    outputs: Dict[str, List[str]]  # 按类型分组的输出文件
    quality_scores: Dict[str, float]
    overall_quality: float
    execution_log: List[Dict[str, Any]]
    created_at: str
    total_execution_time_ms: int


def categorize_files(files: List[str]) -> Dict[str, List[str]]:
    """将文件按类型分类"""
    categories = {
        "code_files": [],
        "test_files": [],
        "doc_files": [],
        "config_files": [],
        "other_files": [],
    }

    for f in files:
        f_lower = f.lower()
        if "test" in f_lower or f_lower.startswith("test_"):
            categories["test_files"].append(f)
        elif f_lower.endswith((".md", ".rst", ".txt")):
            categories["doc_files"].append(f)
        elif f_lower.endswith((".json", ".yaml", ".yml", ".toml", ".ini")):
            categories["config_files"].append(f)
        elif f_lower.endswith((".py", ".js", ".ts", ".java", ".go", ".rs")):
            categories["code_files"].append(f)
        else:
            categories["other_files"].append(f)

    # 移除空类别
    return {k: v for k, v in categories.items() if v}


def calculate_overall_quality(scores: Dict[str, float]) -> float:
    """计算总体质量分数"""
    if not scores:
        return 0.0

    # 加权平均，关键 skill 权重更高
    weights = {
        "code-gen": 1.5,
        "debug": 1.5,
        "test-gen": 1.2,
        "code-review": 1.0,
        "refactor": 1.0,
        "doc-gen": 0.8,
    }

    total_weight = 0
    weighted_sum = 0

    for skill_id, score in scores.items():
        weight = weights.get(skill_id, 1.0)
        weighted_sum += score * weight
        total_weight += weight

    return round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0


def merge_outputs(
    task_id: str,
    pattern: str,
    skill_outputs: List[SkillOutput]
) -> MergedOutput:
    """
    合并多个 Skill 的输出

    Args:
        task_id: 任务 ID
        pattern: 执行模式
        skill_outputs: 各 Skill 的输出列表

    Returns:
        MergedOutput 对象
    """
    # 收集所有输出文件
    all_files = []
    quality_scores = {}
    execution_log = []
    total_time = 0

    completed_count = 0
    failed_count = 0

    for output in skill_outputs:
        # 收集文件
        all_files.extend(output.output_files)

        # 收集质量分数
        if output.status == "completed":
            quality_scores[output.skill_id] = output.quality_score
            completed_count += 1
        elif output.status == "failed":
            failed_count += 1

        # 记录执行日志
        execution_log.append({
            "step_id": output.step_id,
            "skill_id": output.skill_id,
            "status": output.status,
            "quality_score": output.quality_score,
            "execution_time_ms": output.execution_time_ms,
            "error_message": output.error_message,
        })

        total_time += output.execution_time_ms

    # 分类文件
    categorized_files = categorize_files(all_files)

    # 计算总体质量
    overall_quality = calculate_overall_quality(quality_scores)

    # 确定总体状态
    if failed_count == 0 and completed_count > 0:
        status = "completed"
    elif completed_count > 0:
        status = "partial"
    else:
        status = "failed"

    return MergedOutput(
        task_id=task_id,
        status=status,
        pattern=pattern,
        outputs=categorized_files,
        quality_scores=quality_scores,
        overall_quality=overall_quality,
        execution_log=execution_log,
        created_at=datetime.utcnow().isoformat() + "Z",
        total_execution_time_ms=total_time
    )


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Merge Outputs - 合并输出")
    parser.add_argument("--task-id", type=str, required=True, help="Task ID")
    parser.add_argument("--pattern", type=str, default="sequential", help="Execution pattern")
    parser.add_argument("--inputs", type=str, required=True, help="Path to inputs JSON file")
    parser.add_argument("--output", type=str, help="Output file path")

    args = parser.parse_args()

    # 加载输入
    with open(args.inputs, 'r', encoding='utf-8') as f:
        inputs_data = json.load(f)

    # 转换为 SkillOutput 对象
    skill_outputs = []
    for item in inputs_data:
        skill_outputs.append(SkillOutput(
            step_id=item.get("step_id", ""),
            skill_id=item.get("skill_id", ""),
            status=item.get("status", "completed"),
            output_files=item.get("output_files", []),
            output_summary=item.get("output_summary", ""),
            quality_score=item.get("quality_score", 0.0),
            execution_time_ms=item.get("execution_time_ms", 0),
            error_message=item.get("error_message"),
        ))

    # 合并
    result = merge_outputs(args.task_id, args.pattern, skill_outputs)

    # 输出
    output_json = json.dumps(asdict(result), indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output_json, encoding='utf-8')
        print(f"Output written to {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
