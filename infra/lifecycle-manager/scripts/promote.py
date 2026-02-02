#!/usr/bin/env python3
"""
Promote Skill - 晋升 Skill
将 Skill 晋升到更高层级。
"""

import json
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import load_registry, save_registry, get_skill, update_skill


# 晋升条件
PROMOTION_REQUIREMENTS = {
    "experimental_to_extended": {
        "min_fitness": 0.70,
        "min_calls": 20,
        "no_consecutive_failures": True
    },
    "extended_to_core": {
        "min_fitness": 0.90,
        "min_calls": 50,
        "contract_validation": True,
        "human_confirmation": True
    }
}


def check_promotion_eligibility(skill_id: str, current_tier: str, target_tier: str) -> tuple:
    """检查晋升资格"""
    promotion_key = f"{current_tier}_to_{target_tier}"
    requirements = PROMOTION_REQUIREMENTS.get(promotion_key)

    if not requirements:
        return False, [f"Invalid promotion path: {current_tier} -> {target_tier}"]

    skill = get_skill(skill_id)
    if not skill:
        return False, ["Skill not found"]

    issues = []

    # 检查适应度
    fitness = skill.get("fitness_score") or 0
    if fitness < requirements.get("min_fitness", 0):
        issues.append(f"Fitness {fitness} < required {requirements['min_fitness']}")

    # 这里简化：实际应检查调用次数和失败记录
    # issues.append("Not enough calls") if calls < min_calls

    return len(issues) == 0, issues


def move_skill_directory(skill_id: str, from_tier: str, to_tier: str) -> bool:
    """移动 Skill 目录"""
    from_path = PROJECT_ROOT / "L2-execution" / from_tier / skill_id
    to_path = PROJECT_ROOT / "L2-execution" / to_tier / skill_id

    if not from_path.exists():
        return False

    to_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(from_path), str(to_path))

    return True


def main():
    parser = argparse.ArgumentParser(description="Promote skill to higher tier")
    parser.add_argument("--skill-id", required=True, help="Skill ID")
    parser.add_argument("--force", action="store_true", help="Skip eligibility check")
    parser.add_argument("--confirm", action="store_true", help="Human confirmation for core promotion")
    parser.add_argument("--dry-run", action="store_true", help="Preview without applying")

    args = parser.parse_args()

    skill = get_skill(args.skill_id)
    if not skill:
        print(f"Error: Skill '{args.skill_id}' not found")
        sys.exit(1)

    current_tier = skill.get("tier")
    tier_order = ["experimental", "extended", "core"]

    if current_tier not in tier_order:
        print(f"Error: Unknown tier '{current_tier}'")
        sys.exit(1)

    current_index = tier_order.index(current_tier)
    if current_index >= len(tier_order) - 1:
        print(f"Skill '{args.skill_id}' is already at highest tier (core)")
        sys.exit(0)

    target_tier = tier_order[current_index + 1]

    print(f"Promoting {args.skill_id}: {current_tier} -> {target_tier}")

    # 检查资格
    if not args.force:
        eligible, issues = check_promotion_eligibility(args.skill_id, current_tier, target_tier)

        if not eligible:
            print("Promotion blocked:")
            for i in issues:
                print(f"  - {i}")
            print("\nUse --force to override")
            sys.exit(1)

    # Core 晋升需要人工确认
    if target_tier == "core" and not args.confirm and not args.force:
        print("Core promotion requires human confirmation")
        print("Use --confirm to approve")
        sys.exit(1)

    if args.dry_run:
        print(f"Dry run - would promote {args.skill_id} to {target_tier}")
        return

    # 执行晋升
    contract_map = {
        "experimental": "flexible",
        "extended": "standard",
        "core": "strict"
    }

    # 更新注册表
    update_skill(args.skill_id, {
        "tier": target_tier,
        "contract_level": contract_map[target_tier],
        "path": f"L2-execution/{target_tier}/{args.skill_id}/"
    })

    # 移动目录
    move_skill_directory(args.skill_id, current_tier, target_tier)

    print(f"Successfully promoted {args.skill_id} to {target_tier}")


if __name__ == "__main__":
    main()
