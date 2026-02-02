#!/usr/bin/env python3
"""
Plan Generator - DAG 执行计划生成器
根据任务分析结果生成可执行的 DAG 计划。
"""

import json
import sys
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any, Set
from pathlib import Path
from datetime import datetime
import uuid

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


@dataclass
class PlanStep:
    """执行计划步骤"""
    step_id: str
    skill_id: str
    name: str
    description: str
    input_from: List[str] = field(default_factory=list)  # 依赖的 step_id
    output_to: List[str] = field(default_factory=list)   # 输出到的 step_id
    estimated_tokens: int = 0
    fallback_skill: Optional[str] = None
    max_retries: int = 2
    quality_threshold: float = 0.7


@dataclass
class ExecutionPlan:
    """执行计划"""
    plan_id: str
    task_description: str
    pattern: str                 # sequential / parallel / iterative / dag
    steps: List[PlanStep]
    total_estimated_tokens: int
    total_estimated_steps: int
    complexity: str
    fallback_strategy: str
    created_at: str
    context_budget: int = 0      # context 预算（tokens）
    max_parallel: int = 3        # 最大并行数


# Skill 依赖关系图（哪些 Skill 通常一起使用）
SKILL_DEPENDENCIES = {
    "code-gen": {
        "often_after": ["api-design", "db-schema", "arch-explore"],
        "often_before": ["test-gen", "code-review", "doc-gen"],
        "estimated_tokens": 2000
    },
    "test-gen": {
        "often_after": ["code-gen"],
        "often_before": ["code-review"],
        "estimated_tokens": 1500
    },
    "code-review": {
        "often_after": ["code-gen", "test-gen", "refactor"],
        "often_before": [],
        "estimated_tokens": 1000
    },
    "doc-gen": {
        "often_after": ["code-gen", "api-design"],
        "often_before": [],
        "estimated_tokens": 1200
    },
    "refactor": {
        "often_after": ["code-review", "debug"],
        "often_before": ["test-gen", "code-review"],
        "estimated_tokens": 1800
    },
    "debug": {
        "often_after": [],
        "often_before": ["test-gen"],
        "estimated_tokens": 1500
    },
    "api-design": {
        "often_after": ["arch-explore"],
        "often_before": ["code-gen", "doc-gen"],
        "estimated_tokens": 1000
    },
    "db-schema": {
        "often_after": ["arch-explore"],
        "often_before": ["code-gen"],
        "estimated_tokens": 800
    },
    "perf-optimize": {
        "often_after": ["code-gen", "code-review"],
        "often_before": ["test-gen"],
        "estimated_tokens": 1500
    },
    "security-audit": {
        "often_after": ["code-gen"],
        "often_before": [],
        "estimated_tokens": 1200
    },
    "creative-code": {
        "often_after": [],
        "often_before": ["code-review"],
        "estimated_tokens": 2500
    },
    "arch-explore": {
        "often_after": [],
        "often_before": ["api-design", "db-schema", "code-gen"],
        "estimated_tokens": 1500
    },
    "prototype": {
        "often_after": ["arch-explore"],
        "often_before": ["code-gen"],
        "estimated_tokens": 2000
    },
}

# 常用 DAG 模板
DAG_TEMPLATES = {
    "basic-code": {
        "pattern": "sequential",
        "steps": ["code-gen", "test-gen", "code-review"],
        "description": "基础代码开发流程"
    },
    "full-feature": {
        "pattern": "sequential",
        "steps": ["api-design", "code-gen", "test-gen", "doc-gen"],
        "description": "完整功能开发流程"
    },
    "code-quality": {
        "pattern": "iterative",
        "steps": ["code-gen", "code-review", "refactor"],
        "max_iterations": 3,
        "description": "质量驱动开发流程"
    },
    "full-stack": {
        "pattern": "dag",
        "steps": {
            "api-design": [],
            "db-schema": [],
            "code-gen": ["api-design", "db-schema"],
            "test-gen": ["code-gen"],
            "doc-gen": ["api-design", "code-gen"]
        },
        "description": "全栈开发流程"
    },
    "debug-fix": {
        "pattern": "sequential",
        "steps": ["debug", "refactor", "test-gen"],
        "description": "Bug 修复流程"
    },
    "security-review": {
        "pattern": "sequential",
        "steps": ["security-audit", "refactor", "test-gen"],
        "description": "安全审查流程"
    },
    "performance": {
        "pattern": "iterative",
        "steps": ["perf-optimize", "test-gen", "code-review"],
        "max_iterations": 2,
        "description": "性能优化流程"
    },
    "exploration": {
        "pattern": "sequential",
        "steps": ["arch-explore", "prototype", "code-review"],
        "description": "探索性开发流程"
    },
}


