#!/usr/bin/env python3
"""
Register Skill - 注册新 Skill
将新 Skill 添加到注册表。
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

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

from utils.registry_ops import (
    load_registry, save_registry, skill_exists, register_skill
)
from utils.skill_validator import validate_skill_structure, validate_skill_md


def validate_before_register(skill_path: Path, tier: str) -> tuple:
    """注册前验证"""
    errors = []
    warnings = []

    # 检查目录存在
    if not skill_path.exists():
        errors.append(f"Skill directory not found: {skill_path}")
        return errors, warnings

    # 验证结构
    struct_result = validate_skill_structure(skill_path, tier)
    errors.extend(struct_result.errors)
    warnings.extend(struct_result.warnings)

    # 验证 SKILL.md
    md_result = validate_skill_md(skill_path)
    errors.extend(md_result.errors)
    warnings.extend(md_result.warnings)

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Register a new skill")
    parser.add_argument("--id", required=True, help="Skill ID")
    parser.add_argument("--arch-path", required=True, help="Relative path to skill architecture directory")
    parser.add_argument("--deploy-path", help="Relative path in .claude/skills/ (e.g. 'my-skill/')")
    parser.add_argument("--tier", required=True, choices=["core", "extended", "experimental"])
    parser.add_argument("--domains", required=True, help="Comma-separated domains")
    parser.add_argument("--ttl", type=int, help="TTL in hours for temp skills")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    parser.add_argument("--force", action="store_true", help="Skip validation")

    args = parser.parse_args()

    skill_id = args.id
    skill_path = PROJECT_ROOT / args.arch_path
    domains = [d.strip() for d in args.domains.split(",")]

    # 契约等级映射
    contract_map = {
        "core": "strict",
        "extended": "standard",
        "experimental": "flexible"
    }
    contract_level = contract_map[args.tier]

    # 检查是否已存在
    if skill_exists(skill_id):
        print(f"Error: Skill '{skill_id}' already exists")
        sys.exit(1)

    # 验证
    if not args.force:
        errors, warnings = validate_before_register(skill_path, args.tier)

        for w in warnings:
            print(f"Warning: {w}")

        if errors:
            print("Validation errors:")
            for e in errors:
                print(f"  - {e}")
            print("\nUse --force to skip validation")
            sys.exit(1)

    # 从 SKILL.md 提取名称
    skill_md_path = skill_path / "SKILL.md"
    name = skill_id  # 默认

    if skill_md_path.exists():
        content = skill_md_path.read_text(encoding='utf-8')
        if content.startswith("---"):
            # 简单提取 name
            import re
            match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
            if match:
                name = match.group(1).strip()

    if args.dry_run:
        print("Dry run - would register:")
        print(f"  ID: {skill_id}")
        print(f"  Name: {name}")
        print(f"  Arch Path: {args.arch_path}")
        print(f"  Deploy Path: {args.deploy_path or '(not deployed)'}")
        print(f"  Tier: {args.tier}")
        print(f"  Contract: {contract_level}")
        print(f"  Domains: {domains}")
        if args.ttl:
            print(f"  TTL: {args.ttl} hours")
        return

    # 注册
    try:
        entry = register_skill(
            skill_id=skill_id,
            name=name,
            arch_path=args.arch_path,
            tier=args.tier,
            domains=domains,
            deploy_path=args.deploy_path,
            contract_level=contract_level,
            ttl=args.ttl
        )

        print(f"Successfully registered skill: {skill_id}")
        print(json.dumps(entry, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
