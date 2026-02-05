---
name: sensitive-file-detector
description: >
  敏感文件检测器 (L2 Core)。扫描 git staged files，检测 .env/密钥/凭证等敏感文件和内容模式。
  在 commit 前阻止敏感信息泄露。由 commit-orchestrator 在 Smart Commit 流程中并行调度。
  配置来源：.claude/git-config.json 的 sensitive_patterns 和 sensitive_content_patterns。
---

# Sensitive File Detector — 敏感文件检测器

## 触发条件

- 由 `commit-orchestrator` 在 Smart Commit Step 2a 并行调度
- 由 `git-commander` 直接路由（S 级 "检查敏感文件" 请求）
- 由 Claude Code `PreToolUse` hook 在检测到 `git commit` 时触发

## 核心能力

1. **文件名模式匹配**: 检测 .env, .pem, .key, credentials.json 等敏感文件名
2. **内容模式扫描**: 检测代码中硬编码的密码、API key、token 等
3. **白名单过滤**: 排除 .env.example, 测试文件等安全文件
4. **修复建议**: 提供 .gitignore 规则和修复方案

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["staged_files"],
  "properties": {
    "staged_files": {
      "type": "array",
      "items": { "type": "string" },
      "description": "暂存区文件路径列表"
    },
    "file_contents": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "文件路径 → 内容映射（用于内容模式扫描）"
    },
    "config_override": {
      "type": "object",
      "properties": {
        "sensitive_patterns": { "type": "array", "items": { "type": "string" } },
        "sensitive_content_patterns": { "type": "array", "items": { "type": "string" } },
        "whitelist": { "type": "array", "items": { "type": "string" } }
      },
      "description": "覆盖默认配置（可选，默认读取 .claude/git-config.json）"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["passed", "violations"],
  "properties": {
    "passed": {
      "type": "boolean",
      "description": "检测是否通过（无违规则 true）"
    },
    "violations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "file": { "type": "string", "description": "违规文件路径" },
          "type": { "type": "string", "enum": ["filename_match", "content_match"], "description": "违规类型" },
          "pattern": { "type": "string", "description": "匹配的模式" },
          "severity": { "type": "string", "enum": ["warning", "error", "critical"] },
          "line_number": { "type": "integer", "description": "违规行号（仅 content_match）" },
          "snippet": { "type": "string", "description": "违规代码片段（脱敏显示）" },
          "suggestion": { "type": "string", "description": "修复建议" }
        }
      },
      "description": "违规列表"
    },
    "auto_fixable": {
      "type": "boolean",
      "description": "是否可自动修复（如添加到 .gitignore）"
    },
    "gitignore_suggestions": {
      "type": "array",
      "items": { "type": "string" },
      "description": "建议添加到 .gitignore 的规则"
    },
    "scanned_count": {
      "type": "integer",
      "description": "扫描的文件总数"
    }
  }
}
```

## 执行流程

### Step 1: 加载配置

```
读取 .claude/git-config.json:
    ├─ sensitive_patterns: 文件名正则列表
    ├─ sensitive_content_patterns: 内容正则列表
    └─ sensitive_whitelist: 白名单模式
```

### Step 2: 文件名模式检测

```
对每个 staged 文件:
    │
    ├─ 匹配白名单 → 跳过
    │
    ├─ 匹配 sensitive_patterns
    │   ├─ .env → severity: critical
    │   ├─ *.pem / *.key → severity: critical
    │   ├─ credentials.json → severity: critical
    │   └─ secrets.yml → severity: error
    │
    └─ 未匹配 → 安全
```

### Step 3: 内容模式扫描

```
对每个 staged 文件的内容:
    │
    ├─ 跳过二进制文件
    │
    ├─ 匹配 sensitive_content_patterns
    │   ├─ password = "xxx" → severity: error
    │   ├─ api_key = "xxx" → severity: error
    │   ├─ AKIA[0-9A-Z]{16} → severity: critical (AWS Key)
    │   └─ token = "xxx" → severity: warning
    │
    └─ 记录匹配行号和脱敏片段
```

### Step 4: 生成报告

- 汇总所有违规
- 生成 .gitignore 建议
- 判断是否可自动修复
- 输出结构化结果

## 严重度分级

| 等级 | 说明 | 操作 |
|------|------|------|
| `critical` | 密钥/凭证文件 | **阻止提交**，必须修复 |
| `error` | 硬编码密码/token | **阻止提交**，建议使用环境变量 |
| `warning` | 可疑模式 | 警告但不阻止 |

## 配置文件说明

默认配置位于 `.claude/git-config.json`:

```json
{
  "sensitive_patterns": ["\\.env$", ".*\\.pem$", ".*\\.key$", "credentials\\.json$"],
  "sensitive_content_patterns": ["password\\s*=\\s*['\"].+['\"]", "AKIA[0-9A-Z]{16}"],
  "sensitive_whitelist": [".env.example", "*.test.*"]
}
```

## 与其他 Skill 的关系

| Skill | 关系 | 说明 |
|-------|------|------|
| commit-orchestrator | 被调用 | Smart Commit Step 2a (与 validator 并行) |
| diff-analyzer | 并行协作 | 同步获取变更信息 |
| git-hook-manager | 相关 | 安装 pre-commit hook 提供轻量检测 |

## 质量标准

| 维度 | 标准 | 阈值 |
|------|------|------|
| 检测率 | 正确识别敏感文件 | ≥99% |
| 误报率 | 白名单文件不误报 | ≤5% |
| 建议质量 | 修复建议可执行 | 100% |