def load_registry() -> Dict[str, Any]:
    """加载 Skill 注册表"""
    registry_path = PROJECT_ROOT / "registry.json"
    if registry_path.exists():
        with open(registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"skills": {}}


def get_available_skills(registry: Dict[str, Any]) -> Set[str]:
    """获取可用的 Skill 列表"""
    return {
        sid for sid, skill in registry.get("skills", {}).items()
        if skill.get("status") in ("active", "temp")
    }


def select_template(analysis: Dict[str, Any]) -> str:
    """根据分析结果选择 DAG 模板"""
    domains = analysis.get("domains", [])
    skill_matches = analysis.get("skill_matches", [])
    complexity = analysis.get("complexity", "S")

    # 根据 Skill 匹配选择
    if skill_matches:
        top_skill = skill_matches[0].get("skill_id", "")

        if top_skill == "debug":
            return "debug-fix"
        elif top_skill == "security-audit":
            return "security-review"
        elif top_skill == "perf-optimize":
            return "performance"
        elif top_skill in ("arch-explore", "creative-code", "prototype"):
            return "exploration"

    # 根据领域选择
    if "data" in domains and "code" in domains:
        return "full-stack"

    if "security" in domains:
        return "security-review"

    if "perf" in domains:
        return "performance"

    # 根据复杂度选择
    if complexity == "S":
        return "basic-code"
    elif complexity in ("M", "L"):
        return "full-feature"
    else:
        return "full-stack"


def build_steps_from_template(
    template_name: str,
    available_skills: Set[str],
    analysis: Dict[str, Any]
) -> List[PlanStep]:
    """从模板构建步骤列表"""
    template = DAG_TEMPLATES.get(template_name, DAG_TEMPLATES["basic-code"])
    pattern = template["pattern"]
    steps = []

    if pattern in ("sequential", "iterative"):
        step_list = template["steps"]
        prev_step_id = None

        for i, skill_id in enumerate(step_list):
            if skill_id not in available_skills:
                # 尝试找替代
                continue

            step_id = f"step_{i+1}"
            skill_info = SKILL_DEPENDENCIES.get(skill_id, {})

            step = PlanStep(
                step_id=step_id,
                skill_id=skill_id,
                name=f"Execute {skill_id}",
                description=f"Run {skill_id} skill",
                input_from=[prev_step_id] if prev_step_id else [],
                estimated_tokens=skill_info.get("estimated_tokens", 1000),
                max_retries=3 if pattern == "iterative" else 2
            )

            steps.append(step)
            prev_step_id = step_id

    elif pattern == "dag":
        step_deps = template["steps"]
        step_id_map = {}

        # 第一遍：创建所有步骤
        for i, (skill_id, deps) in enumerate(step_deps.items()):
            if skill_id not in available_skills:
                continue

            step_id = f"step_{i+1}"
            step_id_map[skill_id] = step_id
            skill_info = SKILL_DEPENDENCIES.get(skill_id, {})

            step = PlanStep(
                step_id=step_id,
                skill_id=skill_id,
                name=f"Execute {skill_id}",
                description=f"Run {skill_id} skill",
                estimated_tokens=skill_info.get("estimated_tokens", 1000)
            )
            steps.append(step)

        # 第二遍：建立依赖关系
        for skill_id, deps in step_deps.items():
            if skill_id not in step_id_map:
                continue

            step_id = step_id_map[skill_id]
            step = next((s for s in steps if s.step_id == step_id), None)

            if step:
                for dep_skill in deps:
                    if dep_skill in step_id_map:
                        step.input_from.append(step_id_map[dep_skill])

    # 更新 output_to 关系
    for step in steps:
        for other_step in steps:
            if step.step_id in other_step.input_from:
                step.output_to.append(other_step.step_id)

    return steps


def topological_sort(steps: List[PlanStep]) -> List[PlanStep]:
    """拓扑排序步骤"""
    in_degree = {s.step_id: len(s.input_from) for s in steps}
    step_map = {s.step_id: s for s in steps}
    queue = [sid for sid, deg in in_degree.items() if deg == 0]
    sorted_steps = []

    while queue:
        current = queue.pop(0)
        sorted_steps.append(step_map[current])

        for step in steps:
            if current in step.input_from:
                in_degree[step.step_id] -= 1
                if in_degree[step.step_id] == 0:
                    queue.append(step.step_id)

    return sorted_steps


def calculate_estimates(steps: List[PlanStep]) -> tuple:
    """计算总估算"""
    total_tokens = sum(s.estimated_tokens for s in steps)
    total_steps = len(steps)
    return total_tokens, total_steps


