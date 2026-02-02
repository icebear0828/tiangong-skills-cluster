#!/usr/bin/env python3
"""
Prime Mover - Merge Skills Script
Combine multiple skills into a single unified skill.
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


class SkillMerger:
    """Merge multiple skills into unified skills."""

    MERGE_STRATEGIES = {
        "union": "Combine all capabilities from all skills",
        "intersection": "Keep only shared capabilities",
        "primary": "Use primary skill as base, augment with others",
        "composite": "Create wrapper that delegates to component skills"
    }

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.registry_ops = RegistryOperations(str(self.base_path / "registry.json"))

    def merge(
        self,
        skill_ids: List[str],
        new_skill_id: str,
        new_name: str,
        strategy: str = "union",
        target_path: str = None,
        tier: str = None,
        contract_level: str = None
    ) -> Dict[str, Any]:
        """
        Merge multiple skills into one.

        Args:
            skill_ids: List of skill IDs to merge
            new_skill_id: ID for the merged skill
            new_name: Name for the merged skill
            strategy: Merge strategy to use
            target_path: Custom path for merged skill
            tier: Tier for merged skill (defaults to highest of sources)
            contract_level: Contract level (defaults to strictest of sources)

        Returns:
            Dictionary with merge results
        """
        if len(skill_ids) < 2:
            return {"success": False, "error": "Need at least 2 skills to merge"}

        if strategy not in self.MERGE_STRATEGIES:
            return {
                "success": False,
                "error": f"Unknown strategy: {strategy}. Valid: {list(self.MERGE_STRATEGIES.keys())}"
            }

        # Load source skills
        registry = self.registry_ops.load_registry()
        source_skills = []
        for sid in skill_ids:
            if sid not in registry.get("skills", {}):
                return {"success": False, "error": f"Skill not found: {sid}"}
            source_skills.append(registry["skills"][sid])

        # Determine merged skill properties
        merged_tier = tier or self._determine_highest_tier(source_skills)
        merged_contract = contract_level or self._determine_strictest_contract(source_skills)
        merged_domains = self._merge_domains(source_skills)

        # Determine target path
        if target_path:
            merged_path = self.base_path / target_path
        else:
            if merged_tier == "core":
                merged_path = self.base_path / "L2-execution" / "core" / new_skill_id
            elif merged_tier == "extended":
                merged_path = self.base_path / "L2-execution" / "extended" / new_skill_id
            else:
                merged_path = self.base_path / "L2-execution" / "experimental" / new_skill_id

        if merged_path.exists():
            return {"success": False, "error": f"Target path already exists: {merged_path}"}

        # Create merged skill
        try:
            created_files = self._create_merged_skill(
                merged_path,
                new_skill_id,
                new_name,
                source_skills,
                skill_ids,
                strategy,
                merged_tier,
                merged_contract,
                merged_domains
            )
        except Exception as e:
            return {"success": False, "error": f"Failed to create merged skill: {e}"}

        # Register merged skill
        relative_path = str(merged_path.relative_to(self.base_path)) + "/"
        lineage = {
            "parent": None,
            "children": [],
            "mutation_of": None,
            "merged_from": skill_ids
        }

        success = self.registry_ops.register_skill(
            skill_id=new_skill_id,
            name=new_name,
            path=relative_path,
            tier=merged_tier,
            contract_level=merged_contract,
            domains=merged_domains,
            lineage=lineage
        )

        if not success:
            shutil.rmtree(merged_path, ignore_errors=True)
            return {"success": False, "error": "Failed to register merged skill"}

        # Log merge
        self._log_merge(skill_ids, new_skill_id, strategy)

        return {
            "success": True,
            "merged_skill_id": new_skill_id,
            "source_skills": skill_ids,
            "strategy": strategy,
            "path": str(merged_path),
            "tier": merged_tier,
            "contract_level": merged_contract,
            "domains": merged_domains,
            "created_files": created_files
        }

    def _determine_highest_tier(self, skills: List[Dict]) -> str:
        """Determine the highest tier among skills."""
        tier_order = {"core": 3, "extended": 2, "experimental": 1}
        highest = max(skills, key=lambda s: tier_order.get(s.get("tier", "experimental"), 0))
        return highest.get("tier", "experimental")

    def _determine_strictest_contract(self, skills: List[Dict]) -> str:
        """Determine the strictest contract level."""
        contract_order = {"strict": 3, "standard": 2, "flexible": 1}
        strictest = max(skills, key=lambda s: contract_order.get(s.get("contract_level", "flexible"), 0))
        return strictest.get("contract_level", "flexible")

    def _merge_domains(self, skills: List[Dict]) -> List[str]:
        """Merge domains from all skills."""
        domains = set()
        for skill in skills:
            domains.update(skill.get("domains", []))
        return sorted(list(domains))

    def _create_merged_skill(
        self,
        merged_path: Path,
        skill_id: str,
        name: str,
        source_skills: List[Dict],
        skill_ids: List[str],
        strategy: str,
        tier: str,
        contract_level: str,
        domains: List[str]
    ) -> List[str]:
        """Create the merged skill directory structure."""
        created_files = []

        # Create directories
        merged_path.mkdir(parents=True, exist_ok=True)
        (merged_path / "references").mkdir(exist_ok=True)
        (merged_path / "scripts").mkdir(exist_ok=True)

        # Create SKILL.md
        skill_md_content = self._generate_merged_skill_md(
            skill_id, name, source_skills, skill_ids, strategy, tier, contract_level, domains
        )
        skill_md_path = merged_path / "SKILL.md"
        skill_md_path.write_text(skill_md_content, encoding="utf-8")
        created_files.append(str(skill_md_path))

        # Create merge manifest
        manifest = {
            "merged_from": skill_ids,
            "strategy": strategy,
            "created_at": datetime.now().isoformat(),
            "source_versions": {
                sid: skill.get("version", "unknown")
                for sid, skill in zip(skill_ids, source_skills)
            }
        }
        manifest_path = merged_path / "references" / "merge-manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        created_files.append(str(manifest_path))

        # Create component references
        components_md = self._generate_components_reference(source_skills, skill_ids)
        components_path = merged_path / "references" / "components.md"
        components_path.write_text(components_md, encoding="utf-8")
        created_files.append(str(components_path))

        # Create delegation script for composite strategy
        if strategy == "composite":
            delegate_script = self._generate_delegate_script(skill_id, skill_ids, source_skills)
            delegate_path = merged_path / "scripts" / "delegate.py"
            delegate_path.write_text(delegate_script, encoding="utf-8")
            created_files.append(str(delegate_path))

        # Create main execution script
        main_script = self._generate_main_script(skill_id, name, skill_ids, strategy)
        main_path = merged_path / "scripts" / "main.py"
        main_path.write_text(main_script, encoding="utf-8")
        created_files.append(str(main_path))

        return created_files

    def _generate_merged_skill_md(
        self,
        skill_id: str,
        name: str,
        source_skills: List[Dict],
        skill_ids: List[str],
        strategy: str,
        tier: str,
        contract_level: str,
        domains: List[str]
    ) -> str:
        """Generate SKILL.md for merged skill."""
        source_list = "\n".join([f"- `{sid}`: {s['name']}" for sid, s in zip(skill_ids, source_skills)])

        return f"""# {name}

