#!/usr/bin/env python3
"""
Task Analyzer - 增强版任务分析器
分析任务复杂度和类型，提供上下文感知分析、skill 匹配建议和历史模式学习。
供 Meta-Commander 做路由决策。
"""

import json
import sys
import re
import os
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from pathlib import Path
from datetime import datetime

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


@dataclass
class SkillMatch:
    """Skill 匹配结果"""
    skill_id: str
    confidence: float
    matched_keywords: List[str]
    reason: str


@dataclass
class TaskAnalysis:
    """任务分析结果"""
    complexity: str                    # S / M / L / XL
    domains: List[str]                 # 涉及的领域标签
    estimated_steps: int               # 预估步骤数
    requires_orchestration: bool       # 是否需要编排
    recommended_route: str             # direct / domain-orchestrator / multi-agent / prime-mover
    confidence: float                  # 分析置信度 0-1
    reasoning: str                     # 分析推理过程
    skill_matches: List[SkillMatch] = field(default_factory=list)  # Skill 匹配建议
    context_hints: Dict[str, Any] = field(default_factory=dict)     # 上下文提示
    historical_pattern: Optional[str] = None                         # 历史模式匹配


# 领域关键词映射（增强版）
DOMAIN_KEYWORDS = {
    "code": {
        "keywords": ["code", "function", "class", "implement", "program", "script", "bug", "fix",
                     "refactor", "algorithm", "api", "endpoint", "compile", "runtime", "debug",
                     "代码", "函数", "类", "实现", "编程", "脚本", "修复", "重构", "方法", "模块"],
        "weight": 1.0
    },
    "test": {
        "keywords": ["test", "unit test", "integration", "e2e", "coverage", "assert", "mock",
                     "测试", "单元测试", "集成测试", "覆盖率", "断言", "用例"],
        "weight": 0.9
    },
    "doc": {
        "keywords": ["document", "readme", "comment", "docstring", "markdown", "wiki", "documentation",
                     "文档", "注释", "说明", "README", "API文档"],
        "weight": 0.8
    },
    "data": {
        "keywords": ["database", "sql", "query", "schema", "migration", "etl", "csv", "json",
                     "table", "model", "orm", "数据库", "查询", "迁移", "数据", "表", "字段"],
        "weight": 0.9
    },
    "design": {
        "keywords": ["architecture", "design", "pattern", "diagram", "uml", "system design",
                     "架构", "设计", "模式", "结构", "方案"],
        "weight": 0.85
    },
    "deploy": {
        "keywords": ["deploy", "ci/cd", "docker", "kubernetes", "pipeline", "release", "devops",
                     "部署", "发布", "流水线", "容器", "上线"],
        "weight": 0.8
    },
    "security": {
        "keywords": ["security", "auth", "encryption", "vulnerability", "injection", "xss", "csrf",
                     "authentication", "authorization", "安全", "认证", "加密", "漏洞", "鉴权"],
        "weight": 0.9
    },
    "perf": {
        "keywords": ["performance", "optimize", "benchmark", "profil", "latency", "throughput",
                     "cache", "性能", "优化", "基准测试", "缓存", "响应时间"],
        "weight": 0.85
    },
}