def generate_fallback_strategy(complexity: str, steps: List[PlanStep]) -> str:
    """生成回退策略"""
    if complexity == "S":
        return "retry_once_then_abort"
    elif complexity == "M":
        return "retry_with_feedback_then_escalate"
    elif complexity == "L":
        return "retry_then_simplify_then_escalate"
    else:  # XL
        return "checkpoint_and_human_review"


def generate_plan(
    analysis: Dict[str, Any],
    registry: Optional[Dict[str, Any]] = None,
    task_description: str = ""
) -> ExecutionPlan:
    """
    生成执行计划

    Args:
        analysis: task_analyzer 的输出
        registry: Skill 注册表
        task_description: 原始任务描述

    Returns:
        ExecutionPlan
    """
    if registry is None:
        registry = load_registry()

    available_skills = get_available_skills(registry)
    complexity = analysis.get("complexity", "M")

    # 选择模板
    template_name = select_template(analysis)
    template = DAG_TEMPLATES.get(template_name, DAG_TEMPLATES["basic-code"])

    # 构建步骤
    steps = build_steps_from_template(template_name, available_skills, analysis)

    # 拓扑排序
    steps = topological_sort(steps)

    # 计算估算
    total_tokens, total_steps = calculate_estimates(steps)

    # 生成回退策略
    fallback = generate_fallback_strategy(complexity, steps)

    # 创建计划
    plan = ExecutionPlan(
        plan_id=f"plan_{uuid.uuid4().hex[:8]}",
        task_description=task_description,
        pattern=template["pattern"],
        steps=steps,
        total_estimated_tokens=total_tokens,
        total_estimated_steps=total_steps,
        complexity=complexity,
        fallback_strategy=fallback,
        created_at=datetime.utcnow().isoformat() + "Z",
        context_budget=total_tokens * 2,  # 2x buffer
        max_parallel=3 if complexity in ("L", "XL") else 1
    )

    return plan


def validate_plan(plan: ExecutionPlan) -> List[str]:
    """验证执行计划"""
    errors = []

    # 检查步骤数量
    if len(plan.steps) == 0:
        errors.append("Plan has no steps")

    if len(plan.steps) > 10:
        errors.append(f"Plan has too many steps ({len(plan.steps)} > 10)")

    # 检查依赖循环
    visited = set()
    rec_stack = set()

    def has_cycle(step_id: str) -> bool:
        visited.add(step_id)
        rec_stack.add(step_id)

        step = next((s for s in plan.steps if s.step_id == step_id), None)
        if step:
            for dep in step.output_to:
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True

        rec_stack.remove(step_id)
        return False

    for step in plan.steps:
        if step.step_id not in visited:
            if has_cycle(step.step_id):
                errors.append("Plan contains dependency cycle")
                break

    # 检查 context 预算
    if plan.total_estimated_tokens > 50000:
        errors.append(f"Plan exceeds context budget ({plan.total_estimated_tokens} tokens)")

    return errors


def plan_to_mermaid(plan: ExecutionPlan) -> str:
    """将计划转换为 Mermaid 图"""
    lines = ["graph TD"]

    for step in plan.steps:
        node_label = f"{step.step_id}[{step.skill_id}]"
        lines.append(f"    {node_label}")

        for dep in step.input_from:
            lines.append(f"    {dep} --> {step.step_id}")

    return "\n".join(lines)


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Plan Generator - 执行计划生成器")
    parser.add_argument("--analysis", type=str, help="Path to analysis JSON file")
    parser.add_argument("--registry", type=str, help="Path to registry.json")
    parser.add_argument("--task", type=str, help="Task description")
    parser.add_argument("--template", type=str, help="Force specific template")
    parser.add_argument("--validate", action="store_true", help="Validate plan")
    parser.add_argument("--mermaid", action="store_true", help="Output as Mermaid diagram")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")

    args = parser.parse_args()

    if args.list_templates:
        print("Available DAG Templates:")
        for name, template in DAG_TEMPLATES.items():
            print(f"  {name}: {template['description']} ({template['pattern']})")
        return

    # 加载分析结果
    if args.analysis:
        with open(args.analysis, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    else:
        # 使用默认分析
        analysis = {
            "complexity": "M",
            "domains": ["code", "test"],
            "skill_matches": []
        }

    # 加载注册表
    registry = None
    if args.registry:
        with open(args.registry, 'r', encoding='utf-8') as f:
            registry = json.load(f)

    # 生成计划
    plan = generate_plan(
        analysis,
        registry,
        task_description=args.task or ""
    )

    # 验证
    if args.validate:
        errors = validate_plan(plan)
        if errors:
            print("Validation Errors:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        print("Plan validation passed")

    # 输出
    if args.mermaid:
        print(plan_to_mermaid(plan))
    else:
        # 转换为可序列化格式
        output = asdict(plan)
        output["steps"] = [asdict(s) for s in plan.steps]
        print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
