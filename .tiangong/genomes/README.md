# Skill Genomes

This directory stores the genetic/evolutionary history of skills.

## Purpose

When skills are mutated, merged, or speciated via the Prime Mover, their "genome" (configuration and lineage) is stored here for:

1. **Lineage Tracking**: Trace the evolution of skills over time
2. **Rollback**: Restore previous versions of skills
3. **Analysis**: Study which mutations/merges are most effective
4. **Reproduction**: Re-create skills from their genome

## File Structure

Each genome file is named `{skill_id}-{version}.json` and contains:

```json
{
  "skill_id": "example-skill",
  "version": "1.0.0",
  "created_at": "2026-02-02T00:00:00Z",
  "genome": {
    "contract_level": "strict",
    "domains": ["example"],
    "capabilities": [],
    "dependencies": []
  },
  "lineage": {
    "parent": null,
    "mutation_type": null,
    "merged_from": []
  },
  "fitness_history": []
}
```

## Usage

Genomes are automatically created by:
- `prime-mover/scripts/spawn_skill.py`
- `prime-mover/scripts/mutate_skill.py`
- `prime-mover/scripts/merge_skills.py`
- `prime-mover/scripts/speciate.py`
