#!/usr/bin/env python3
"""
Health Check - 健康检查
检查 Skills 集群的健康状态。
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import load_registry
from utils.skill_validator import validate_skill_structure, validate_skill_md


@dataclass
class HealthReport:
    """健康报告"""
    timestamp: str
    total_skills: int
    active_skills: int
    deprecated_skills: int
    issues: List[Dict[str, Any]]
    warnings: List[str]
    recommendations: List[str]
    overall_health: str  # healthy, warning, critical


def check_skill_health(skill_id: str, skill_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """检查单个 Skill 健康"""
    issues = []

    skill_path = PROJECT_ROOT / skill_info.get("path", skill_id)

    # 1. 检查文件存在
    if not skill_path.exists():
        issues.append({
            "skill_id": skill_id,
            "type": "missing_directory",
            "severity": "critical",
            "message": f"Skill directory not found: {skill_path}"
        })
        return issues

    # 2. 检查 SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        issues.append({
            "skill_id": skill_id,
            "type": "missing_skill_md",
            "severity": "critical",
            "message": "SKILL.md not found"
        })
    else:
        # 验证格式
        result = validate_skill_md(skill_path)
        for error in result.errors:
            issues.append({
                "skill_id": skill_id,
                "type": "skill_md_error",
                "severity": "major",
                "message": error
            })

    # 3. 检查适应度趋势
    fitness = skill_info.get("fitness_score")
    if fitness is not None and fitness < 0.5:
        issues.append({
            "skill_id": skill_id,
            "type": "low_fitness",
            "severity": "warning",
            "message": f"Low fitness score: {fitness}"
        })

    # 4. 检查临时 Skill 过期
    if skill_info.get("status") == "temp":
        ttl = skill_info.get("ttl")
        created_at = skill_info.get("created_at")
        if ttl and created_at:
            # 简化检查
            issues.append({
                "skill_id": skill_id,
                "type": "temp_skill",
                "severity": "info",
                "message": f"Temporary skill with TTL: {ttl}h"
            })

    return issues


def check_registry_consistency(registry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """检查注册表一致性"""
    issues = []

    # 检查孤儿 Skill（在文件系统但不在注册表）
    registered_paths = set()
    for skill_info in registry.get("skills", {}).values():
        registered_paths.add(skill_info.get("path", ""))

    # 扫描 L2-execution
    for category in ["core", "extended", "experimental"]:
        category_path = PROJECT_ROOT / "L2-execution" / category
        if category_path.exists():
            for skill_dir in category_path.iterdir():
                if skill_dir.is_dir():
                    rel_path = f"L2-execution/{category}/{skill_dir.name}/"
                    if rel_path not in registered_paths:
                        issues.append({
                            "skill_id": skill_dir.name,
                            "type": "orphan_skill",
                            "severity": "warning",
                            "message": f"Skill not in registry: {rel_path}"
                        })

    return issues


def run_health_check(skill_id: str = None) -> HealthReport:
    """执行健康检查"""
    registry = load_registry()
    skills = registry.get("skills", {})

    all_issues = []
    warnings = []
    recommendations = []

    if skill_id:
        # 检查单个 Skill
        if skill_id not in skills:
            all_issues.append({
                "skill_id": skill_id,
                "type": "not_found",
                "severity": "critical",
                "message": "Skill not in registry"
            })
        else:
            all_issues.extend(check_skill_health(skill_id, skills[skill_id]))
    else:
        # 检查所有 Skill
        for sid, skill_info in skills.items():
            if skill_info.get("status") != "archived":
                all_issues.extend(check_skill_health(sid, skill_info))

        # 检查注册表一致性
        all_issues.extend(check_registry_consistency(registry))

    # 统计
    total = len(skills)
    active = sum(1 for s in skills.values() if s.get("status") == "active")
    deprecated = sum(1 for s in skills.values() if s.get("status") == "deprecated")

    # 分析问题
    critical_count = sum(1 for i in all_issues if i.get("severity") == "critical")
    warning_count = sum(1 for i in all_issues if i.get("severity") == "warning")

    # 生成建议
    if critical_count > 0:
        recommendations.append("Fix critical issues immediately")
    if warning_count > 3:
        recommendations.append("Review and address accumulated warnings")

    orphans = [i for i in all_issues if i.get("type") == "orphan_skill"]
    if orphans:
        recommendations.append(f"Register {len(orphans)} orphan skill(s)")

    low_fitness = [i for i in all_issues if i.get("type") == "low_fitness"]
    if low_fitness:
        recommendations.append(f"Review {len(low_fitness)} skill(s) with low fitness")

    # 总体健康状态
    if critical_count > 0:
        overall_health = "critical"
    elif warning_count > 5:
        overall_health = "warning"
    else:
        overall_health = "healthy"

    return HealthReport(
        timestamp=datetime.utcnow().isoformat() + "Z",
        total_skills=total,
        active_skills=active,
        deprecated_skills=deprecated,
        issues=all_issues,
        warnings=warnings,
        recommendations=recommendations,
        overall_health=overall_health
    )


def main():
    parser = argparse.ArgumentParser(description="Run health check")
    parser.add_argument("--skill-id", help="Check specific skill")
    parser.add_argument("--all", action="store_true", help="Check all skills")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    report = run_health_check(args.skill_id if not args.all else None)

    if args.json:
        print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
    else:
        print("Health Check Report")
        print("=" * 50)
        print(f"Timestamp: {report.timestamp}")
        print(f"Overall Health: {report.overall_health.upper()}")
        print(f"\nSkills: {report.total_skills} total, {report.active_skills} active, {report.deprecated_skills} deprecated")

        if report.issues:
            print(f"\nIssues ({len(report.issues)}):")
            for issue in report.issues:
                severity = issue.get("severity", "").upper()
                print(f"  [{severity}] {issue.get('skill_id')}: {issue.get('message')}")

        if report.recommendations:
            print(f"\nRecommendations:")
            for rec in report.recommendations:
                print(f"  - {rec}")

        # 退出码
        if report.overall_health == "critical":
            sys.exit(2)
        elif report.overall_health == "warning":
            sys.exit(1)


if __name__ == "__main__":
    main()
