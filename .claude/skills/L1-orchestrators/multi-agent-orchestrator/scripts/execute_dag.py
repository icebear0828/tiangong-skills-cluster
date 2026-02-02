#!/usr/bin/env python3
"""
Execute DAG - 执行 DAG
按照 DAG 定义执行 Skills，管理依赖、并行和状态。
"""

import json
import sys
import time
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional, Set, Callable
from pathlib import Path
from datetime import datetime
from enum import Enum


class NodeStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class NodeExecution:
    """节点执行状态"""
    node_id: str
    skill_id: str
    status: NodeStatus
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retries: int = 0
    quality_score: float = 0.0


@dataclass
class DAGExecution:
    """DAG 执行状态"""
    dag_id: str
    status: str  # running, completed, failed, partial
    nodes: Dict[str, NodeExecution]
    start_time: str
    end_time: Optional[str] = None
    current_parallel_group: int = 0


class DAGExecutor:
    """DAG 执行器"""

    def __init__(self, dag_config: Dict[str, Any], max_parallel: int = 3):
        self.dag_id = dag_config["dag_id"]
        self.nodes = {n["node_id"]: n for n in dag_config["nodes"]}
        self.max_parallel = min(max_parallel, dag_config.get("max_parallel", 3))

        # 初始化执行状态
        self.execution = DAGExecution(
            dag_id=self.dag_id,
            status="running",
            nodes={},
            start_time=datetime.utcnow().isoformat() + "Z"
        )

        for node_id, node in self.nodes.items():
            self.execution.nodes[node_id] = NodeExecution(
                node_id=node_id,
                skill_id=node["skill_id"],
                status=NodeStatus.PENDING
            )

    def get_ready_nodes(self) -> List[str]:
        """获取可以执行的节点（所有依赖已完成）"""
        ready = []

        for node_id, exec_state in self.execution.nodes.items():
            if exec_state.status != NodeStatus.PENDING:
                continue

            node_config = self.nodes[node_id]
            deps = node_config.get("depends_on", [])

            # 检查所有依赖是否完成
            all_deps_done = all(
                self.execution.nodes[dep].status == NodeStatus.COMPLETED
                for dep in deps
            )

            if all_deps_done:
                ready.append(node_id)

        return ready[:self.max_parallel]  # 限制并行数

    def can_continue(self) -> bool:
        """检查是否可以继续执行"""
        # 有可执行的节点
        if self.get_ready_nodes():
            return True

        # 有正在运行的节点
        running = any(
            n.status == NodeStatus.RUNNING
            for n in self.execution.nodes.values()
        )

        return running

    def all_completed(self) -> bool:
        """检查是否全部完成"""
        return all(
            n.status in (NodeStatus.COMPLETED, NodeStatus.SKIPPED, NodeStatus.FAILED)
            for n in self.execution.nodes.values()
        )

    def execute_node(
        self,
        node_id: str,
        skill_executor: Callable[[str, Dict[str, Any]], Dict[str, Any]]
    ) -> bool:
        """
        执行单个节点

        Args:
            node_id: 节点 ID
            skill_executor: Skill 执行函数

        Returns:
            是否成功
        """
        node_config = self.nodes[node_id]
        exec_state = self.execution.nodes[node_id]

        exec_state.status = NodeStatus.RUNNING
        exec_state.start_time = datetime.utcnow().isoformat() + "Z"

        # 收集依赖节点的输出作为输入
        input_context = {}
        for dep_id in node_config.get("depends_on", []):
            dep_output = self.execution.nodes[dep_id].output
            if dep_output:
                input_context[dep_id] = dep_output

        try:
            # 执行 Skill
            result = skill_executor(node_config["skill_id"], input_context)

            exec_state.end_time = datetime.utcnow().isoformat() + "Z"
            exec_state.output = result
            exec_state.quality_score = result.get("quality_score", 0.8)

            # 检查质量阈值
            threshold = node_config.get("quality_threshold", 0.7)
            if exec_state.quality_score >= threshold:
                exec_state.status = NodeStatus.COMPLETED
                return True
            else:
                # 质量不达标，但不算失败
                exec_state.status = NodeStatus.COMPLETED
                return True

        except Exception as e:
            exec_state.end_time = datetime.utcnow().isoformat() + "Z"
            exec_state.error = str(e)
            exec_state.retries += 1

            max_retries = node_config.get("max_retries", 2)
            if exec_state.retries < max_retries:
                exec_state.status = NodeStatus.PENDING  # 重试
                return False
            else:
                exec_state.status = NodeStatus.FAILED
                return False

    def execute(
        self,
        skill_executor: Callable[[str, Dict[str, Any]], Dict[str, Any]]
    ) -> DAGExecution:
        """
        执行整个 DAG

        Args:
            skill_executor: Skill 执行函数

        Returns:
            执行结果
        """
        while self.can_continue():
            ready_nodes = self.get_ready_nodes()

            if not ready_nodes:
                # 等待正在运行的节点
                time.sleep(0.1)
                continue

            # 执行所有就绪节点（模拟并行）
            for node_id in ready_nodes:
                self.execute_node(node_id, skill_executor)

        # 确定最终状态
        self.execution.end_time = datetime.utcnow().isoformat() + "Z"

        completed = sum(
            1 for n in self.execution.nodes.values()
            if n.status == NodeStatus.COMPLETED
        )
        failed = sum(
            1 for n in self.execution.nodes.values()
            if n.status == NodeStatus.FAILED
        )
        total = len(self.execution.nodes)

        if failed == 0 and completed == total:
            self.execution.status = "completed"
        elif completed > 0:
            self.execution.status = "partial"
        else:
            self.execution.status = "failed"

        return self.execution

    def get_execution_summary(self) -> Dict[str, Any]:
        """获取执行摘要"""
        return {
            "dag_id": self.dag_id,
            "status": self.execution.status,
            "start_time": self.execution.start_time,
            "end_time": self.execution.end_time,
            "nodes_summary": {
                "total": len(self.execution.nodes),
                "completed": sum(1 for n in self.execution.nodes.values()
                                if n.status == NodeStatus.COMPLETED),
                "failed": sum(1 for n in self.execution.nodes.values()
                             if n.status == NodeStatus.FAILED),
                "skipped": sum(1 for n in self.execution.nodes.values()
                              if n.status == NodeStatus.SKIPPED),
            },
            "quality_scores": {
                nid: n.quality_score
                for nid, n in self.execution.nodes.items()
                if n.status == NodeStatus.COMPLETED
            }
        }


def mock_skill_executor(skill_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """模拟 Skill 执行器（用于测试）"""
    time.sleep(0.1)  # 模拟执行时间

    return {
        "status": "completed",
        "output_files": [f"output/{skill_id}_result.txt"],
        "quality_score": 0.85,
        "summary": f"Executed {skill_id} successfully"
    }


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Execute DAG")
    parser.add_argument("--dag", type=str, required=True, help="Path to DAG JSON")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (mock execution)")
    parser.add_argument("--output", type=str, help="Output file for results")

    args = parser.parse_args()

    # 加载 DAG
    with open(args.dag, 'r', encoding='utf-8') as f:
        dag_config = json.load(f)

    # 创建执行器
    executor = DAGExecutor(dag_config)

    # 执行
    if args.dry_run:
        result = executor.execute(mock_skill_executor)
    else:
        # 真实执行需要实际的 skill_executor
        print("Real execution not implemented. Use --dry-run for testing.")
        sys.exit(1)

    # 输出结果
    summary = executor.get_execution_summary()
    output_json = json.dumps(summary, indent=2, ensure_ascii=False, default=str)

    if args.output:
        Path(args.output).write_text(output_json, encoding='utf-8')
        print(f"Results written to {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
