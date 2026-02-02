#!/usr/bin/env python3
"""
Resolve Conflicts - 解决 Skill 输出冲突
检测并解决多个 Skill 输出之间的冲突。
"""

import json
import sys
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from enum import Enum


class ConflictType(Enum):
    FILE = "file"           # 文件冲突
    SEMANTIC = "semantic"   # 语义冲突
    DEPENDENCY = "dependency"  # 依赖冲突
    RESOURCE = "resource"   # 资源冲突


class ResolutionStrategy(Enum):
    MERGE = "merge"         # 合并
    PRIORITY = "priority"   # 优先级
    SEQUENTIAL = "sequential"  # 顺序执行
    MANUAL = "manual"       # 人工处理


@dataclass
class Conflict:
    """冲突描述"""
    conflict_type: ConflictType
    involved_skills: List[str]
    resource: str
    description: str
    severity: str = "medium"  # low, medium, high, critical


@dataclass
class Resolution:
    """解决方案"""
    conflict: Conflict
    strategy: ResolutionStrategy
    details: Dict[str, Any]
    success: bool
    result: Optional[str] = None


def detect_file_conflicts(outputs: Dict[str, Dict[str, Any]]) -> List[Conflict]:
    """检测文件冲突"""
    conflicts = []
    file_map = {}  # file_path -> [skill_ids]

    for skill_id, output in outputs.items():
        for file_path in output.get("output_files", []):
            if file_path not in file_map:
                file_map[file_path] = []
            file_map[file_path].append(skill_id)

    for file_path, skills in file_map.items():
        if len(skills) > 1:
            conflicts.append(Conflict(
                conflict_type=ConflictType.FILE,
                involved_skills=skills,
                resource=file_path,
                description=f"Multiple skills modifying {file_path}",
                severity="high"
            ))

    return conflicts


def detect_semantic_conflicts(outputs: Dict[str, Dict[str, Any]]) -> List[Conflict]:
    """检测语义冲突（简化版）"""
    conflicts = []

    # 提取各输出中定义的实体
    entities = {}  # entity_name -> {skill_id: definition}

    for skill_id, output in outputs.items():
        # 简单提取：查找类名、函数名、变量名等
        content = output.get("content", "") or str(output)

        # 提取类定义
        classes = re.findall(r'class\s+(\w+)', content)
        for cls in classes:
            if cls not in entities:
                entities[cls] = {}
            entities[cls][skill_id] = f"class {cls}"

        # 提取函数定义
        functions = re.findall(r'def\s+(\w+)', content)
        for func in functions:
            if func not in entities:
                entities[func] = {}
            entities[func][skill_id] = f"function {func}"

    # 检查同名实体是否有冲突定义
    for entity, definitions in entities.items():
        if len(definitions) > 1:
            # 检查定义是否一致（简化：仅检查是否存在多个定义）
            conflicts.append(Conflict(
                conflict_type=ConflictType.SEMANTIC,
                involved_skills=list(definitions.keys()),
                resource=entity,
                description=f"Multiple definitions of '{entity}'",
                severity="medium"
            ))

    return conflicts


def detect_dependency_conflicts(dag_nodes: List[Dict[str, Any]]) -> List[Conflict]:
    """检测依赖冲突（循环依赖）"""
    conflicts = []

    # 构建依赖图
    deps = {n["node_id"]: set(n.get("depends_on", [])) for n in dag_nodes}

    # 检测循环
    def has_cycle(node: str, visited: set, rec_stack: set) -> Optional[List[str]]:
        visited.add(node)
        rec_stack.add(node)

        for neighbor in deps.get(node, []):
            if neighbor not in visited:
                cycle = has_cycle(neighbor, visited, rec_stack)
                if cycle:
                    return [node] + cycle
            elif neighbor in rec_stack:
                return [node, neighbor]

        rec_stack.remove(node)
        return None

    visited = set()
    for node in deps:
        if node not in visited:
            cycle = has_cycle(node, visited, set())
            if cycle:
                conflicts.append(Conflict(
                    conflict_type=ConflictType.DEPENDENCY,
                    involved_skills=cycle,
                    resource="dependency_graph",
                    description=f"Circular dependency: {' -> '.join(cycle)}",
                    severity="critical"
                ))
                break

    return conflicts


def detect_resource_conflicts(
    outputs: Dict[str, Dict[str, Any]],
    budget: int = 50000
) -> List[Conflict]:
    """检测资源冲突"""
    conflicts = []

    total_tokens = sum(
        o.get("estimated_tokens", 1000)
        for o in outputs.values()
    )

    if total_tokens > budget:
        conflicts.append(Conflict(
            conflict_type=ConflictType.RESOURCE,
            involved_skills=list(outputs.keys()),
            resource="context_budget",
            description=f"Total tokens ({total_tokens}) exceeds budget ({budget})",
            severity="high"
        ))

    return conflicts


def resolve_file_conflict(conflict: Conflict, outputs: Dict[str, Dict[str, Any]]) -> Resolution:
    """解决文件冲突"""
    # 尝试合并策略
    file_path = conflict.resource
    contents = []

    for skill_id in conflict.involved_skills:
        content = outputs.get(skill_id, {}).get("content", "")
        if content:
            contents.append((skill_id, content))

    if len(contents) == 2:
        # 尝试简单合并
        merged = merge_contents(contents[0][1], contents[1][1])
        if merged:
            return Resolution(
                conflict=conflict,
                strategy=ResolutionStrategy.MERGE,
                details={"merged_from": conflict.involved_skills},
                success=True,
                result=merged
            )

    # 回退到优先级策略
    return Resolution(
        conflict=conflict,
        strategy=ResolutionStrategy.PRIORITY,
        details={"winner": conflict.involved_skills[0]},
        success=True,
        result=f"Using output from {conflict.involved_skills[0]}"
    )


