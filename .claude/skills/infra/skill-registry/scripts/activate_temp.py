#!/usr/bin/env python3
"""
Activate Temp Skill - 激活临时 Skill
创建有生存时间限制的临时 Skill。
"""

import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import register_skill, skill_exists


def main():
    parser = argparse.ArgumentParser(description="Activate a temporary skill")
    parser.add_argument("--id", required=True, help="Skill ID")
    parser.add_argument("--path", required=True, help="Relative path to skill")
    parser.add_argument("--ttl", required=True, type=int, help="Time to live in hours")
    parser.add_argument("--domains", required=True, help="Comma-separated domains")
    parser.add_argument("--promote", action="store_true", help="Promote existing temp skill to permanent")

    args = parser.parse_args()

    if args.promote:
        # 将临时 Skill 升级为永久
        from utils.registry_ops import update_skill, get_skill

        if not skill_exists(args.id):
            print(f"Error: Skill '{args.id}' not found")
            sys.exit(1)

        skill = get_skill(args.id)
        if skill.get("status") != "temp":
            print(f"Error: Skill '{args.id}' is not a temporary skill")
            sys.exit(1)

        update_skill(args.id, {"status": "active", "ttl": None})
        print(f"Successfully promoted temp skill '{args.id}' to permanent")
        return

    if skill_exists(args.id):
        print(f"Error: Skill '{args.id}' already exists")
        sys.exit(1)

    domains = [d.strip() for d in args.domains.split(",")]

    try:
        entry = register_skill(
            skill_id=args.id,
            name=args.id,
            path=args.path,
            tier="experimental",
            domains=domains,
            contract_level="flexible",
            ttl=args.ttl
        )

        print(f"Successfully activated temporary skill: {args.id}")
        print(f"TTL: {args.ttl} hours")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