> Merged skill combining capabilities from multiple source skills.

## Metadata

| Field | Value |
|-------|-------|
| ID | `{skill_id}` |
| Version | 1.0.0 |
| Tier | {tier} |
| Contract Level | {contract_level} |
| Domains | {', '.join(domains)} |
| Status | active |
| Merge Strategy | {strategy} |

## Source Skills

{source_list}

## Description

This skill is a merged combination of {len(skill_ids)} source skills using the **{strategy}** strategy.

### Merge Strategy: {strategy}

{self.MERGE_STRATEGIES[strategy]}

## Contract

### Input Schema

```json
{{
  "type": "object",
  "properties": {{
    "task": {{
      "type": "string",
      "description": "The task to perform"
    }},
    "context": {{
      "type": "object",
      "description": "Additional context"
    }},
    "delegate_to": {{
      "type": "string",
      "description": "Optional: specific component skill to delegate to",
      "enum": {json.dumps(skill_ids)}
    }}
  }},
  "required": ["task"]
}}
```

### Output Schema

```json
{{
  "type": "object",
  "properties": {{
    "result": {{
      "type": "object",
      "description": "Combined result from component skills"
    }},
    "status": {{
      "type": "string",
      "enum": ["success", "partial", "failed"]
    }},
    "component_results": {{
      "type": "object",
      "description": "Individual results from each component skill"
    }}
  }},
  "required": ["result", "status"]
}}
```

