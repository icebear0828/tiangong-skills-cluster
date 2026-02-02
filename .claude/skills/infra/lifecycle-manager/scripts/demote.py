#!/usr/bin/env python3
"""
Demote Skill - 降级 Skill
将 Skill 降级到更低层级。
"""

import json
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import get_skill, update_skill


def move_skill_directory(skill_id: str, from_tier: str, to_tier: str) -> bool:
    """移动 Skill 目录"""
    from_path = PROJECT_ROOT / "L2-execution" / from_tier / skill_id
    to_path = PROJECT_ROOT / "L2-execution" / to_tier / skill_id

    if not from_path.exists():
        return False

    to_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(from_path), str(to_path))

    return True


def log_demotion(skill_id: str, from_tier: str, to_tier: str, reason: str):
    """记录降级"""
    log_path = PROJECT_ROOT / ".tiangong" / "rlaif-log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "skill_id": skill_id,
        "mode": "lifecycle",
        "action": "demote",
        "details": {
            "from_tier": from_tier,
            "to_tier": to_tier,
            "reason": reason
        }
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Demote skill to lower tier")
    parser.add_argument("--skill-id", required=True, help="Skill ID")
    parser.add_argument("--reason", required=True, help="Reason for demotion")
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
    if current_index <= 0:
        print(f"Skill '{args.skill_id}' is already at lowest tier (experimental)")
        sys.exit(0)

    target_tier = tier_order[current_index - 1]

    print(f"Demoting {args.skill_id}: {current_tier} -> {target_tier}")
    print(f"Reason: {args.reason}")

    if args.dry_run:
        print(f"Dry run - would demote {args.skill_id} to {target_tier}")
        return

    # 执行降级
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

    # 记录
    log_demotion(args.skill_id, current_tier, target_tier, args.reason)

    print(f"Successfully demoted {args.skill_id} to {target_tier}")


if __name__ == "__main__":
    main()
