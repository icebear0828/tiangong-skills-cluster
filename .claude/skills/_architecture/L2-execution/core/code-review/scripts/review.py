#!/usr/bin/env python3
"""
Code Review - 代码审查主脚本
对代码进行全面审查。
"""

import json
import sys
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class Issue:
    """审查问题"""
    severity: str  # critical, major, minor, suggestion
    category: str  # security, bug, performance, style, maintainability
    line_number: int
    code_snippet: str
    description: str
    suggestion: str


@dataclass
class ReviewSummary:
    """审查摘要"""
    total_issues: int
    critical_count: int
    major_count: int
    minor_count: int
    suggestion_count: int
    quality_score: float


@dataclass
class ReviewResult:
    """审查结果"""
    issues: List[Issue]
    summary: ReviewSummary
    recommendations: List[str]


# 安全检查模式
SECURITY_PATTERNS = {
    "sql_injection": {
        "patterns": [
            r'execute\s*\([^)]*[\'"][^"\']*%s',
            r'f"[^"]*{[^}]*}".*execute',
            r"query\s*=\s*['\"].*\+",
        ],
        "severity": "critical",
        "description": "Potential SQL injection vulnerability",
        "suggestion": "Use parameterized queries"
    },
    "hardcoded_password": {
        "patterns": [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
        ],
        "severity": "critical",
        "description": "Hardcoded credentials detected",
        "suggestion": "Use environment variables or secret management"
    },
    "eval_usage": {
        "patterns": [
            r'\beval\s*\(',
            r'\bexec\s*\(',
        ],
        "severity": "critical",
        "description": "Dangerous eval/exec usage",
        "suggestion": "Avoid eval/exec, use safer alternatives"
    },
}

# 代码质量模式
QUALITY_PATTERNS = {
    "long_function": {
        "check": lambda lines: len(lines) > 50,
        "severity": "minor",
        "category": "maintainability",
        "description": "Function too long (>50 lines)",
        "suggestion": "Break into smaller functions"
    },
    "too_many_params": {
        "pattern": r'def\s+\w+\s*\([^)]{100,}\)',
        "severity": "minor",
        "category": "maintainability",
        "description": "Too many parameters",
        "suggestion": "Consider using a configuration object"
    },
    "bare_except": {
        "pattern": r'except\s*:',
        "severity": "major",
        "category": "bug",
        "description": "Bare except clause",
        "suggestion": "Catch specific exceptions"
    },
    "unused_import": {
        "pattern": r'^import\s+(\w+)',
        "severity": "minor",
        "category": "style",
        "description": "Potentially unused import",
        "suggestion": "Remove if not used"
    },
    "magic_number": {
        "pattern": r'[^0-9]([2-9]\d{2,}|[1-9]\d{3,})[^0-9]',
        "severity": "suggestion",
        "category": "maintainability",
        "description": "Magic number detected",
        "suggestion": "Use named constants"
    },
    "todo_comment": {
        "pattern": r'#\s*(TODO|FIXME|XXX|HACK)',
        "severity": "suggestion",
        "category": "maintainability",
        "description": "TODO/FIXME comment found",
        "suggestion": "Address or create ticket"
    },
}


def check_security(code: str, lines: List[str]) -> List[Issue]:
    """安全检查"""
    issues = []

    for name, config in SECURITY_PATTERNS.items():
        for pattern in config["patterns"]:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(Issue(
                        severity=config["severity"],
                        category="security",
                        line_number=i,
                        code_snippet=line.strip()[:100],
                        description=f"{config['description']} ({name})",
                        suggestion=config["suggestion"]
                    ))

    return issues


def check_quality(code: str, lines: List[str]) -> List[Issue]:
    """代码质量检查"""
    issues = []

    for name, config in QUALITY_PATTERNS.items():
        if "pattern" in config:
            pattern = config["pattern"]
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    issues.append(Issue(
                        severity=config["severity"],
                        category=config["category"],
                        line_number=i,
                        code_snippet=line.strip()[:100],
                        description=config["description"],
                        suggestion=config["suggestion"]
                    ))

    return issues


