#!/usr/bin/env python3
"""
Generate Report - 生成评测报告
生成 Skill 评测的详细报告。
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def generate_markdown_report(skill_id: str, eval_history: list) -> str:
    """生成 Markdown 格式报告"""
    report = []
    report.append(f"# Evaluation Report: {skill_id}")
    report.append(f"\nGenerated: {datetime.utcnow().isoformat()}Z\n")

    if not eval_history:
        report.append("No evaluation data available.")
        return "\n".join(report)

    # 摘要
    report.append("## Summary")
    latest = eval_history[-1]
    report.append(f"- Latest Fitness: {latest.get('fitness', 'N/A')}")
    report.append(f"- Total Evaluations: {len(eval_history)}")

    # 计算平均
    avg_fitness = sum(e.get('fitness', 0) for e in eval_history) / len(eval_history)
    report.append(f"- Average Fitness: {avg_fitness:.3f}")

    # 趋势
    if len(eval_history) >= 2:
        recent_avg = sum(e.get('fitness', 0) for e in eval_history[-5:]) / min(5, len(eval_history))
        older_avg = sum(e.get('fitness', 0) for e in eval_history[:-5]) / max(1, len(eval_history) - 5)
        if recent_avg > older_avg + 0.05:
            trend = "Improving ↑"
        elif recent_avg < older_avg - 0.05:
            trend = "Declining ↓"
        else:
            trend = "Stable →"
        report.append(f"- Trend: {trend}")

    # 分数明细
    report.append("\n## Score Breakdown")
    report.append("\n| Dimension | Latest | Average |")
    report.append("|-----------|--------|---------|")

    dimensions = set()
    for e in eval_history:
        dimensions.update(e.get('scores', {}).keys())

    for dim in sorted(dimensions):
        latest_score = latest.get('scores', {}).get(dim, 'N/A')
        avg_score = sum(e.get('scores', {}).get(dim, 0) for e in eval_history) / len(eval_history)
        if isinstance(latest_score, (int, float)):
            latest_str = f"{latest_score:.2f}"
        else:
            latest_str = str(latest_score)
        report.append(f"| {dim} | {latest_str} | {avg_score:.2f} |")

    # 历史记录
    report.append("\n## Recent History")
    report.append("\n| Timestamp | Fitness | Type |")
    report.append("|-----------|---------|------|")

    for e in eval_history[-10:]:
        ts = e.get('timestamp', 'N/A')[:19]
        fitness = e.get('fitness', 'N/A')
        eval_type = e.get('eval_type', 'N/A')
        report.append(f"| {ts} | {fitness} | {eval_type} |")

    return "\n".join(report)


def load_eval_history(skill_id: str = None) -> list:
    """加载评测历史"""
    history_path = PROJECT_ROOT / ".tiangong" / "eval-history.jsonl"

    if not history_path.exists():
        return []

    results = []
    with open(history_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                if skill_id is None or record.get("skill_id") == skill_id:
                    results.append(record)

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate evaluation report")
    parser.add_argument("--skill-id", help="Skill ID (omit for all)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    args = parser.parse_args()

    history = load_eval_history(args.skill_id)

    if args.format == "markdown":
        report = generate_markdown_report(args.skill_id or "All Skills", history)
    else:
        report = json.dumps(history, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report saved to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
