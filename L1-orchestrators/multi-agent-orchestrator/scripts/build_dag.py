#!/usr/bin/env python3
"""
Build DAG - 构建执行 DAG
根据任务分析和 Skill 组合规则构建执行 DAG。
"""

import json
import sys
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional, Set
from pathlib import Path


@dataclass
class DAGNode:
    """DAG 节点"""
    node_id: str
    skill_id: str
    description: str
    depends_on: List[str] = field(default_factory=list)
    parallel_group: Optional[int] = None
    estimated_tokens: int = 1000
    timeout_ms: int = 60000
    max_retries: int = 2
    quality_threshold: float = 0.7


@dataclass
class DAG:
    """执行 DAG"""
    dag_id: str
    pattern: str
    nodes: List[DAGNode]
    entry_nodes: List[str]
    exit_nodes: List[str]
    max_parallel: int = 3
    total_estimated_tokens: int = 0


# Skill 估算 token
SKILL_TOKENS = {
    "code-gen": 2000,
    "test-gen": 1500,
    "code-review": 1000,
    "doc-gen": 1200,
    "refactor": 1800,
    "debug": 1500,
    "api-design": 1000,
    "db-schema": 800,
    "perf-optimize": 1500,
    "security-audit": 1200,
    "creative-code": 2500,
    "arch-explore": 1500,
    "prototype": 2000,
}

# 有效的 Skill 连接
VALID_CONNECTIONS = {
    "arch-explore": ["api-design", "db-schema", "code-gen", "prototype"],
    "api-design": ["code-gen", "doc-gen"],
    "db-schema": ["code-gen"],
    "code-gen": ["test-gen", "code-review", "doc-gen"],
    "test-gen": ["code-review"],
    "code-review": ["refactor", "debug", "doc-gen"],
    "refactor": ["test-gen", "code-review"],
    "debug": ["test-gen", "code-review"],
    "prototype": ["code-gen", "arch-explore", "code-review"],
    "doc-gen": [],
    "perf-optimize": ["test-gen", "code-review"],
    "security-audit": ["refactor", "code-review"],
    "creative-code": ["code-review", "test-gen"],
}


def validate_connection(from_skill: str, to_skill: str) -> bool:
    """验证 Skill 连接是否有效"""
    valid_targets = VALID_CONNECTIONS.get(from_skill, [])
    return to_skill in valid_targets or len(valid_targets) == 0


def topological_sort(nodes: List[DAGNode]) -> List[DAGNode]:
    """拓扑排序"""
    node_map = {n.node_id: n for n in nodes}
    in_degree = {n.node_id: len(n.depends_on) for n in nodes}
    queue = [nid for nid, deg in in_degree.items() if deg == 0]
    sorted_nodes = []

    while queue:
        current = queue.pop(0)
        sorted_nodes.append(node_map[current])

        for node in nodes:
            if current in node.depends_on:
                in_degree[node.node_id] -= 1
                if in_degree[node.node_id] == 0:
                    queue.append(node.node_id)

    if len(sorted_nodes) != len(nodes):
        raise ValueError("DAG contains cycle")

    return sorted_nodes


def detect_cycle(nodes: List[DAGNode]) -> bool:
    """检测是否有环"""
    try:
        topological_sort(nodes)
        return False
    except ValueError:
        return True


def find_entry_nodes(nodes: List[DAGNode]) -> List[str]:
    """找到入口节点（无依赖的节点）"""
    return [n.node_id for n in nodes if not n.depends_on]


def find_exit_nodes(nodes: List[DAGNode]) -> List[str]:
    """找到出口节点（无后继的节点）"""
    all_deps = set()
    for n in nodes:
        all_deps.update(n.depends_on)

    return [n.node_id for n in nodes if n.node_id not in all_deps or not any(
        n.node_id in other.depends_on for other in nodes
    )]


def assign_parallel_groups(nodes: List[DAGNode]) -> None:
    """分配并行组"""
    # 使用拓扑层级作为并行组
    node_map = {n.node_id: n for n in nodes}
    levels = {}

    def get_level(node_id: str) -> int:
        if node_id in levels:
            return levels[node_id]

        node = node_map[node_id]
        if not node.depends_on:
            levels[node_id] = 0
        else:
            levels[node_id] = max(get_level(d) for d in node.depends_on) + 1

        return levels[node_id]

    for node in nodes:
        node.parallel_group = get_level(node.node_id)


