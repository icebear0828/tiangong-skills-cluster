#!/usr/bin/env python3
"""
Prime Mover - Spawn Skill Script
Create new skills from templates or specifications.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "utils"))
from registry_ops import RegistryOperations


class SkillSpawner:
    """Spawn new skills from templates or specifications."""

    TEMPLATES = {
        "core": {
            "contract_level": "strict",
            "tier": "core",
            "structure": {
                "SKILL.md": True,
                "references/": ["best-practices.md"],
                "scripts/": ["main.py"]
            }
        },
        "extended": {
            "contract_level": "standard",
            "tier": "extended",
            "structure": {
                "SKILL.md": True,
                "references/": ["guidelines.md"],
                "scripts/": []
            }
        },
        "experimental": {
            "contract_level": "flexible",
            "tier": "experimental",
            "structure": {
                "SKILL.md": True,
                "references/": [],
                "scripts/": []
            }
        },
        "orchestrator": {
            "contract_level": "strict",
            "tier": "core",
            "structure": {
                "SKILL.md": True,
                "references/": ["patterns.md", "quality-gates.md"],
                "scripts/": ["orchestrate.py"]
            }
        }
    }

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.registry_ops = RegistryOperations(str(self.base_path / "registry.json"))

    def spawn(
        self,
        skill_id: str,
        name: str,
        template: str = "experimental",
        domains: list = None,
        parent: str = None,
        target_path: str = None,
        description: str = None
    ) -> Dict[str, Any]:
        """
        Spawn a new skill.

        Args:
            skill_id: Unique identifier for the skill
            name: Human-readable name
            template: Template type (core, extended, experimental, orchestrator)
            domains: List of domains the skill operates in
            parent: Parent skill ID if this is derived from another
            target_path: Custom path for the skill
            description: Skill description for SKILL.md

        Returns:
            Dictionary with spawn results
        """
        if template not in self.TEMPLATES:
            return {"success": False, "error": f"Unknown template: {template}"}

        template_config = self.TEMPLATES[template]

        # Determine target path
        if target_path:
            skill_path = self.base_path / target_path
        else:
            tier = template_config["tier"]
            if tier == "core":
                skill_path = self.base_path / "L2-execution" / "core" / skill_id
            elif tier == "extended":
                skill_path = self.base_path / "L2-execution" / "extended" / skill_id
            else:
                skill_path = self.base_path / "L2-execution" / "experimental" / skill_id

        # Check if skill already exists
        if skill_path.exists():
            return {"success": False, "error": f"Skill path already exists: {skill_path}"}

        # Create directory structure
        try:
            created_files = self._create_structure(
                skill_path,
                skill_id,
                name,
                template_config,
                description,
                domains or []
            )
        except Exception as e:
            return {"success": False, "error": f"Failed to create structure: {e}"}

        # Register the skill
        relative_path = str(skill_path.relative_to(self.base_path)) + "/"
        lineage = {
            "parent": parent,
            "children": [],
            "mutation_of": None,
            "merged_from": []
        }

        success = self.registry_ops.register_skill(
            skill_id=skill_id,
            name=name,
            path=relative_path,
            tier=template_config["tier"],
            contract_level=template_config["contract_level"],
            domains=domains or ["general"],
            lineage=lineage
        )

        if not success:
            return {"success": False, "error": "Failed to register skill in registry"}

        # Update parent's lineage if specified
        if parent:
            self._update_parent_lineage(parent, skill_id)

        return {
            "success": True,
            "skill_id": skill_id,
            "path": str(skill_path),
            "template": template,
            "created_files": created_files,
            "registered": True
        }

    def _create_structure(
        self,
        skill_path: Path,
        skill_id: str,
        name: str,
        template_config: Dict,
        description: str,
        domains: list
    ) -> list:
        """Create the skill directory structure."""
        created_files = []
        structure = template_config["structure"]

        # Create base directory
        skill_path.mkdir(parents=True, exist_ok=True)

        # Create SKILL.md
        if structure.get("SKILL.md"):
            skill_md_path = skill_path / "SKILL.md"
            skill_md_content = self._generate_skill_md(
                skill_id, name, template_config, description, domains
            )
            skill_md_path.write_text(skill_md_content, encoding="utf-8")
            created_files.append(str(skill_md_path))

        # Create references/
        if "references/" in structure:
            ref_path = skill_path / "references"
            ref_path.mkdir(exist_ok=True)
            for ref_file in structure["references/"]:
                ref_file_path = ref_path / ref_file
                ref_file_path.write_text(
                    f"# {ref_file.replace('.md', '').replace('-', ' ').title()}\n\n"
                    f"Reference documentation for {name}.\n\n"
                    f"## Contents\n\n- TODO: Add content\n",
                    encoding="utf-8"
                )
                created_files.append(str(ref_file_path))

        # Create scripts/
        if "scripts/" in structure:
            scripts_path = skill_path / "scripts"
            scripts_path.mkdir(exist_ok=True)
            for script_file in structure["scripts/"]:
                script_file_path = scripts_path / script_file
                script_content = self._generate_script_template(skill_id, name, script_file)
                script_file_path.write_text(script_content, encoding="utf-8")
                created_files.append(str(script_file_path))

        return created_files

    def _generate_skill_md(
        self,
        skill_id: str,
        name: str,
        template_config: Dict,
        description: str,
        domains: list
    ) -> str:
        """Generate SKILL.md content."""
        contract_level = template_config["contract_level"]
        tier = template_config["tier"]

        desc = description or f"{name} skill for {', '.join(domains)} domain(s)."

        content = f"""# {name}

