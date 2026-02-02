---
name: prime-mover
description: >
  元 Skill——造化总指挥。当现有 skill 无法解决当前任务时触发。核心能力：
  (1) 即时孵化新 skill 填补能力缺口，(2) 变异现有 skill 以适应新需求，
  (3) 融合两个 skill 的优势创造更强 skill，(4) 从宽泛 skill 分化出专注变体。
  仅在 Meta-Commander 判定复杂度为 XL 且现有 skill 不足时触发。
---

# Prime Mover — 造化总指挥

## 核心能力

### 1. 孵化新 Skill (spawn_skill.py)

当系统中不存在能处理某类任务的 skill 时，即时创建。

```bash
python scripts/spawn_skill.py \
  --name <new-skill-name> \
  --purpose "skill 的用途描述" \
  --domains <domain1,domain2> \
  --tier experimental \
  --examples "示例任务1 | 示例任务2"
```

孵化流程：
1. 分析任务需求，确定新 skill 需要的能力
2. 查阅 `references/skill-genome.md` 获取 skill 结构模板
3. 生成 SKILL.md（frontmatter + body）
4. 根据需要生成 scripts/ 和 references/
5. 注册到 skill-registry（tier=experimental, status=active）
6. 放入 L2/experimental/ 目录

### 2. 变异 Skill (mutate_skill.py)

修改现有 skill 以适应新需求或改进性能。

```bash
python scripts/mutate_skill.py \
  --skill-id <skill-id> \
  --mutation-type <minor|major> \
  --target "变异目标描述" \
  [--preserve-tests]  # 保持现有测试通过
```

变异类型：
- **minor**：微调指令措辞、参数、示例
- **major**：重写核心逻辑、策略方向

输出：变异后的 skill 副本（原始 skill 保留不动）

### 3. 融合 Skill (merge_skills.py)

将两个 skill 的优势合并为一个更强的 skill。

```bash
python scripts/merge_skills.py \
  --skill-a <skill-id-a> \
  --skill-b <skill-id-b> \
  --merge-strategy <union|intersection|complement>
  --new-name <merged-skill-name>
```

融合策略：
- **union**：取两者所有能力的并集
- **intersection**：取两者共同能力，强化深度
- **complement**：取两者互补的能力

### 4. 分化 Skill (speciate.py)

从一个覆盖面广的 skill 分化出专注于子领域的变体。

```bash
python scripts/speciate.py \
  --skill-id <parent-skill-id> \
  --subspecialty "子领域描述" \
  --new-name <variant-name>
```

分化逻辑：
1. 分析父 skill 的能力范围
2. 提取与子领域相关的部分
3. 深化该部分的指令和资源
4. 创建新 skill，lineage 标记父 skill

## Skill 基因组

参考 `references/skill-genome.md`，每个 skill 的 "基因组" 包括：

```json
{
  "identity": { "name": "...", "purpose": "...", "domains": [] },
  "instructions": { "workflow": "...", "constraints": [], "examples": [] },
  "resources": { "scripts": [], "references": [], "assets": [] },
  "contract": { "level": "...", "input_schema": {}, "output_schema": {} },
  "fitness": { "score": 0.0, "history": [], "test_cases": [] },
  "lineage": { "parent": null, "mutations": [], "generation": 0 }
}
```

基因组用于：
- 版本控制（每个版本保存基因组快照）
- 进化追踪（谱系树可视化）
- 变异操作（明确哪些 "基因" 可变异）

## 适应度函数

参考 `references/fitness-func.md`。

核心适应度 = f(正确性, 质量, 效率, 泛化能力)

- **正确性**（0.4）：在标准测试集上的通过率
- **质量**（0.25）：输出的专业度评分
- **效率**（0.15）：token/步骤使用量的倒数归一化
- **泛化能力**（0.2）：在未见过的测试用例上的表现

## 安全约束

- 新孵化的 skill 必须在 sandbox 中通过基础测试后才可激活
- 每个进化周期最多创建 3 个新 skill（避免种群爆炸）
- 所有操作记录到 `../state/rlaif-log.jsonl`
- XL 级变异必须人工确认