def build_dag_from_skills(
    skills: List[str],
    pattern: str = "sequential",
    dag_id: str = None
) -> DAG:
    """
    从 Skill 列表构建 DAG

    Args:
        skills: Skill ID 列表
        pattern: 执行模式 (sequential, parallel, dag)
        dag_id: DAG ID

    Returns:
        DAG 对象
    """
    import uuid
    dag_id = dag_id or f"dag_{uuid.uuid4().hex[:8]}"

    nodes = []

    if pattern == "sequential":
        # 顺序执行
        prev_node_id = None
        for i, skill_id in enumerate(skills):
            node = DAGNode(
                node_id=f"node_{i+1}",
                skill_id=skill_id,
                description=f"Execute {skill_id}",
                depends_on=[prev_node_id] if prev_node_id else [],
                estimated_tokens=SKILL_TOKENS.get(skill_id, 1000)
            )
            nodes.append(node)
            prev_node_id = node.node_id

    elif pattern == "parallel":
        # 并行执行（假设第一个是前置，中间并行，最后汇合）
        if len(skills) <= 2:
            return build_dag_from_skills(skills, "sequential", dag_id)

        # 第一个节点
        entry_node = DAGNode(
            node_id="node_1",
            skill_id=skills[0],
            description=f"Execute {skills[0]}",
            estimated_tokens=SKILL_TOKENS.get(skills[0], 1000)
        )
        nodes.append(entry_node)

        # 中间并行节点
        parallel_node_ids = []
        for i, skill_id in enumerate(skills[1:-1], start=2):
            node = DAGNode(
                node_id=f"node_{i}",
                skill_id=skill_id,
                description=f"Execute {skill_id} (parallel)",
                depends_on=["node_1"],
                parallel_group=1,
                estimated_tokens=SKILL_TOKENS.get(skill_id, 1000)
            )
            nodes.append(node)
            parallel_node_ids.append(node.node_id)

        # 最后汇合节点
        exit_node = DAGNode(
            node_id=f"node_{len(skills)}",
            skill_id=skills[-1],
            description=f"Execute {skills[-1]} (merge)",
            depends_on=parallel_node_ids,
            estimated_tokens=SKILL_TOKENS.get(skills[-1], 1000)
        )
        nodes.append(exit_node)

    else:
        # 默认顺序
        return build_dag_from_skills(skills, "sequential", dag_id)

    # 分配并行组
    assign_parallel_groups(nodes)

    # 计算总 token
    total_tokens = sum(n.estimated_tokens for n in nodes)

    return DAG(
        dag_id=dag_id,
        pattern=pattern,
        nodes=nodes,
        entry_nodes=find_entry_nodes(nodes),
        exit_nodes=find_exit_nodes(nodes),
        total_estimated_tokens=total_tokens
    )


def build_dag_from_config(config: Dict[str, Any]) -> DAG:
    """
    从配置构建 DAG

    Args:
        config: DAG 配置字典

    Returns:
        DAG 对象
    """
    import uuid

    dag_id = config.get("dag_id", f"dag_{uuid.uuid4().hex[:8]}")
    pattern = config.get("pattern", "dag")

    nodes = []
    for node_config in config.get("nodes", []):
        node = DAGNode(
            node_id=node_config["id"],
            skill_id=node_config["skill"],
            description=node_config.get("description", f"Execute {node_config['skill']}"),
            depends_on=node_config.get("depends_on", []),
            parallel_group=node_config.get("parallel_group"),
            estimated_tokens=SKILL_TOKENS.get(node_config["skill"], 1000),
            timeout_ms=node_config.get("timeout_ms", 60000),
            max_retries=node_config.get("max_retries", 2),
            quality_threshold=node_config.get("quality_threshold", 0.7)
        )
        nodes.append(node)

    # 验证无环
    if detect_cycle(nodes):
        raise ValueError("DAG configuration contains cycle")

    # 验证连接有效性
    node_map = {n.node_id: n for n in nodes}
    for node in nodes:
        for dep_id in node.depends_on:
            if dep_id not in node_map:
                raise ValueError(f"Invalid dependency: {dep_id} not found")

            dep_skill = node_map[dep_id].skill_id
            if not validate_connection(dep_skill, node.skill_id):
                print(f"Warning: Unusual connection {dep_skill} -> {node.skill_id}")

    # 分配并行组
    assign_parallel_groups(nodes)

    total_tokens = sum(n.estimated_tokens for n in nodes)

    return DAG(
        dag_id=dag_id,
        pattern=pattern,
        nodes=nodes,
        entry_nodes=find_entry_nodes(nodes),
        exit_nodes=find_exit_nodes(nodes),
        max_parallel=config.get("max_parallel", 3),
        total_estimated_tokens=total_tokens
    )


def dag_to_mermaid(dag: DAG) -> str:
    """将 DAG 转换为 Mermaid 图"""
    lines = ["graph TD"]

    for node in dag.nodes:
        label = f"{node.node_id}[{node.skill_id}]"
        lines.append(f"    {label}")

        for dep in node.depends_on:
            lines.append(f"    {dep} --> {node.node_id}")

    return "\n".join(lines)


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Build DAG")
    parser.add_argument("--skills", type=str, help="Comma-separated skill IDs")
    parser.add_argument("--pattern", type=str, default="sequential",
                        choices=["sequential", "parallel", "dag"])
    parser.add_argument("--config", type=str, help="Path to DAG config JSON")
    parser.add_argument("--mermaid", action="store_true", help="Output as Mermaid")
    parser.add_argument("--validate", action="store_true", help="Validate only")

    args = parser.parse_args()

    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        dag = build_dag_from_config(config)
    elif args.skills:
        skills = [s.strip() for s in args.skills.split(",")]
        dag = build_dag_from_skills(skills, args.pattern)
    else:
        print("Error: Either --skills or --config required")
        sys.exit(1)

    if args.validate:
        print("DAG is valid")
        print(f"  Nodes: {len(dag.nodes)}")
        print(f"  Entry: {dag.entry_nodes}")
        print(f"  Exit: {dag.exit_nodes}")
        print(f"  Estimated tokens: {dag.total_estimated_tokens}")
        return

    if args.mermaid:
        print(dag_to_mermaid(dag))
    else:
        output = asdict(dag)
        output["nodes"] = [asdict(n) for n in dag.nodes]
        print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
