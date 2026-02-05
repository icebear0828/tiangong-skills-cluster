#!/usr/bin/env python3
"""
Health Check - 健康检查
检查 Skills 集群的健康状态。
支持同时检查 _architecture/ 和 .claude/skills/ 两层。
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# 使用向上查找定位项目根
_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SCRIPT_DIR
for _ in range(10):
    if (PROJECT_ROOT / "registry.json").exists():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent
else:
    PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent.parent

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
    planned_skills: int
    issues: List[Dict[str, Any]]
    warnings: List[str]
    recommendations: List[str]
    overall_health: str  # healthy, warning, critical


def check_skill_health(skill_id: str, skill_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """检查单个 Skill 健康"""
    issues = []

    # 检查架构目录
    arch_path = skill_info.get("arch_path", "")
    if arch_path:
        full_arch_path = PROJECT_ROOT / arch_path
        if not full_arch_path.exists():
            issues.append({
                "skill_id": skill_id,
                "type": "missing_arch_directory",
                "severity": "warning",
                "message": f"Architecture directory not found: {arch_path}"
            })

    # 检查部署目录（仅对已部署的 skill）
    deploy_path = skill_info.get("deploy_path")
    if deploy_path:
        # deploy_path 是相对于 .claude/skills/ 的
        deploy_root = PROJECT_ROOT.parent  # _architecture 的父目录就是 .claude/skills/
        full_deploy_path = deploy_root / deploy_path
        if not full_deploy_path.exists():
            issues.append({
                "skill_id": skill_id,
                "type": "missing_deploy_directory",
                "severity": "critical",
                "message": f"Deploy directory not found: {deploy_path}"
            })
        else:
            # 验证部署目录中有 SKILL.md
            skill_md = full_deploy_path / "SKILL.md"
            if not skill_md.exists():
                issues.append({
                    "skill_id": skill_id,
                    "type": "missing_deploy_skill_md",
                    "severity": "critical",
                    "message": "SKILL.md not found in deploy directory"
                })
    elif skill_info.get("status") == "active":
        issues.append({
            "skill_id": skill_id,
            "type": "active_not_deployed",
            "severity": "warning",
            "message": "Skill is active but has no deploy_path"
        })

    # 检查适应度趋势
    fitness = skill_info.get("fitness_score")
    if fitness is not None and fitness < 0.5:
        issues.append({
            "skill_id": skill_id,
            "type": "low_fitness",
            "severity": "warning",
            "message": f"Low fitness score: {fitness}"
        })

    # 检查临时 Skill 过期
    if skill_info.get("status") == "temp":
        ttl = skill_info.get("ttl")
        created_at = skill_info.get("created_at")
        if ttl and created_at:
            try:
                created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                elapsed_hours = (now - created).total_seconds() / 3600
                if elapsed_hours > ttl:
                    issues.append({
                        "skill_id": skill_id,
                        "type": "temp_expired",
                        "severity": "major",
                        "message": f"Temporary skill expired: TTL={ttl}h, elapsed={elapsed_hours:.1f}h"
                    })
                else:
                    remaining = ttl - elapsed_hours
                    issues.append({
                        "skill_id": skill_id,
                        "type": "temp_skill",
                        "severity": "info",
                        "message": f"Temporary skill: {remaining:.1f}h remaining of {ttl}h TTL"
                    })
            except (ValueError, TypeError):
                issues.append({
                    "skill_id": skill_id,
                    "type": "temp_invalid_dates",
                    "severity": "warning",
                    "message": f"Cannot parse created_at for TTL check: {created_at}"
                })

    return issues


def check_registry_consistency(registry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """检查注册表一致性"""
    issues = []

    # 检查孤儿 Skill（在文件系统但不在注册表）
    registered_arch_paths = set()
    for skill_info in registry.get("skills", {}).values():
        arch_path = skill_info.get("arch_path", "")
        registered_arch_paths.add(arch_path.rstrip("/"))

    # 扫描 L2-execution
    for category in ["core", "extended", "experimental", "workers"]:
        category_path = PROJECT_ROOT / "L2-execution" / category
        if category_path.exists():
            for skill_dir in category_path.iterdir():
                if skill_dir.is_dir():
                    rel_path = f"L2-execution/{category}/{skill_dir.name}"
                    if rel_path not in registered_arch_paths:
                        issues.append({
                            "skill_id": skill_dir.name,
                            "type": "orphan_skill",
                            "severity": "warning",
                            "message": f"Skill not in registry: {rel_path}/"
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
            if skill_info.get("status") not in ("archived", "planned"):
                all_issues.extend(check_skill_health(sid, skill_info))

        # 检查注册表一致性
        all_issues.extend(check_registry_consistency(registry))

    # 统计
    total = len(skills)
    active = sum(1 for s in skills.values() if s.get("status") == "active")
    deprecated = sum(1 for s in skills.values() if s.get("status") == "deprecated")
    planned = sum(1 for s in skills.values() if s.get("status") == "planned")

    # 分析问题
    critical_count = sum(1 for i in all_issues if i.get("severity") == "critical")
    major_count = sum(1 for i in all_issues if i.get("severity") == "major")
    warning_count = sum(1 for i in all_issues if i.get("severity") == "warning")

    # 生成建议
    if critical_count > 0:
        recommendations.append("Fix critical issues immediately")
    if major_count > 0:
        recommendations.append(f"Address {major_count} major issue(s)")
    if warning_count > 3:
        recommendations.append("Review and address accumulated warnings")

    orphans = [i for i in all_issues if i.get("type") == "orphan_skill"]
    if orphans:
        recommendations.append(f"Register {len(orphans)} orphan skill(s)")

    low_fitness = [i for i in all_issues if i.get("type") == "low_fitness"]
    if low_fitness:
        recommendations.append(f"Review {len(low_fitness)} skill(s) with low fitness")

    expired = [i for i in all_issues if i.get("type") == "temp_expired"]
    if expired:
        recommendations.append(f"Clean up {len(expired)} expired temporary skill(s)")

    # 总体健康状态
    if critical_count > 0:
        overall_health = "critical"
    elif major_count > 0 or warning_count > 5:
        overall_health = "warning"
    else:
        overall_health = "healthy"

    return HealthReport(
        timestamp=datetime.now(timezone.utc).isoformat(),
        total_skills=total,
        active_skills=active,
        deprecated_skills=deprecated,
        planned_skills=planned,
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
        print(f"\nSkills: {report.total_skills} total, {report.active_skills} active, "
              f"{report.deprecated_skills} deprecated, {report.planned_skills} planned")

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