def resolve_semantic_conflict(conflict: Conflict) -> Resolution:
    """解决语义冲突"""
    # 应用命名标准化
    return Resolution(
        conflict=conflict,
        strategy=ResolutionStrategy.PRIORITY,
        details={
            "rule": "Use first definition",
            "winner": conflict.involved_skills[0]
        },
        success=True,
        result=f"Standardized to {conflict.involved_skills[0]}'s definition"
    )


def resolve_dependency_conflict(conflict: Conflict) -> Resolution:
    """解决依赖冲突"""
    # 循环依赖需要打破
    if len(conflict.involved_skills) >= 2:
        # 移除最后一条边
        return Resolution(
            conflict=conflict,
            strategy=ResolutionStrategy.SEQUENTIAL,
            details={
                "removed_edge": f"{conflict.involved_skills[-1]} -> {conflict.involved_skills[0]}"
            },
            success=True,
            result="Broke cycle by removing dependency"
        )

    return Resolution(
        conflict=conflict,
        strategy=ResolutionStrategy.MANUAL,
        details={},
        success=False,
        result="Requires manual intervention"
    )


def resolve_resource_conflict(conflict: Conflict, outputs: Dict[str, Dict[str, Any]]) -> Resolution:
    """解决资源冲突"""
    # 尝试压缩 context
    return Resolution(
        conflict=conflict,
        strategy=ResolutionStrategy.SEQUENTIAL,
        details={
            "action": "Split into phases",
            "phases": 2
        },
        success=True,
        result="Split execution into multiple phases"
    )


def merge_contents(content1: str, content2: str) -> Optional[str]:
    """简单内容合并"""
    # 简化实现：如果没有重叠，直接拼接
    lines1 = set(content1.strip().split('\n'))
    lines2 = set(content2.strip().split('\n'))

    overlap = lines1 & lines2
    if len(overlap) < min(len(lines1), len(lines2)) * 0.3:
        # 重叠较少，可以合并
        return content1 + "\n\n" + content2

    return None  # 需要更复杂的合并


def detect_all_conflicts(
    outputs: Dict[str, Dict[str, Any]],
    dag_nodes: List[Dict[str, Any]] = None
) -> List[Conflict]:
    """检测所有类型的冲突"""
    conflicts = []

    conflicts.extend(detect_file_conflicts(outputs))
    conflicts.extend(detect_semantic_conflicts(outputs))

    if dag_nodes:
        conflicts.extend(detect_dependency_conflicts(dag_nodes))

    conflicts.extend(detect_resource_conflicts(outputs))

    return conflicts


def resolve_conflicts(
    conflicts: List[Conflict],
    outputs: Dict[str, Dict[str, Any]]
) -> List[Resolution]:
    """解决所有冲突"""
    resolutions = []

    for conflict in conflicts:
        if conflict.conflict_type == ConflictType.FILE:
            resolution = resolve_file_conflict(conflict, outputs)
        elif conflict.conflict_type == ConflictType.SEMANTIC:
            resolution = resolve_semantic_conflict(conflict)
        elif conflict.conflict_type == ConflictType.DEPENDENCY:
            resolution = resolve_dependency_conflict(conflict)
        elif conflict.conflict_type == ConflictType.RESOURCE:
            resolution = resolve_resource_conflict(conflict, outputs)
        else:
            resolution = Resolution(
                conflict=conflict,
                strategy=ResolutionStrategy.MANUAL,
                details={},
                success=False,
                result="Unknown conflict type"
            )

        resolutions.append(resolution)

    return resolutions


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Resolve Conflicts")
    parser.add_argument("--outputs", type=str, required=True,
                        help="Path to outputs JSON")
    parser.add_argument("--dag", type=str, help="Path to DAG JSON (optional)")
    parser.add_argument("--detect-only", action="store_true",
                        help="Only detect, don't resolve")

    args = parser.parse_args()

    # 加载输出
    with open(args.outputs, 'r', encoding='utf-8') as f:
        outputs = json.load(f)

    dag_nodes = None
    if args.dag:
        with open(args.dag, 'r', encoding='utf-8') as f:
            dag = json.load(f)
            dag_nodes = dag.get("nodes", [])

    # 检测冲突
    conflicts = detect_all_conflicts(outputs, dag_nodes)

    if args.detect_only:
        result = {
            "conflicts": [
                {
                    "type": c.conflict_type.value,
                    "involved_skills": c.involved_skills,
                    "resource": c.resource,
                    "description": c.description,
                    "severity": c.severity
                }
                for c in conflicts
            ],
            "total": len(conflicts)
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # 解决冲突
    resolutions = resolve_conflicts(conflicts, outputs)

    result = {
        "conflicts_detected": len(conflicts),
        "resolutions": [
            {
                "conflict_type": r.conflict.conflict_type.value,
                "resource": r.conflict.resource,
                "strategy": r.strategy.value,
                "success": r.success,
                "result": r.result,
                "details": r.details
            }
            for r in resolutions
        ],
        "all_resolved": all(r.success for r in resolutions)
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