# Skill 关键词直接映射
SKILL_KEYWORDS = {
    "code-gen": {
        "keywords": ["写代码", "生成代码", "实现功能", "写函数", "写类", "create function",
                     "implement", "generate code", "write code", "新增功能"],
        "domain": "code",
        "tier": "core"
    },
    "code-review": {
        "keywords": ["review", "审查", "检查代码", "code review", "代码审查", "review code",
                     "检视", "走查"],
        "domain": "code",
        "tier": "core"
    },
    "test-gen": {
        "keywords": ["写测试", "生成测试", "测试用例", "unit test", "write test", "generate test",
                     "单测", "集成测试"],
        "domain": "test",
        "tier": "core"
    },
    "doc-gen": {
        "keywords": ["写文档", "生成文档", "README", "API文档", "write doc", "generate doc",
                     "document", "注释"],
        "domain": "doc",
        "tier": "core"
    },
    "refactor": {
        "keywords": ["重构", "refactor", "优化代码结构", "清理代码", "改善代码", "restructure"],
        "domain": "code",
        "tier": "core"
    },
    "debug": {
        "keywords": ["调试", "debug", "修bug", "fix bug", "排错", "定位问题", "修复错误"],
        "domain": "code",
        "tier": "core"
    },
    "api-design": {
        "keywords": ["设计API", "API设计", "接口设计", "REST", "GraphQL", "design API"],
        "domain": "design",
        "tier": "extended"
    },
    "db-schema": {
        "keywords": ["数据库设计", "表设计", "schema", "DDL", "ERD", "数据模型", "database design"],
        "domain": "data",
        "tier": "extended"
    },
    "perf-optimize": {
        "keywords": ["性能优化", "optimize", "加速", "performance", "提升性能", "性能调优"],
        "domain": "perf",
        "tier": "extended"
    },
    "security-audit": {
        "keywords": ["安全审计", "security audit", "漏洞检查", "安全检查", "security review"],
        "domain": "security",
        "tier": "extended"
    },
    "creative-code": {
        "keywords": ["创意", "创新", "实验", "探索性", "creative", "experimental", "有趣的"],
        "domain": "code",
        "tier": "experimental"
    },
    "arch-explore": {
        "keywords": ["架构探索", "方案对比", "技术选型", "architecture exploration", "compare solutions"],
        "domain": "design",
        "tier": "experimental"
    },
    "prototype": {
        "keywords": ["原型", "prototype", "MVP", "快速验证", "POC", "demo"],
        "domain": "code",
        "tier": "experimental"
    },
}

# 复杂度信号
COMPLEXITY_SIGNALS = {
    "XL": {
        "keywords": ["from scratch", "entire system", "full stack", "complete rewrite",
                     "design and implement", "build a complete", "从零开始", "完整系统",
                     "全栈", "完全重写", "整个项目", "全新的"],
        "min_domains": 4
    },
    "L": {
        "keywords": ["multiple", "integrate", "coordinate", "across", "both frontend and backend",
                     "end-to-end", "多个", "集成", "协调", "跨", "端到端", "前后端",
                     "全链路", "综合"],
        "min_domains": 3
    },
    "M": {
        "keywords": ["and then", "after that", "step by step", "workflow", "pipeline",
                     "然后", "之后", "步骤", "流程", "先...再", "接着"],
        "min_domains": 2
    },
}

# 历史模式数据库路径
HISTORY_PATH = PROJECT_ROOT / ".tiangong" / "task_history.jsonl"


def detect_domains(task_text: str) -> List[Dict[str, Any]]:
    """检测任务涉及的领域（带权重）"""
    task_lower = task_text.lower()
    detected = []

    for domain, config in DOMAIN_KEYWORDS.items():
        matched_keywords = []
        for kw in config["keywords"]:
            if kw.lower() in task_lower:
                matched_keywords.append(kw)

        if matched_keywords:
            detected.append({
                "domain": domain,
                "weight": config["weight"],
                "matched_keywords": matched_keywords,
                "match_count": len(matched_keywords)
            })

    # 按匹配数量和权重排序
    detected.sort(key=lambda x: (x["match_count"], x["weight"]), reverse=True)

    return detected if detected else [{"domain": "general", "weight": 0.5, "matched_keywords": [], "match_count": 0}]


def match_skills(task_text: str, detected_domains: List[Dict[str, Any]]) -> List[SkillMatch]:
    """匹配最适合的 Skills"""
    task_lower = task_text.lower()
    matches = []

    for skill_id, config in SKILL_KEYWORDS.items():
        matched_keywords = []
        for kw in config["keywords"]:
            if kw.lower() in task_lower:
                matched_keywords.append(kw)

        if matched_keywords:
            # 计算置信度
            base_confidence = len(matched_keywords) / len(config["keywords"])

            # 领域匹配加分
            domain_match = any(d["domain"] == config["domain"] for d in detected_domains)
            if domain_match:
                base_confidence += 0.2

            # 限制在 0-1
            confidence = min(1.0, base_confidence)

            matches.append(SkillMatch(
                skill_id=skill_id,
                confidence=round(confidence, 2),
                matched_keywords=matched_keywords,
                reason=f"Matched {len(matched_keywords)} keywords, domain={config['domain']}"
            ))

    # 按置信度排序
    matches.sort(key=lambda x: x.confidence, reverse=True)

    return matches[:5]  # 返回 top 5