## Capabilities

Combined capabilities from all source skills:

{self._list_combined_capabilities(source_skills)}

## Dependencies

- Component skills must be available
- See references/components.md for details

## Merge History

- **Created**: {datetime.now().strftime('%Y-%m-%d')}
- **Strategy**: {strategy}
- **Sources**: {', '.join(skill_ids)}
"""

    def _list_combined_capabilities(self, source_skills: List[Dict]) -> str:
        """List combined capabilities (placeholder)."""
        return "- See individual component skills for detailed capabilities"

    def _generate_components_reference(self, source_skills: List[Dict], skill_ids: List[str]) -> str:
        """Generate components reference document."""
        content = """# Component Skills Reference

This document describes the component skills that were merged.

"""
        for sid, skill in zip(skill_ids, source_skills):
            content += f"""## {skill['name']} (`{sid}`)

- **Path**: {skill['path']}
- **Tier**: {skill.get('tier', 'unknown')}
- **Contract Level**: {skill.get('contract_level', 'unknown')}
- **Domains**: {', '.join(skill.get('domains', []))}

---

"""
        return content

    def _generate_delegate_script(self, skill_id: str, skill_ids: List[str], source_skills: List[Dict]) -> str:
        """Generate delegation script for composite strategy."""
        return f'''#!/usr/bin/env python3
"""
{skill_id} - Delegation Script
Delegates tasks to appropriate component skills.
"""

import json
import sys
from typing import Dict, Any, List

# Component skill mappings
COMPONENTS = {{
{chr(10).join([f'    "{sid}": "{s["path"]}",' for sid, s in zip(skill_ids, source_skills)])}
}}


def select_component(task: str, context: Dict) -> str:
    """
    Select the most appropriate component skill for a task.

    Args:
        task: The task description
        context: Additional context

    Returns:
        Component skill ID
    """
    # TODO: Implement intelligent selection logic
    # For now, return first component
    return list(COMPONENTS.keys())[0]


def delegate(skill_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delegate execution to a component skill.

    Args:
        skill_id: Component skill ID
        input_data: Input data to pass

    Returns:
        Result from component skill
    """
    if skill_id not in COMPONENTS:
        return {{
            "result": None,
            "status": "failed",
            "error": f"Unknown component: {{skill_id}}"
        }}

    # TODO: Implement actual delegation
    # This would typically import and call the component skill
    return {{
        "result": {{"delegated_to": skill_id}},
        "status": "success",
        "metadata": {{"component": skill_id}}
    }}


