#!/usr/bin/env python3
"""
Decompose Task - 代码任务分解器
将复杂的代码任务分解为可执行的子任务序列。
"""

import json
import sys
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path

@dataclass
class SubTask:
    """子任务"""
    step_id: str
    skill_id: str
    description: str
    input_context: Dict[str, Any]
    depends_on: List[str]
    quality_threshold: float = 0.7


@dataclass
class TaskDecomposition:
    """任务分解结果"""
    original_task: str
    pattern: str
    subtasks: List[SubTask]
    total_steps: int
    estimated_tokens: int


# 任务模式识别关键词
PATTERN_KEYWORDS = {
    "bug_fix": ["修复", "bug", "fix", "error", "错误", "问题", "异常", "crash"],
    "optimization": ["重构", "refactor", "优化", "clean", "整理", "改善"],
    "api_endpoint": ["API", "端点", "endpoint", "接口", "REST", "GraphQL"],
    "feature": ["实现", "功能", "implement", "feature", "新增", "添加", "创建"],
}

# 模式到 Skill 序列的映射
PATTERN_TEMPLATES = {
    "bug_fix": [
        ("debug", "诊断并修复问题"),
        ("test-gen", "生成回归测试"),
        ("code-review", "确认修复质量"),
    ],
    "optimization": [
        ("code-review", "识别优化点"),
        ("refactor", "执行重构"),
        ("test-gen", "确保行为不变"),
        ("code-review", "验证改进"),
    ],
    "api_endpoint": [
        ("code-gen", "生成 API 端点代码"),
        ("test-gen", "生成 API 测试"),
        ("doc-gen", "生成 API 文档"),
    ],
    "feature": [
        ("code-gen", "生成核心代码"),
        ("test-gen", "生成测试"),
        ("code-review", "代码审查"),
    ],
}

# Skill token 估算
SKILL_TOKENS = {
    "code-gen": 2000,
    "test-gen": 1500,
    "code-review": 1000,
    "doc-gen": 1200,
    "refactor": 1800,
    "debug": 1500,
}


def detect_pattern(task_text: str) -> str:
    """检测任务模式"""
    task_lower = task_text.lower()

    # 计算每个模式的匹配分数
    scores = {}
    for pattern, keywords in PATTERN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in task_lower)
        scores[pattern] = score

    # 选择最高分的模式
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)

    return "feature"  # 默认


def extract_context(task_text: str) -> Dict[str, Any]:
    """从任务描述中提取上下文信息"""
    context = {}

    # 提取语言
    languages = {
        "python": ["python", "py", "django", "flask", "fastapi"],
        "javascript": ["javascript", "js", "node", "react", "vue", "typescript", "ts"],
        "java": ["java", "spring"],
        "go": ["golang", "go"],
    }

    task_lower = task_text.lower()
    for lang, keywords in languages.items():
        if any(kw in task_lower for kw in keywords):
            context["language"] = lang
            break

    # 提取文件引用
    file_refs = re.findall(r'[\w/.-]+\.(py|js|ts|java|go|rs)', task_text)
    if file_refs:
        context["mentioned_files"] = list(set(file_refs))

    # 检测是否需要测试
    context["needs_test"] = any(kw in task_lower for kw in ["测试", "test", "验证"])

    # 检测是否需要文档
    context["needs_doc"] = any(kw in task_lower for kw in ["文档", "document", "readme"])

    return context


def customize_template(
    pattern: str,
    context: Dict[str, Any],
    task_text: str
) -> List[tuple]:
    """根据上下文定制模板"""
    template = PATTERN_TEMPLATES.get(pattern, PATTERN_TEMPLATES["feature"]).copy()

    # 如果明确不需要测试，移除 test-gen
    if not context.get("needs_test", True):
        task_lower = task_text.lower()
        if "不需要测试" in task_lower or "skip test" in task_lower:
            template = [(s, d) for s, d in template if s != "test-gen"]

    # 如果需要文档且模板中没有
    if context.get("needs_doc", False):
        if not any(s == "doc-gen" for s, _ in template):
            template.append(("doc-gen", "生成文档"))

    return template


def decompose(task_text: str) -> TaskDecomposition:
    """
    主分解函数

    Args:
        task_text: 任务描述

    Returns:
        TaskDecomposition 对象
    """
    # 检测模式
    pattern = detect_pattern(task_text)

    # 提取上下文
    context = extract_context(task_text)

    # 获取定制化的模板
    template = customize_template(pattern, context, task_text)

    # 构建子任务
    subtasks = []
    prev_step_id = None

    for i, (skill_id, description) in enumerate(template):
        step_id = f"step_{i+1}"

        subtask = SubTask(
            step_id=step_id,
            skill_id=skill_id,
            description=description,
            input_context={
                **context,
                "original_task": task_text[:200],  # 截断
            },
            depends_on=[prev_step_id] if prev_step_id else [],
            quality_threshold=0.8 if skill_id in ("code-gen", "debug") else 0.7
        )

        subtasks.append(subtask)
        prev_step_id = step_id

    # 计算总 token 估算
    total_tokens = sum(SKILL_TOKENS.get(st.skill_id, 1000) for st in subtasks)

    return TaskDecomposition(
        original_task=task_text,
        pattern=pattern,
        subtasks=subtasks,
        total_steps=len(subtasks),
        estimated_tokens=total_tokens
    )


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Decompose Task - 任务分解器")
    parser.add_argument("task", nargs="*", help="Task description")
    parser.add_argument("--pattern", type=str, help="Force specific pattern")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if not args.task:
        task = sys.stdin.read().strip()
    else:
        task = " ".join(args.task)

    if not task:
        print("Usage: decompose_task.py <task_description>")
        sys.exit(1)

    result = decompose(task)

    if args.verbose:
        print(f"Pattern: {result.pattern}")
        print(f"Total Steps: {result.total_steps}")
        print(f"Estimated Tokens: {result.estimated_tokens}")
        print("\nSubtasks:")
        for st in result.subtasks:
            deps = ", ".join(st.depends_on) if st.depends_on else "none"
            print(f"  {st.step_id}: {st.skill_id} - {st.description} (depends: {deps})")
    else:
        # JSON 输出
        output = asdict(result)
        output["subtasks"] = [asdict(st) for st in result.subtasks]
        print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