def estimate_complexity(task_text: str, domains: List[Dict[str, Any]]) -> tuple:
    """估计任务复杂度"""
    task_lower = task_text.lower()
    domain_count = len([d for d in domains if d["domain"] != "general"])

    # 检查显式复杂度信号
    for level in ["XL", "L", "M"]:
        config = COMPLEXITY_SIGNALS[level]

        # 关键词匹配
        for signal in config["keywords"]:
            if signal.lower() in task_lower:
                return level, f"Detected complexity signal: '{signal}'"

        # 领域数量匹配
        if domain_count >= config["min_domains"]:
            return level, f"Involves {domain_count} domains (>= {config['min_domains']})"

    # 基于任务长度/句子数推断
    sentences = [s.strip() for s in re.split(r'[.。!！?？\n;；]', task_text) if s.strip()]
    if len(sentences) >= 8:
        return "L", f"Complex description with {len(sentences)} clauses"
    elif len(sentences) >= 4:
        return "M", f"Multi-part description with {len(sentences)} clauses"

    return "S", "Simple single-domain task"


def determine_route(complexity: str, domains: List[Dict[str, Any]], skill_matches: List[SkillMatch]) -> str:
    """确定路由策略"""
    domain_names = [d["domain"] for d in domains if d["domain"] != "general"]

    if complexity == "S":
        # 如果有高置信度的 Skill 匹配，直接路由
        if skill_matches and skill_matches[0].confidence >= 0.7:
            return f"direct:{skill_matches[0].skill_id}"
        return "direct"

    elif complexity == "M":
        if len(domain_names) == 1:
            return f"domain-orchestrator:{domain_names[0]}"
        return "multi-agent"

    elif complexity == "L":
        return "multi-agent"

    else:  # XL
        return "prime-mover"


def estimate_steps(complexity: str, domains: List[Dict[str, Any]], skill_matches: List[SkillMatch]) -> int:
    """估计执行步骤数"""
    base = {"S": 1, "M": 3, "L": 5, "XL": 8}
    domain_count = len([d for d in domains if d["domain"] != "general"])

    steps = base.get(complexity, 3) + max(0, domain_count - 1)

    # 如果匹配到多个 Skill，可能需要更多步骤
    if len(skill_matches) > 2:
        steps += len(skill_matches) - 2

    return min(steps, 10)  # 最多 10 步


def extract_context_hints(task_text: str) -> Dict[str, Any]:
    """提取上下文提示"""
    hints = {}

    # 检测编程语言
    languages = {
        "python": ["python", "py", "django", "flask", "fastapi"],
        "javascript": ["javascript", "js", "node", "react", "vue", "angular", "typescript", "ts"],
        "java": ["java", "spring", "maven", "gradle"],
        "go": ["golang", "go语言"],
        "rust": ["rust"],
        "c++": ["c++", "cpp"],
    }

    task_lower = task_text.lower()
    for lang, keywords in languages.items():
        if any(kw in task_lower for kw in keywords):
            hints["language"] = lang
            break

    # 检测框架
    frameworks = {
        "react": ["react", "jsx"],
        "vue": ["vue", "vuex"],
        "django": ["django"],
        "flask": ["flask"],
        "fastapi": ["fastapi"],
        "spring": ["spring", "springboot"],
        "express": ["express"],
    }

    for fw, keywords in frameworks.items():
        if any(kw in task_lower for kw in keywords):
            hints["framework"] = fw
            break

    # 检测文件类型提及
    file_patterns = re.findall(r'\b[\w-]+\.(py|js|ts|java|go|rs|cpp|h|sql|json|yaml|yml|md)\b', task_text)
    if file_patterns:
        hints["mentioned_files"] = list(set(file_patterns))

    # 检测是否有具体文件路径
    path_patterns = re.findall(r'[/\\]?[\w-]+[/\\][\w/\\.-]+', task_text)
    if path_patterns:
        hints["mentioned_paths"] = path_patterns[:5]

    return hints


def load_historical_patterns() -> List[Dict[str, Any]]:
    """加载历史模式"""
    if not HISTORY_PATH.exists():
        return []

    patterns = []
    try:
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    patterns.append(json.loads(line))
    except Exception:
        pass

    return patterns[-100:]  # 只保留最近 100 条


