#!/usr/bin/env python3
"""
Skill Validator - Skill 验证工具
验证 Skill 目录结构、SKILL.md 格式、契约符合性等。
"""

import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

# 契约等级要求
CONTRACT_REQUIREMENTS = {
    "strict": {
        "required_files": ["SKILL.md"],
        "required_frontmatter": ["name", "description"],
        "recommended_dirs": ["references", "scripts"],
        "requires_input_schema": True,
        "requires_output_schema": True,
    },
    "standard": {
        "required_files": ["SKILL.md"],
        "required_frontmatter": ["name", "description"],
        "recommended_dirs": ["references"],
        "requires_input_schema": False,
        "requires_output_schema": False,
    },
    "flexible": {
        "required_files": ["SKILL.md"],
        "required_frontmatter": ["name"],
        "recommended_dirs": [],
        "requires_input_schema": False,
        "requires_output_schema": False,
    },
}

# Tier 到契约等级的默认映射
TIER_CONTRACT_MAP = {
    "core": "strict",
    "extended": "standard",
    "experimental": "flexible",
}

@dataclass
class ValidationResult:
    """验证结果"""
    valid: bool
    skill_id: str
    errors: List[str]
    warnings: List[str]
    info: Dict[str, Any]


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """
    解析 SKILL.md 的 frontmatter

    Args:
        content: 文件内容

    Returns:
        (frontmatter 字典, body 内容)
    """
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()

            # 简单的 YAML 解析（支持多行 description）
            current_key = None
            current_value = []

            for line in fm_text.split("\n"):
                # 检查是否是新的 key
                match = re.match(r'^(\w+):\s*(.*)$', line)
                if match:
                    # 保存之前的 key-value
                    if current_key:
                        frontmatter[current_key] = " ".join(current_value).strip()

                    current_key = match.group(1)
                    value = match.group(2).strip()

                    # 处理 YAML 多行字符串标记
                    if value in (">", "|", ">-", "|-"):
                        current_value = []
                    else:
                        current_value = [value]
                elif current_key and line.strip():
                    current_value.append(line.strip())

            # 保存最后一个 key-value
            if current_key:
                frontmatter[current_key] = " ".join(current_value).strip()

    return frontmatter, body


def validate_skill_md(skill_path: Path, contract_level: str = "flexible") -> ValidationResult:
    """
    验证 SKILL.md 文件

    Args:
        skill_path: Skill 目录路径
        contract_level: 契约等级

    Returns:
        ValidationResult
    """
    errors = []
    warnings = []
    info = {}

    skill_id = skill_path.name
    skill_md_path = skill_path / "SKILL.md"

    # 检查 SKILL.md 存在
    if not skill_md_path.exists():
        errors.append(f"Missing SKILL.md in {skill_path}")
        return ValidationResult(False, skill_id, errors, warnings, info)

    # 读取并解析
    try:
        content = skill_md_path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"Cannot read SKILL.md: {e}")
        return ValidationResult(False, skill_id, errors, warnings, info)

    frontmatter, body = parse_frontmatter(content)
    info["frontmatter"] = frontmatter

    # 检查必需的 frontmatter 字段
    requirements = CONTRACT_REQUIREMENTS.get(contract_level, CONTRACT_REQUIREMENTS["flexible"])

    for field in requirements["required_frontmatter"]:
        if field not in frontmatter or not frontmatter[field]:
            errors.append(f"Missing required frontmatter field: {field}")

    # 检查 body 内容
    if len(body) < 100:
        warnings.append("SKILL.md body is very short (< 100 chars)")

    # 提取 skill 名称
    if "name" in frontmatter:
        info["name"] = frontmatter["name"]

    valid = len(errors) == 0
    return ValidationResult(valid, skill_id, errors, warnings, info)


def validate_skill_structure(
    skill_path: Path,
    tier: str = "experimental"
) -> ValidationResult:
    """
    验证 Skill 目录结构

    Args:
        skill_path: Skill 目录路径
        tier: Skill 层级

    Returns:
        ValidationResult
    """
    errors = []
    warnings = []
    info = {"path": str(skill_path), "tier": tier}

    skill_id = skill_path.name
    contract_level = TIER_CONTRACT_MAP.get(tier, "flexible")
    requirements = CONTRACT_REQUIREMENTS.get(contract_level, CONTRACT_REQUIREMENTS["flexible"])

    # 检查目录存在
    if not skill_path.exists():
        errors.append(f"Skill directory does not exist: {skill_path}")
        return ValidationResult(False, skill_id, errors, warnings, info)

    if not skill_path.is_dir():
        errors.append(f"Skill path is not a directory: {skill_path}")
        return ValidationResult(False, skill_id, errors, warnings, info)

    # 检查必需文件
    for required_file in requirements["required_files"]:
        if not (skill_path / required_file).exists():
            errors.append(f"Missing required file: {required_file}")

    # 检查推荐目录
    for recommended_dir in requirements["recommended_dirs"]:
        if not (skill_path / recommended_dir).exists():
            warnings.append(f"Missing recommended directory: {recommended_dir}")

    # 统计目录内容
    info["files"] = [f.name for f in skill_path.iterdir() if f.is_file()]
    info["directories"] = [d.name for d in skill_path.iterdir() if d.is_dir()]

    valid = len(errors) == 0
    return ValidationResult(valid, skill_id, errors, warnings, info)


