#!/usr/bin/env python3
"""
Deprecate Skill - 废弃 Skill
将 Skill 标记为废弃状态。
"""

import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import load_registry, save_registry, skill_exists, deprecate_skill


def main():
    parser = argparse.ArgumentParser(description="Deprecate a skill")
    parser.add_argument("--id", required=True, help="Skill ID to deprecate")
    parser.add_argument("--reason", required=True, help="Reason for deprecation")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")

    args = parser.parse_args()

    if not skill_exists(args.id):
        print(f"Error: Skill '{args.id}' not found")
        sys.exit(1)

    if args.dry_run:
        print(f"Dry run - would deprecate skill: {args.id}")
        print(f"  Reason: {args.reason}")
        return

    try:
        deprecate_skill(args.id, args.reason)
        print(f"Successfully deprecated skill: {args.id}")
        print(f"Reason: {args.reason}")
        print("\nNote: The skill will be archived after 30 days")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
