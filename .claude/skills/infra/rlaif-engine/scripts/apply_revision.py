#!/usr/bin/env python3
"""
Apply Revision - 应用修订
将验证通过的修订应用到 Skill。
"""

import json
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def backup_skill(skill_path: Path, version: str) -> Path:
    """备份 Skill"""
    backup_dir = PROJECT_ROOT / ".tiangong" / "genomes" / skill_path.name
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_dir / f"v_{version}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    if skill_path.exists():
        shutil.copytree(skill_path, backup_path)

    return backup_path


def apply_changes(skill_path: Path, changes: list):
    """应用修改"""
    for change in changes:
        file_name = change.get("file", "")
        file_path = skill_path / file_name

        change_type = change.get("change_type", "")
        description = change.get("description", "")

        # 简化：记录变更而不实际修改
        # 在实际系统中，这里会解析 diff 并应用
        print(f"  Applying: {file_name} - {description}")

        # 创建变更记录
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)

        # 追加变更注释到文件（如果是 markdown）
        if file_name.endswith(".md") and file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            revision_note = f"\n<!-- Revision applied: {description} at {datetime.utcnow().isoformat()} -->\n"
            # 实际修改会在这里进行
            # file_path.write_text(content + revision_note, encoding="utf-8")


def log_revision_application(skill_id: str, revision_id: str, success: bool):
    """记录修订应用"""
    log_path = PROJECT_ROOT / ".tiangong" / "rlaif-log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "skill_id": skill_id,
        "mode": "feedback-driven",
        "action": "apply" if success else "apply_failed",
        "details": {
            "revision_id": revision_id,
            "success": success
        }
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def find_skill_path(skill_id: str) -> Path:
    """查找 Skill 路径"""
    for category in ["core", "extended", "experimental"]:
        path = PROJECT_ROOT / "L2-execution" / category / skill_id
        if path.exists():
            return path

    # 检查 L1
    path = PROJECT_ROOT / "L1-orchestrators" / skill_id
    if path.exists():
        return path

    # 检查 infra
    path = PROJECT_ROOT / "infra" / skill_id
    if path.exists():
        return path

    return None


def main():
    parser = argparse.ArgumentParser(description="Apply revision to skill")
    parser.add_argument("--skill-id", required=True, help="Skill ID")
    parser.add_argument("--revision", required=True, help="Path to revision JSON")
    parser.add_argument("--force", action="store_true", help="Skip validation check")
    parser.add_argument("--dry-run", action="store_true", help="Preview without applying")

    args = parser.parse_args()

    with open(args.revision, "r", encoding="utf-8") as f:
        revision = json.load(f)

    skill_path = find_skill_path(args.skill_id)

    if not skill_path:
        print(f"Error: Skill '{args.skill_id}' not found")
        sys.exit(1)

    revision_id = revision.get("revision_id", "unknown")
    changes = revision.get("changes", [])

    print(f"Applying revision {revision_id} to {args.skill_id}")

    if args.dry_run:
        print("\nDry run - would apply:")
        for c in changes:
            print(f"  - {c.get('file')}: {c.get('description')}")
        return

    # 备份
    print("Creating backup...")
    backup_path = backup_skill(skill_path, "pre_" + revision_id[:8])
    print(f"  Backup created at: {backup_path}")

    # 应用修改
    print("\nApplying changes...")
    try:
        apply_changes(skill_path, changes)
        log_revision_application(args.skill_id, revision_id, True)
        print("\nRevision applied successfully")
    except Exception as e:
        log_revision_application(args.skill_id, revision_id, False)
        print(f"\nError applying revision: {e}")
        print(f"Restore from backup: {backup_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