def validate_contract(
    skill_path: Path,
    contract_level: str
) -> ValidationResult:
    """
    验证 Skill 契约符合性

    Args:
        skill_path: Skill 目录路径
        contract_level: 契约等级

    Returns:
        ValidationResult
    """
    errors = []
    warnings = []
    info = {"contract_level": contract_level}

    skill_id = skill_path.name
    requirements = CONTRACT_REQUIREMENTS.get(contract_level, CONTRACT_REQUIREMENTS["flexible"])

    # 先验证 SKILL.md
    md_result = validate_skill_md(skill_path, contract_level)
    errors.extend(md_result.errors)
    warnings.extend(md_result.warnings)
    info.update(md_result.info)

    # strict 契约需要额外检查
    if contract_level == "strict":
        skill_md_path = skill_path / "SKILL.md"
        if skill_md_path.exists():
            content = skill_md_path.read_text(encoding="utf-8")

            # 检查是否有输入/输出格式描述
            if "输入" not in content and "Input" not in content and "input" not in content:
                warnings.append("Strict contract: consider documenting input format")

            if "输出" not in content and "Output" not in content and "output" not in content:
                warnings.append("Strict contract: consider documenting output format")

            # 检查是否有操作/脚本文档
            scripts_dir = skill_path / "scripts"
            if scripts_dir.exists():
                scripts = list(scripts_dir.glob("*.py"))
                info["scripts_count"] = len(scripts)

                # 检查脚本是否在 SKILL.md 中有文档
                for script in scripts:
                    if script.stem not in content:
                        warnings.append(f"Script '{script.name}' not documented in SKILL.md")

    valid = len(errors) == 0
    return ValidationResult(valid, skill_id, errors, warnings, info)


def check_directory_structure(base_path: Path) -> ValidationResult:
    """
    检查整体目录结构完整性

    Args:
        base_path: 项目根目录

    Returns:
        ValidationResult
    """
    errors = []
    warnings = []
    info = {"base_path": str(base_path)}

    # 预期的目录结构
    expected_dirs = [
        "references",
        "scripts",
        "scripts/utils",
        "L1-orchestrators",
        "L2-execution/core",
        "L2-execution/extended",
        "L2-execution/experimental",
        "infra",
        "genesis",
    ]

    existing = []
    missing = []

    for expected in expected_dirs:
        dir_path = base_path / expected
        if dir_path.exists():
            existing.append(expected)
        else:
            missing.append(expected)
            warnings.append(f"Missing directory: {expected}")

    info["existing_directories"] = existing
    info["missing_directories"] = missing

    # 检查关键文件
    key_files = ["SKILL.md", "registry.json"]
    for key_file in key_files:
        if not (base_path / key_file).exists():
            errors.append(f"Missing key file: {key_file}")

    valid = len(errors) == 0
    return ValidationResult(valid, "structure", errors, warnings, info)


def run_full_validation(base_path: Path, registry_path: Optional[Path] = None) -> Dict[str, ValidationResult]:
    """
    运行完整验证

    Args:
        base_path: 项目根目录
        registry_path: 注册表路径

    Returns:
        所有验证结果的字典
    """
    results = {}

    # 验证目录结构
    results["structure"] = check_directory_structure(base_path)

    # 加载注册表
    if registry_path is None:
        registry_path = base_path / "registry.json"

    if registry_path.exists():
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)

            # 验证每个注册的 Skill
            for skill_id, skill_info in registry.get("skills", {}).items():
                skill_path = base_path / skill_info.get("arch_path", skill_info.get("path", skill_id))
                tier = skill_info.get("tier", "experimental")
                contract_level = skill_info.get("contract_level", "flexible")

                # 综合验证
                struct_result = validate_skill_structure(skill_path, tier)
                contract_result = validate_contract(skill_path, contract_level)

                # 合并结果
                combined_errors = struct_result.errors + contract_result.errors
                combined_warnings = struct_result.warnings + contract_result.warnings
                combined_info = {**struct_result.info, **contract_result.info}

                results[skill_id] = ValidationResult(
                    valid=len(combined_errors) == 0,
                    skill_id=skill_id,
                    errors=combined_errors,
                    warnings=combined_warnings,
                    info=combined_info
                )
        except json.JSONDecodeError as e:
            results["registry"] = ValidationResult(
                False, "registry", [f"Invalid registry.json: {e}"], [], {}
            )
    else:
        results["registry"] = ValidationResult(
            False, "registry", ["registry.json not found"], [], {}
        )

    return results


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Skill Validator")
    parser.add_argument("--check-structure", action="store_true", help="Check directory structure")
    parser.add_argument("--skill", type=str, help="Validate specific skill by path")
    parser.add_argument("--tier", type=str, default="experimental", help="Skill tier")
    parser.add_argument("--contract", type=str, help="Contract level override")
    parser.add_argument("--all", action="store_true", help="Run full validation")
    parser.add_argument("--base-path", type=str, default=".", help="Base path")

    args = parser.parse_args()
    base_path = Path(args.base_path).resolve()

    if args.check_structure:
        result = check_directory_structure(base_path)
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))

    elif args.skill:
        skill_path = Path(args.skill).resolve()
        contract_level = args.contract or TIER_CONTRACT_MAP.get(args.tier, "flexible")

        result = validate_contract(skill_path, contract_level)
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))

    elif args.all:
        results = run_full_validation(base_path)

        all_valid = True
        for name, result in results.items():
            if not result.valid:
                all_valid = False

            status = "✓" if result.valid else "✗"
            print(f"{status} {name}")

            for error in result.errors:
                print(f"  ERROR: {error}")

            for warning in result.warnings:
                print(f"  WARN: {warning}")

        print(f"\nOverall: {'PASS' if all_valid else 'FAIL'}")
        sys.exit(0 if all_valid else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
