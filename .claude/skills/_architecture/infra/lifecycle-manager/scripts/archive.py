#!/usr/bin/env python3
"""
Archive Skill - 归档 Skill
将废弃超过 30 天的 Skill 归档。
"""

import json
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils.registry_ops import load_registry, save_registry, get_skill, update_skill


def find_skill_path(skill_id: str) -> Path:
    """查找 Skill 路径"""
    for category in ["core", "extended", "experimental"]:
        path = PROJECT_ROOT / "L2-execution" / category / skill_id
        if path.exists():
            return path

    path = PROJECT_ROOT / "L1-orchestrators" / skill_id
    if path.exists():
        return path

    return None


def archive_skill(skill_id: str, dry_run: bool = False) -> bool:
    """归档 Skill"""
    skill = get_skill(skill_id)
    if not skill:
        print(f"Skill '{skill_id}' not found")
        return False

    if skill.get("status") != "deprecated":
        print(f"Skill '{skill_id}' is not deprecated")
        return False

    # 检查废弃时间
    deprecated_at = skill.get("deprecated_at")
    if deprecated_at:
        deprecated_date = datetime.fromisoformat(deprecated_at.replace("Z", "+00:00"))
        days_deprecated = (datetime.now(deprecated_date.tzinfo) - deprecated_date).days
        if days_deprecated < 30:
            print(f"Skill '{skill_id}' deprecated only {days_deprecated} days ago (need 30)")
            return False

    if dry_run:
        print(f"Would archive skill: {skill_id}")
        return True

    # 移动到归档目录
    skill_path = find_skill_path(skill_id)
    if skill_path:
        archive_dir = PROJECT_ROOT / ".tiangong" / "archived" / skill_id
        archive_dir.parent.mkdir(parents=True, exist_ok=True)

        if skill_path.exists():
            shutil.move(str(skill_path), str(archive_dir))

    # 更新注册表
    update_skill(skill_id, {"status": "archived"})

    return True


def auto_archive():
    """自动归档所有符合条件的 Skill"""
    registry = load_registry()
    archived = []

    for skill_id, skill in registry.get("skills", {}).items():
        if skill.get("status") == "deprecated":
            deprecated_at = skill.get("deprecated_at")
            if deprecated_at:
                try:
                    deprecated_date = datetime.fromisoformat(deprecated_at.replace("Z", "+00:00"))
                    days = (datetime.now(deprecated_date.tzinfo) - deprecated_date).days
                    if days >= 30:
                        if archive_skill(skill_id):
                            archived.append(skill_id)
                except:
                    pass

    return archived


def main():
    parser = argparse.ArgumentParser(description="Archive deprecated skills")
    parser.add_argument("--skill-id", help="Specific skill ID to archive")
    parser.add_argument("--auto", action="store_true", help="Auto-archive all eligible skills")
    parser.add_argument("--dry-run", action="store_true", help="Preview without archiving")
    parser.add_argument("--force", action="store_true", help="Archive even if < 30 days")

    args = parser.parse_args()

    if args.auto:
        archived = auto_archive()
        if archived:
            print(f"Archived {len(archived)} skill(s): {', '.join(archived)}")
        else:
            print("No skills eligible for archiving")
        return

    if not args.skill_id:
        print("Error: --skill-id required (or use --auto)")
        sys.exit(1)

    success = archive_skill(args.skill_id, args.dry_run)

    if success:
        if not args.dry_run:
            print(f"Successfully archived skill: {args.skill_id}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