def find_historical_match(task_text: str, patterns: List[Dict[str, Any]]) -> Optional[str]:
    """查找历史模式匹配"""
    if not patterns:
        return None

    task_words = set(task_text.lower().split())

    best_match = None
    best_score = 0

    for pattern in patterns:
        if pattern.get("success", False):
            pattern_words = set(pattern.get("task_text", "").lower().split())
            # 计算 Jaccard 相似度
            intersection = len(task_words & pattern_words)
            union = len(task_words | pattern_words)
            if union > 0:
                score = intersection / union
                if score > best_score and score > 0.5:  # 相似度阈值
                    best_score = score
                    best_match = pattern.get("route")

    return best_match


def save_analysis_to_history(task_text: str, analysis: 'TaskAnalysis', success: bool = True) -> None:
    """保存分析结果到历史"""
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "task_text": task_text[:500],  # 限制长度
        "complexity": analysis.complexity,
        "domains": analysis.domains,
        "route": analysis.recommended_route,
        "success": success
    }

    with open(HISTORY_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def analyze_task(task_text: str, save_history: bool = False) -> TaskAnalysis:
    """主分析函数"""
    # 检测领域
    domain_info = detect_domains(task_text)
    domains = [d["domain"] for d in domain_info]

    # 匹配 Skills
    skill_matches = match_skills(task_text, domain_info)

    # 估计复杂度
    complexity, reasoning = estimate_complexity(task_text, domain_info)

    # 确定路由
    route = determine_route(complexity, domain_info, skill_matches)

    # 估计步骤
    steps = estimate_steps(complexity, domain_info, skill_matches)

    # 提取上下文提示
    context_hints = extract_context_hints(task_text)

    # 查找历史模式
    historical_patterns = load_historical_patterns()
    historical_match = find_historical_match(task_text, historical_patterns)

    # 计算置信度
    base_confidence = 0.6
    if skill_matches and skill_matches[0].confidence > 0.7:
        base_confidence = 0.85
    elif domains[0] != "general":
        base_confidence = 0.75

    if historical_match:
        base_confidence += 0.1
        if historical_match == route:
            base_confidence += 0.05

    confidence = min(1.0, base_confidence)

    requires_orch = complexity in ("M", "L", "XL")

    analysis = TaskAnalysis(
        complexity=complexity,
        domains=domains,
        estimated_steps=steps,
        requires_orchestration=requires_orch,
        recommended_route=route,
        confidence=round(confidence, 2),
        reasoning=reasoning,
        skill_matches=[asdict(sm) for sm in skill_matches],
        context_hints=context_hints,
        historical_pattern=historical_match
    )

    if save_history:
        save_analysis_to_history(task_text, analysis)

    return analysis


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Task Analyzer - 任务分析器")
    parser.add_argument("task", nargs="*", help="Task description")
    parser.add_argument("--save-history", action="store_true", help="Save to history")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output as JSON only")

    args = parser.parse_args()

    if not args.task:
        # 从 stdin 读取
        task = sys.stdin.read().strip()
    else:
        task = " ".join(args.task)

    if not task:
        print("Usage: task_analyzer.py <task_description>")
        print('  or:  task_analyzer.py "multi word task description"')
        print('  or:  echo "task description" | task_analyzer.py')
        sys.exit(1)

    result = analyze_task(task, save_history=args.save_history)

    if args.json or not args.verbose:
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    else:
        # 人类可读格式
        print(f"Task Analysis")
        print(f"=" * 50)
        print(f"Complexity: {result.complexity}")
        print(f"Domains: {', '.join(result.domains)}")
        print(f"Estimated Steps: {result.estimated_steps}")
        print(f"Requires Orchestration: {result.requires_orchestration}")
        print(f"Recommended Route: {result.recommended_route}")
        print(f"Confidence: {result.confidence}")
        print(f"Reasoning: {result.reasoning}")

        if result.skill_matches:
            print(f"\nSkill Matches:")
            for sm in result.skill_matches[:3]:
                print(f"  - {sm['skill_id']}: {sm['confidence']} ({sm['reason']})")

        if result.context_hints:
            print(f"\nContext Hints: {json.dumps(result.context_hints, ensure_ascii=False)}")

        if result.historical_pattern:
            print(f"\nHistorical Pattern: {result.historical_pattern}")


if __name__ == "__main__":
    main()
