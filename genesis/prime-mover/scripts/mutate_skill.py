#!/usr/bin/env python3
"""
Prime Mover - Mutate Skill Script
Apply mutations/modifications to existing skills to create improved variants.
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "utils"))
from registry_ops import RegistryOperations


class SkillMutator:
    """Apply mutations to skills to create improved variants."""

    MUTATION_TYPES = {
        "enhance": "Add new capabilities to existing skill",
        "optimize": "Optimize performance or efficiency",
        "specialize": "Create specialized version for specific domain",
        "generalize": "Create more general version",
        "refactor": "Restructure without changing behavior",
        "extend": "Extend with additional features",
        "simplify": "Simplify by removing complexity"
    }

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.registry_ops = RegistryOperations(str(self.base_path / "registry.json"))

    def mutate(
        self,
        source_skill_id: str,
        new_skill_id: str,
        mutation_type: str,
        mutation_spec: Dict[str, Any] = None,
        new_name: str = None
    ) -> Dict[str, Any]:
        """
        Create a mutated version of an existing skill.

        Args:
            source_skill_id: ID of the skill to mutate
            new_skill_id: ID for the new mutated skill
            mutation_type: Type of mutation to apply
            mutation_spec: Specification for the mutation
            new_name: Optional new name for the mutated skill

        Returns:
            Dictionary with mutation results
        """
        if mutation_type not in self.MUTATION_TYPES:
            return {
                "success": False,
                "error": f"Unknown mutation type: {mutation_type}. Valid types: {list(self.MUTATION_TYPES.keys())}"
            }

        # Get source skill info
        registry = self.registry_ops.load_registry()
        if source_skill_id not in registry.get("skills", {}):
            return {"success": False, "error": f"Source skill not found: {source_skill_id}"}

        source_skill = registry["skills"][source_skill_id]
        source_path = self.base_path / source_skill["path"].rstrip("/")

        if not source_path.exists():
            return {"success": False, "error": f"Source skill path not found: {source_path}"}

        # Determine new skill path
        new_path = source_path.parent / new_skill_id
        if new_path.exists():
            return {"success": False, "error": f"Target path already exists: {new_path}"}

        # Copy source skill
        try:
            shutil.copytree(source_path, new_path)
        except Exception as e:
            return {"success": False, "error": f"Failed to copy skill: {e}"}

        # Apply mutations
        try:
            mutations_applied = self._apply_mutations(
                new_path,
                source_skill_id,
                new_skill_id,
                mutation_type,
                mutation_spec or {},
                new_name or f"{source_skill['name']} ({mutation_type})"
            )
        except Exception as e:
            # Cleanup on failure
            shutil.rmtree(new_path, ignore_errors=True)
            return {"success": False, "error": f"Failed to apply mutations: {e}"}

        # Register new skill
        new_name_final = new_name or f"{source_skill['name']} ({mutation_type})"
        relative_path = str(new_path.relative_to(self.base_path)) + "/"

        lineage = {
            "parent": source_skill_id,
            "children": [],
            "mutation_of": source_skill_id,
            "merged_from": []
        }

        success = self.registry_ops.register_skill(
            skill_id=new_skill_id,
            name=new_name_final,
            path=relative_path,
            tier=source_skill.get("tier", "experimental"),
            contract_level=source_skill.get("contract_level", "flexible"),
            domains=source_skill.get("domains", ["general"]),
            lineage=lineage
        )

        if not success:
            shutil.rmtree(new_path, ignore_errors=True)
            return {"success": False, "error": "Failed to register mutated skill"}

        # Update source skill's lineage
        self._update_source_lineage(source_skill_id, new_skill_id)

        # Log mutation
        self._log_mutation(source_skill_id, new_skill_id, mutation_type, mutation_spec)

        return {
            "success": True,
            "source_skill": source_skill_id,
            "new_skill_id": new_skill_id,
            "mutation_type": mutation_type,
            "path": str(new_path),
            "mutations_applied": mutations_applied
        }

    def _apply_mutations(
        self,
        skill_path: Path,
        source_id: str,
        new_id: str,
        mutation_type: str,
        mutation_spec: Dict,
        new_name: str
    ) -> List[str]:
        """Apply mutations to the copied skill."""
        mutations_applied = []

        # Update SKILL.md
        skill_md_path = skill_path / "SKILL.md"
        if skill_md_path.exists():
            content = skill_md_path.read_text(encoding="utf-8")

            # Update metadata
            content = content.replace(f"| ID | `{source_id}` |", f"| ID | `{new_id}` |")

            # Update title
            lines = content.split("\n")
            if lines and lines[0].startswith("# "):
                lines[0] = f"# {new_name}"
                content = "\n".join(lines)

            # Add mutation note
            mutation_note = f"\n\n## Mutation History\n\n- **Mutated from**: `{source_id}`\n- **Mutation type**: {mutation_type}\n- **Date**: {datetime.now().strftime('%Y-%m-%d')}\n"
            if "## Notes" in content:
                content = content.replace("## Notes", f"## Notes{mutation_note}\n---\n")
            else:
                content += mutation_note

            skill_md_path.write_text(content, encoding="utf-8")
            mutations_applied.append("Updated SKILL.md with new identity and mutation history")

        # Apply type-specific mutations
        if mutation_type == "enhance":
            mutations_applied.extend(self._apply_enhance_mutation(skill_path, mutation_spec))
        elif mutation_type == "optimize":
            mutations_applied.extend(self._apply_optimize_mutation(skill_path, mutation_spec))
        elif mutation_type == "specialize":
            mutations_applied.extend(self._apply_specialize_mutation(skill_path, mutation_spec))
        elif mutation_type == "generalize":
            mutations_applied.extend(self._apply_generalize_mutation(skill_path, mutation_spec))
        elif mutation_type == "refactor":
            mutations_applied.extend(self._apply_refactor_mutation(skill_path, mutation_spec))
        elif mutation_type == "extend":
            mutations_applied.extend(self._apply_extend_mutation(skill_path, mutation_spec))
        elif mutation_type == "simplify":
            mutations_applied.extend(self._apply_simplify_mutation(skill_path, mutation_spec))

        return mutations_applied

    def _apply_enhance_mutation(self, skill_path: Path, spec: Dict) -> List[str]:
        """Add new capabilities."""
        mutations = []

        # Add new capabilities to SKILL.md
        if "capabilities" in spec:
            skill_md_path = skill_path / "SKILL.md"
            if skill_md_path.exists():
                content = skill_md_path.read_text(encoding="utf-8")
                new_caps = "\n".join([f"- {cap}" for cap in spec["capabilities"]])
                if "## Capabilities" in content:
                    content = content.replace(
                        "## Capabilities\n",
                        f"## Capabilities\n\n### Enhanced Capabilities\n\n{new_caps}\n\n### Original Capabilities\n"
                    )
                    skill_md_path.write_text(content, encoding="utf-8")
                    mutations.append(f"Added {len(spec['capabilities'])} new capabilities")

        return mutations

    def _apply_optimize_mutation(self, skill_path: Path, spec: Dict) -> List[str]:
        """Apply optimization markers."""
        mutations = []

        # Add optimization notes
        skill_md_path = skill_path / "SKILL.md"
        if skill_md_path.exists():
            content = skill_md_path.read_text(encoding="utf-8")
            opt_note = "\n## Optimizations\n\n- Performance-optimized variant\n"
            if "optimizations" in spec:
                opt_note += "\n".join([f"- {opt}" for opt in spec["optimizations"]])
            content += opt_note
            skill_md_path.write_text(content, encoding="utf-8")
            mutations.append("Added optimization documentation")

        return mutations

    def _apply_specialize_mutation(self, skill_path: Path, spec: Dict) -> List[str]:
        """Create specialized version."""
        mutations = []

        # Update domains if specified
        if "domain" in spec:
            skill_md_path = skill_path / "SKILL.md"
            if skill_md_path.exists():
                content = skill_md_path.read_text(encoding="utf-8")
                content += f"\n## Specialization\n\nSpecialized for: {spec['domain']}\n"
                skill_md_path.write_text(content, encoding="utf-8")
                mutations.append(f"Specialized for domain: {spec['domain']}")

        return mutations

    def _apply_generalize_mutation(self, skill_path: Path, spec: Dict) -> List[str]:
        """Create generalized version."""
        mutations = []
        mutations.append("Marked as generalized variant (manual review needed)")
        return mutations

    def _apply_refactor_mutation(self, skill_path: Path, spec: Dict) -> List[str]:
        """Apply refactoring markers."""
        mutations = []
        mutations.append("Marked for refactoring (manual implementation needed)")
        return mutations

    def _apply_extend_mutation(self, skill_path: Path, spec: Dict) -> List[str]:
        """Extend with additional features."""
        mutations = []

        if "features" in spec:
            skill_md_path = skill_path / "SKILL.md"
            if skill_md_path.exists():
                content = skill_md_path.read_text(encoding="utf-8")
                features = "\n".join([f"- {f}" for f in spec["features"]])
                content += f"\n## Extended Features\n\n{features}\n"
                skill_md_path.write_text(content, encoding="utf-8")
                mutations.append(f"Added {len(spec['features'])} extended features")

        return mutations

    def _apply_simplify_mutation(self, skill_path: Path, spec: Dict) -> List[str]:
        """Simplify the skill."""
        mutations = []
        mutations.append("Marked as simplified variant (manual review needed)")
        return mutations

    def _update_source_lineage(self, source_id: str, child_id: str):
        """Update source skill's lineage."""
        registry = self.registry_ops.load_registry()
        if source_id in registry.get("skills", {}):
            source = registry["skills"][source_id]
            if "lineage" not in source:
                source["lineage"] = {"parent": None, "children": [], "mutation_of": None, "merged_from": []}
            if child_id not in source["lineage"]["children"]:
                source["lineage"]["children"].append(child_id)
            self.registry_ops.save_registry(registry)

    def _log_mutation(self, source_id: str, new_id: str, mutation_type: str, spec: Dict):
        """Log the mutation to RLAIF log."""
        log_path = self.base_path / ".tiangong" / "rlaif-log.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "mutation",
            "source_skill": source_id,
            "new_skill": new_id,
            "mutation_type": mutation_type,
            "spec": spec
        }

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Mutate existing skills")
    parser.add_argument("source_skill", help="Source skill ID to mutate")
    parser.add_argument("new_skill_id", help="ID for the new mutated skill")
    parser.add_argument("--type", "-t", required=True,
                        choices=list(SkillMutator.MUTATION_TYPES.keys()),
                        help="Type of mutation")
    parser.add_argument("--name", "-n", help="New name for mutated skill")
    parser.add_argument("--spec", "-s", type=json.loads, default={},
                        help="Mutation specification as JSON")
    parser.add_argument("--base-path", default=".", help="Base project path")
    parser.add_argument("--list-types", action="store_true",
                        help="List available mutation types")

    args = parser.parse_args()

    if args.list_types:
        print("Available mutation types:")
        for mt, desc in SkillMutator.MUTATION_TYPES.items():
            print(f"  {mt}: {desc}")
        return 0

    mutator = SkillMutator(args.base_path)
    result = mutator.mutate(
        source_skill_id=args.source_skill,
        new_skill_id=args.new_skill_id,
        mutation_type=args.type,
        mutation_spec=args.spec,
        new_name=args.name
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