def check_style(code: str, lines: List[str]) -> List[Issue]:
    """风格检查"""
    issues = []

    for i, line in enumerate(lines, 1):
        # 行长度检查
        if len(line) > 120:
            issues.append(Issue(
                severity="suggestion",
                category="style",
                line_number=i,
                code_snippet=line[:50] + "...",
                description="Line too long (>120 characters)",
                suggestion="Break into multiple lines"
            ))

        # 尾部空白检查
        if line.rstrip() != line.rstrip('\n'):
            issues.append(Issue(
                severity="suggestion",
                category="style",
                line_number=i,
                code_snippet=line.strip()[:50],
                description="Trailing whitespace",
                suggestion="Remove trailing whitespace"
            ))

    return issues


def calculate_quality_score(issues: List[Issue], total_lines: int) -> float:
    """计算质量分数"""
    weights = {
        "critical": 0.3,
        "major": 0.15,
        "minor": 0.05,
        "suggestion": 0.01
    }

    penalty = sum(weights.get(i.severity, 0.01) for i in issues)
    normalized_penalty = penalty / max(total_lines / 100, 1)

    return max(0, min(1, 1.0 - normalized_penalty))


def review_code(
    code: str,
    file_path: Optional[str] = None,
    language: str = "python",
    focus_areas: Optional[List[str]] = None
) -> ReviewResult:
    """
    主审查函数

    Args:
        code: 代码内容
        file_path: 文件路径
        language: 编程语言
        focus_areas: 关注领域

    Returns:
        ReviewResult
    """
    lines = code.split('\n')
    issues = []

    focus = focus_areas or ["all"]

    # 执行各项检查
    if "all" in focus or "security" in focus:
        issues.extend(check_security(code, lines))

    if "all" in focus or "logic" in focus or "performance" in focus:
        issues.extend(check_quality(code, lines))

    if "all" in focus or "style" in focus:
        issues.extend(check_style(code, lines))

    # 统计
    critical_count = sum(1 for i in issues if i.severity == "critical")
    major_count = sum(1 for i in issues if i.severity == "major")
    minor_count = sum(1 for i in issues if i.severity == "minor")
    suggestion_count = sum(1 for i in issues if i.severity == "suggestion")

    quality_score = calculate_quality_score(issues, len(lines))

    summary = ReviewSummary(
        total_issues=len(issues),
        critical_count=critical_count,
        major_count=major_count,
        minor_count=minor_count,
        suggestion_count=suggestion_count,
        quality_score=round(quality_score, 2)
    )

    # 生成建议
    recommendations = []
    if critical_count > 0:
        recommendations.append("Address all critical security issues immediately")
    if major_count > 2:
        recommendations.append("Consider refactoring to address major issues")
    if quality_score < 0.7:
        recommendations.append("Code quality below acceptable threshold")
    if not recommendations:
        recommendations.append("Code looks good overall")

    return ReviewResult(
        issues=issues,
        summary=summary,
        recommendations=recommendations
    )


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Code Review")
    parser.add_argument("--file", "-f", type=str, help="File to review")
    parser.add_argument("--code", "-c", type=str, help="Code string to review")
    parser.add_argument("--language", "-l", type=str, default="python")
    parser.add_argument("--focus", type=str, help="Comma-separated focus areas")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.file:
        code = Path(args.file).read_text(encoding='utf-8')
    elif args.code:
        code = args.code
    else:
        code = sys.stdin.read()

    focus_areas = args.focus.split(',') if args.focus else None

    result = review_code(
        code=code,
        file_path=args.file,
        language=args.language,
        focus_areas=focus_areas
    )

    if args.json:
        output = {
            "issues": [asdict(i) for i in result.issues],
            "summary": asdict(result.summary),
            "recommendations": result.recommendations
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("Code Review Report")
        print("=" * 50)
        print(f"\nSummary:")
        print(f"  Total Issues: {result.summary.total_issues}")
        print(f"  Critical: {result.summary.critical_count}")
        print(f"  Major: {result.summary.major_count}")
        print(f"  Minor: {result.summary.minor_count}")
        print(f"  Suggestions: {result.summary.suggestion_count}")
        print(f"  Quality Score: {result.summary.quality_score}")

        if result.issues:
            print(f"\nIssues:")
            for issue in result.issues:
                print(f"  [{issue.severity.upper()}] Line {issue.line_number}: {issue.description}")
                print(f"    Suggestion: {issue.suggestion}")

        print(f"\nRecommendations:")
        for rec in result.recommendations:
            print(f"  - {rec}")


if __name__ == "__main__":
    main()
