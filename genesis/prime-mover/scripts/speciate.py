#!/usr/bin/env python3
"""
Prime Mover - Speciate Script
Create skill variants optimized for different niches/environments.
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


class SkillSpeciator:
    """Create skill variants for different niches/environments."""

    NICHES = {
        "web-frontend": {
            "description": "Web frontend development (React, Vue, Angular)",
            "domains": ["frontend", "web"],
            "tech_stack": ["react", "vue", "angular", "typescript", "css"]
        },
        "web-backend": {
            "description": "Web backend development (Node.js, Python, Go)",
            "domains": ["backend", "api"],
            "tech_stack": ["nodejs", "python", "go", "rest", "graphql"]
        },
        "mobile": {
            "description": "Mobile app development (iOS, Android, React Native)",
            "domains": ["mobile"],
            "tech_stack": ["swift", "kotlin", "react-native", "flutter"]
        },
        "data-science": {
            "description": "Data science and ML (Python, R, Jupyter)",
            "domains": ["data", "ml"],
            "tech_stack": ["python", "pandas", "numpy", "scikit-learn", "tensorflow"]
        },
        "devops": {
            "description": "DevOps and infrastructure (Docker, K8s, CI/CD)",
            "domains": ["devops", "infrastructure"],
            "tech_stack": ["docker", "kubernetes", "terraform", "github-actions"]
        },
        "embedded": {
            "description": "Embedded systems (C, C++, Rust)",
            "domains": ["embedded", "iot"],
            "tech_stack": ["c", "cpp", "rust", "arduino"]
        },
        "enterprise": {
            "description": "Enterprise applications (Java, .NET, Spring)",
            "domains": ["enterprise"],
            "tech_stack": ["java", "csharp", "spring", "dotnet"]
        },
        "game-dev": {
            "description": "Game development (Unity, Unreal, Godot)",
            "domains": ["games"],
            "tech_stack": ["unity", "unreal", "godot", "csharp", "cpp"]
        }
    }

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.registry_ops = RegistryOperations(str(self.base_path / "registry.json"))

    def speciate(
        self,
        source_skill_id: str,
        niche: str,
        new_skill_id: str = None,
        new_name: str = None,
        customizations: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a niche-specialized variant of a skill.

        Args:
            source_skill_id: ID of the skill to speciate
            niche: Target niche for specialization
            new_skill_id: Optional custom ID (default: {source}-{niche})
            new_name: Optional custom name
            customizations: Additional customizations

        Returns:
            Dictionary with speciation results
        """
        if niche not in self.NICHES:
            return {
                "success": False,
                "error": f"Unknown niche: {niche}. Valid niches: {list(self.NICHES.keys())}"
            }

        niche_config = self.NICHES[niche]

        # Get source skill
        registry = self.registry_ops.load_registry()
        if source_skill_id not in registry.get("skills", {}):
            return {"success": False, "error": f"Source skill not found: {source_skill_id}"}

        source_skill = registry["skills"][source_skill_id]
        source_path = self.base_path / source_skill["path"].rstrip("/")

        if not source_path.exists():
            return {"success": False, "error": f"Source skill path not found: {source_path}"}

        # Generate IDs and names
        new_skill_id = new_skill_id or f"{source_skill_id}-{niche}"
        new_name = new_name or f"{source_skill['name']} ({niche_config['description'].split('(')[0].strip()})"

        # Determine target path
        new_path = source_path.parent / new_skill_id
        if new_path.exists():
            return {"success": False, "error": f"Target path already exists: {new_path}"}

        # Copy source skill
        try:
            shutil.copytree(source_path, new_path)
        except Exception as e:
            return {"success": False, "error": f"Failed to copy skill: {e}"}

        # Apply specialization
        try:
            specializations_applied = self._apply_specialization(
                new_path,
                source_skill_id,
                new_skill_id,
                source_skill['name'],
                new_name,
                niche,
                niche_config,
                customizations or {}
            )
        except Exception as e:
            shutil.rmtree(new_path, ignore_errors=True)
            return {"success": False, "error": f"Failed to apply specialization: {e}"}

        # Merge domains
        merged_domains = list(set(source_skill.get("domains", []) + niche_config["domains"]))

        # Register new skill
        relative_path = str(new_path.relative_to(self.base_path)) + "/"
        lineage = {
            "parent": source_skill_id,
            "children": [],
            "mutation_of": source_skill_id,
            "merged_from": [],
            "speciation": {
                "niche": niche,
                "config": niche_config
            }
        }

        success = self.registry_ops.register_skill(
            skill_id=new_skill_id,
            name=new_name,
            path=relative_path,
            tier=source_skill.get("tier", "experimental"),
            contract_level=source_skill.get("contract_level", "flexible"),
            domains=merged_domains,
            lineage=lineage
        )

        if not success:
            shutil.rmtree(new_path, ignore_errors=True)
            return {"success": False, "error": "Failed to register specialized skill"}

        # Update source lineage
        self._update_source_lineage(source_skill_id, new_skill_id)

        # Log speciation
        self._log_speciation(source_skill_id, new_skill_id, niche)

        return {
            "success": True,
            "source_skill": source_skill_id,
            "new_skill_id": new_skill_id,
            "new_name": new_name,
            "niche": niche,
            "path": str(new_path),
            "domains": merged_domains,
            "specializations_applied": specializations_applied
        }

    def speciate_all(
        self,
        source_skill_id: str,
        niches: List[str] = None
    ) -> Dict[str, Any]:
        """
        Create variants for multiple niches.

        Args:
            source_skill_id: ID of the skill to speciate
            niches: List of niches (default: all)

        Returns:
            Dictionary with results for each niche
        """
        niches = niches or list(self.NICHES.keys())
        results = {}

        for niche in niches:
            results[niche] = self.speciate(source_skill_id, niche)

        successful = sum(1 for r in results.values() if r.get("success"))

        return {
            "source_skill": source_skill_id,
            "total_niches": len(niches),
            "successful": successful,
            "failed": len(niches) - successful,
            "results": results
        }

    def _apply_specialization(
        self,
        skill_path: Path,
        source_id: str,
        new_id: str,
        source_name: str,
        new_name: str,
        niche: str,
        niche_config: Dict,
        customizations: Dict
    ) -> List[str]:
        """Apply niche-specific specializations."""
        specializations = []

        # Update SKILL.md
        skill_md_path = skill_path / "SKILL.md"
        if skill_md_path.exists():
            content = skill_md_path.read_text(encoding="utf-8")

            # Update identity
            content = content.replace(f"| ID | `{source_id}` |", f"| ID | `{new_id}` |")

            # Update title
            lines = content.split("\n")
            if lines and lines[0].startswith("# "):
                lines[0] = f"# {new_name}"
                content = "\n".join(lines)

            # Add specialization section
            spec_section = f"""

## Specialization

### Niche: {niche}

{niche_config['description']}

### Target Domains

{chr(10).join([f'- {d}' for d in niche_config['domains']])}

### Tech Stack

{chr(10).join([f'- {t}' for t in niche_config['tech_stack']])}

### Speciated From

- **Source**: `{source_id}`
- **Date**: {datetime.now().strftime('%Y-%m-%d')}
"""

            if "## Notes" in content:
                content = content.replace("## Notes", f"{spec_section}\n## Notes")
            else:
                content += spec_section

            skill_md_path.write_text(content, encoding="utf-8")
            specializations.append("Updated SKILL.md with specialization info")

        # Create niche-specific reference
        ref_path = skill_path / "references"
        ref_path.mkdir(exist_ok=True)

        niche_ref_path = ref_path / f"niche-{niche}.md"
        niche_ref_content = f"""# {niche.replace('-', ' ').title()} Specialization

## Overview

This skill has been specialized for {niche_config['description'].lower()}.

## Tech Stack Focus

{chr(10).join([f'- **{t}**: Best practices and patterns' for t in niche_config['tech_stack']])}

## Domain-Specific Considerations

{chr(10).join([f'### {d.title()}{chr(10)}{chr(10)}- TODO: Add {d}-specific guidance{chr(10)}' for d in niche_config['domains']])}

## Customizations

{json.dumps(customizations, indent=2) if customizations else 'None specified'}
"""
        niche_ref_path.write_text(niche_ref_content, encoding="utf-8")
        specializations.append(f"Created niche reference: {niche_ref_path.name}")

        # Apply custom patterns based on niche
        if niche in ["web-frontend", "web-backend"]:
            specializations.extend(self._apply_web_patterns(skill_path, niche))
        elif niche == "data-science":
            specializations.extend(self._apply_data_science_patterns(skill_path))
        elif niche == "devops":
            specializations.extend(self._apply_devops_patterns(skill_path))

        return specializations

    def _apply_web_patterns(self, skill_path: Path, niche: str) -> List[str]:
        """Apply web development patterns."""
        patterns = []

        ref_path = skill_path / "references" / "web-patterns.md"
        content = f"""# Web Development Patterns

## {'Frontend' if 'frontend' in niche else 'Backend'} Patterns

### Component/Module Structure

- Follow framework conventions
- Keep components/modules small and focused
- Use consistent naming

### Testing

- Unit tests for business logic
- Integration tests for API endpoints
- {'E2E tests for critical user flows' if 'frontend' in niche else 'Contract tests for APIs'}

### Performance

- {'Lazy loading, code splitting' if 'frontend' in niche else 'Caching, connection pooling'}
- Monitoring and observability
"""
        ref_path.write_text(content, encoding="utf-8")
        patterns.append("Added web development patterns reference")

        return patterns

    def _apply_data_science_patterns(self, skill_path: Path) -> List[str]:
        """Apply data science patterns."""
        patterns = []

        ref_path = skill_path / "references" / "data-science-patterns.md"
        content = """# Data Science Patterns

## Notebook Best Practices

- Clear markdown documentation
- Reproducible execution order
- Version control for notebooks

## Data Pipeline Patterns

- Data validation at ingestion
- Feature engineering pipeline
- Model versioning

## Experiment Tracking

- Log hyperparameters
- Track metrics
- Save artifacts
"""
        ref_path.write_text(content, encoding="utf-8")
        patterns.append("Added data science patterns reference")

        return patterns

    def _apply_devops_patterns(self, skill_path: Path) -> List[str]:
        """Apply DevOps patterns."""
        patterns = []

        ref_path = skill_path / "references" / "devops-patterns.md"
        content = """# DevOps Patterns

## Infrastructure as Code

- Declarative over imperative
- Version controlled infrastructure
- Environment parity

## CI/CD Patterns

- Fast feedback loops
- Progressive delivery
- Rollback capabilities

## Observability

- Metrics, logs, traces
- Alerting thresholds
- Runbooks for incidents
"""
        ref_path.write_text(content, encoding="utf-8")
        patterns.append("Added DevOps patterns reference")

        return patterns

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

    def _log_speciation(self, source_id: str, new_id: str, niche: str):
        """Log the speciation to RLAIF log."""
        log_path = self.base_path / ".tiangong" / "rlaif-log.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "speciation",
            "source_skill": source_id,
            "new_skill": new_id,
            "niche": niche
        }

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Create skill variants for different niches")
    parser.add_argument("source_skill", help="Source skill ID to speciate")
    parser.add_argument("--niche", "-n", choices=list(SkillSpeciator.NICHES.keys()),
                        help="Target niche (or use --all)")
    parser.add_argument("--all", "-a", action="store_true",
                        help="Create variants for all niches")
    parser.add_argument("--new-id", "-i", help="Custom ID for new skill")
    parser.add_argument("--name", help="Custom name for new skill")
    parser.add_argument("--customizations", "-c", type=json.loads, default={},
                        help="Additional customizations as JSON")
    parser.add_argument("--base-path", default=".", help="Base project path")
    parser.add_argument("--list-niches", action="store_true",
                        help="List available niches")

    args = parser.parse_args()

    if args.list_niches:
        print("Available niches:")
        for niche, config in SkillSpeciator.NICHES.items():
            print(f"  {niche}: {config['description']}")
            print(f"    Domains: {', '.join(config['domains'])}")
            print(f"    Tech: {', '.join(config['tech_stack'][:3])}...")
            print()
        return 0

    if not args.niche and not args.all:
        parser.error("Must specify --niche or --all")

    speciator = SkillSpeciator(args.base_path)

    if args.all:
        result = speciator.speciate_all(args.source_skill)
    else:
        result = speciator.speciate(
            source_skill_id=args.source_skill,
            niche=args.niche,
            new_skill_id=args.new_id,
            new_name=args.name,
            customizations=args.customizations
        )

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.all:
        return 0 if result["successful"] > 0 else 1
    else:
        return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