> {desc}

## Metadata

| Field | Value |
|-------|-------|
| ID | `{skill_id}` |
| Version | 1.0.0 |
| Tier | {tier} |
| Contract Level | {contract_level} |
| Domains | {', '.join(domains) if domains else 'general'} |
| Status | active |

## Description

{desc}

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
      "description": "The result of the operation"
    }},
    "status": {{
      "type": "string",
      "enum": ["success", "partial", "failed"]
    }},
    "metadata": {{
      "type": "object"
    }}
  }},
  "required": ["result", "status"]
}}
```

## Capabilities

- TODO: Define capabilities

## Dependencies

- None specified

## Usage

```python
# Example usage
from {skill_id.replace('-', '_')} import main

result = main.execute({{
    "task": "example task",
    "context": {{}}
}})
```

## Notes

- Created: {datetime.now().strftime('%Y-%m-%d')}
- Template: {tier}
"""
        return content

    def _generate_script_template(self, skill_id: str, name: str, filename: str) -> str:
        """Generate a script template."""
        module_name = filename.replace(".py", "")
        return f'''#!/usr/bin/env python3
"""
{name} - {module_name.replace('_', ' ').title()}
Auto-generated script template.
"""

import argparse
import json
import sys
from typing import Dict, Any


def execute(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the skill.

    Args:
        input_data: Input following the contract schema

    Returns:
        Output following the contract schema
    """
    task = input_data.get("task", "")
    context = input_data.get("context", {{}})

    # TODO: Implement skill logic
    result = {{
        "message": f"Executed {name} with task: {{task}}"
    }}

    return {{
        "result": result,
        "status": "success",
        "metadata": {{
            "skill_id": "{skill_id}",
            "input_task": task
        }}
    }}


def main():
    parser = argparse.ArgumentParser(description="{name}")
    parser.add_argument("--task", required=True, help="Task to perform")
    parser.add_argument("--context", type=json.loads, default={{}}, help="Context JSON")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    input_data = {{
        "task": args.task,
        "context": args.context
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

    def _update_parent_lineage(self, parent_id: str, child_id: str):
        """Update parent skill's lineage to include new child."""
        registry = self.registry_ops.load_registry()
        if parent_id in registry.get("skills", {}):
            parent = registry["skills"][parent_id]
            if "lineage" not in parent:
                parent["lineage"] = {"parent": None, "children": [], "mutation_of": None, "merged_from": []}
            if child_id not in parent["lineage"]["children"]:
                parent["lineage"]["children"].append(child_id)
            self.registry_ops.save_registry(registry)


def main():
    parser = argparse.ArgumentParser(description="Spawn new skills")
    parser.add_argument("skill_id", help="Unique skill identifier")
    parser.add_argument("name", help="Human-readable skill name")
    parser.add_argument("--template", "-t", default="experimental",
                        choices=["core", "extended", "experimental", "orchestrator"],
                        help="Template type")
    parser.add_argument("--domains", "-d", nargs="+", default=["general"],
                        help="Skill domains")
    parser.add_argument("--parent", "-p", help="Parent skill ID")
    parser.add_argument("--path", help="Custom target path")
    parser.add_argument("--description", help="Skill description")
    parser.add_argument("--base-path", default=".", help="Base project path")

    args = parser.parse_args()

    spawner = SkillSpawner(args.base_path)
    result = spawner.spawn(
        skill_id=args.skill_id,
        name=args.name,
        template=args.template,
        domains=args.domains,
        parent=args.parent,
        target_path=args.path,
        description=args.description
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