def delegate_all(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delegate to all components and aggregate results.

    Args:
        input_data: Input data to pass

    Returns:
        Aggregated results
    """
    results = {{}}
    for skill_id in COMPONENTS:
        results[skill_id] = delegate(skill_id, input_data)

    # Determine overall status
    statuses = [r.get("status") for r in results.values()]
    if all(s == "success" for s in statuses):
        overall_status = "success"
    elif any(s == "success" for s in statuses):
        overall_status = "partial"
    else:
        overall_status = "failed"

    return {{
        "result": {{"aggregated": True}},
        "status": overall_status,
        "component_results": results
    }}


if __name__ == "__main__":
    # Test delegation
    test_input = {{"task": "test", "context": {{}}}}
    print(json.dumps(delegate_all(test_input), indent=2))
'''

    def _generate_main_script(self, skill_id: str, name: str, skill_ids: List[str], strategy: str) -> str:
        """Generate main execution script."""
        return f'''#!/usr/bin/env python3
"""
{name} - Main Execution Script
Merged skill using {strategy} strategy.
"""

import argparse
import json
import sys
from typing import Dict, Any

COMPONENT_SKILLS = {json.dumps(skill_ids)}
MERGE_STRATEGY = "{strategy}"


def execute(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the merged skill.

    Args:
        input_data: Input following the contract schema

    Returns:
        Output following the contract schema
    """
    task = input_data.get("task", "")
    context = input_data.get("context", {{}})
    delegate_to = input_data.get("delegate_to")

    if MERGE_STRATEGY == "composite":
        # Import and use delegation
        from delegate import delegate, delegate_all, select_component

        if delegate_to:
            return delegate(delegate_to, input_data)
        else:
            selected = select_component(task, context)
            return delegate(selected, input_data)

    else:
        # Union/intersection/primary strategies
        # Implement combined execution logic
        result = {{
            "message": f"Executed merged skill with task: {{task}}",
            "strategy": MERGE_STRATEGY,
            "components": COMPONENT_SKILLS
        }}

        return {{
            "result": result,
            "status": "success",
            "metadata": {{
                "skill_id": "{skill_id}",
                "merge_strategy": MERGE_STRATEGY
            }}
        }}


def main():
    parser = argparse.ArgumentParser(description="{name}")
    parser.add_argument("--task", required=True, help="Task to perform")
    parser.add_argument("--context", type=json.loads, default={{}}, help="Context JSON")
    parser.add_argument("--delegate-to", help="Specific component to delegate to")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    input_data = {{
        "task": args.task,
        "context": args.context,
        "delegate_to": args.delegate_to
    }}

    result = execute(input_data)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to {{args.output}}")
    else:
        print(output)

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
'''

    def _log_merge(self, skill_ids: List[str], new_id: str, strategy: str):
        """Log the merge to RLAIF log."""
        log_path = self.base_path / ".tiangong" / "rlaif-log.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "merge",
            "source_skills": skill_ids,
            "new_skill": new_id,
            "strategy": strategy
        }

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Merge multiple skills")
    parser.add_argument("skill_ids", nargs="+", help="Skill IDs to merge (at least 2)")
    parser.add_argument("--new-id", "-i", required=True, help="ID for merged skill")
    parser.add_argument("--name", "-n", required=True, help="Name for merged skill")
    parser.add_argument("--strategy", "-s", default="union",
                        choices=list(SkillMerger.MERGE_STRATEGIES.keys()),
                        help="Merge strategy")
    parser.add_argument("--path", help="Custom target path")
    parser.add_argument("--tier", choices=["core", "extended", "experimental"],
                        help="Override tier")
    parser.add_argument("--contract-level", choices=["strict", "standard", "flexible"],
                        help="Override contract level")
    parser.add_argument("--base-path", default=".", help="Base project path")
    parser.add_argument("--list-strategies", action="store_true",
                        help="List available merge strategies")

    args = parser.parse_args()

    if args.list_strategies:
        print("Available merge strategies:")
        for strat, desc in SkillMerger.MERGE_STRATEGIES.items():
            print(f"  {strat}: {desc}")
        return 0

    merger = SkillMerger(args.base_path)
    result = merger.merge(
        skill_ids=args.skill_ids,
        new_skill_id=args.new_id,
        new_name=args.name,
        strategy=args.strategy,
        target_path=args.path,
        tier=args.tier,
        contract_level=args.contract_level
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
