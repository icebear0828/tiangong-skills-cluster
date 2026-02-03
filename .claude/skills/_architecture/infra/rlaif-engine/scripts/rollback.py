#!/usr/bin/env python3
"""
Rollback - 回滚修订
将 Skill 回滚到之前的版本。
"""

import json
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def list_versions(skill_id: str) -> list:
    """列出可用版本"""
    backup_dir = PROJECT_ROOT / ".tiangong" / "genomes" / skill_id

    if not backup_dir.exists():
        return []

    versions = []
    for item in sorted(backup_dir.iterdir(), reverse=True):
        if item.is_dir() and item.name.startswith("v_"):
            versions.append({
                "name": item.name,
                "path": str(item),
                "created": item.stat().st_mtime
            })

    return versions


def find_skill_path(skill_id: str) -> Path:
    """查找 Skill 当前路径"""
    for category in ["core", "extended", "experimental"]:
        path = PROJECT_ROOT / "L2-execution" / category / skill_id
        if path.exists():
            return path

    path = PROJECT_ROOT / "L1-orchestrators" / skill_id
    if path.exists():
        return path

    path = PROJECT_ROOT / "infra" / skill_id
    if path.exists():
        return path

    return None


def rollback_to_version(skill_id: str, version_name: str, dry_run: bool = False) -> bool:
    """回滚到指定版本"""
    backup_dir = PROJECT_ROOT / ".tiangong" / "genomes" / skill_id
    version_path = backup_dir / version_name

    if not version_path.exists():
        print(f"Error: Version '{version_name}' not found")
        return False

    current_path = find_skill_path(skill_id)

    if not current_path:
        print(f"Error: Current skill path not found for '{skill_id}'")
        return False

    if dry_run:
        print(f"Would rollback {skill_id} to {version_name}")
        print(f"  From: {current_path}")
        print(f"  To: {version_path}")
        return True

    # 创建当前版本的备份
    pre_rollback_backup = backup_dir / f"v_pre_rollback_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    shutil.copytree(current_path, pre_rollback_backup)
    print(f"Current version backed up to: {pre_rollback_backup}")

    # 执行回滚
    shutil.rmtree(current_path)
    shutil.copytree(version_path, current_path)

    # 记录
    log_path = PROJECT_ROOT / ".tiangong" / "rlaif-log.jsonl"
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "skill_id": skill_id,
        "mode": "feedback-driven",
        "action": "rollback",
        "details": {
            "to_version": version_name,
            "pre_rollback_backup": str(pre_rollback_backup)
        }
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return True


def main():
    parser = argparse.ArgumentParser(description="Rollback skill to previous version")
    parser.add_argument("--skill-id", required=True, help="Skill ID")
    parser.add_argument("--to-version", help="Version name to rollback to")
    parser.add_argument("--list", action="store_true", help="List available versions")
    parser.add_argument("--dry-run", action="store_true", help="Preview without applying")

    args = parser.parse_args()

    if args.list:
        versions = list_versions(args.skill_id)
        if not versions:
            print(f"No backup versions found for {args.skill_id}")
        else:
            print(f"Available versions for {args.skill_id}:")
            for v in versions:
                print(f"  - {v['name']}")
        return

    if not args.to_version:
        # 默认回滚到最近版本
        versions = list_versions(args.skill_id)
        if not versions:
            print(f"No backup versions available for {args.skill_id}")
            sys.exit(1)
        args.to_version = versions[0]["name"]
        print(f"Rolling back to most recent version: {args.to_version}")

    success = rollback_to_version(args.skill_id, args.to_version, args.dry_run)

    if success:
        print(f"Successfully rolled back {args.skill_id} to {args.to_version}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
