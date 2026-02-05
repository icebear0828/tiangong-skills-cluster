---
name: sensitive-file-detector
description: >
  敏感文件检测器。扫描 staged files，检测 .env/密钥/凭证等敏感文件和内容。
  阻止敏感信息泄露到 git 仓库。
---

# Sensitive File Detector — 敏感文件检测器

> 详细文档: [_architecture/L2-execution/core/sensitive-file-detector/SKILL.md](_architecture/L2-execution/core/sensitive-file-detector/SKILL.md)

## 执行流程

收到敏感文件检测请求后，按以下步骤执行：

### Step 1: 加载配置

读取 `.claude/git-config.json` 获取检测规则：
- `sensitive_patterns`: 敏感文件名模式列表
- `sensitive_content_patterns`: 敏感内容模式列表
- `sensitive_whitelist`: 白名单文件

### Step 2: 获取待检文件

```bash
git diff --staged --name-only   # 获取暂存文件列表
```

### Step 3: 文件名模式检测

对每个文件检查是否匹配敏感模式：
| 模式 | 严重度 |
|------|--------|
| `.env`, `.env.*` | critical |
| `*.pem`, `*.key`, `id_rsa` | critical |
| `credentials.json`, `secrets.yml` | critical |
| 白名单文件 (.env.example, *.test.*) | 跳过 |

### Step 4: 内容模式扫描

对文件内容扫描硬编码凭证：
| 模式 | 严重度 |
|------|--------|
| `password = "..."` | error |
| `api_key = "..."` | error |
| `AKIA[0-9A-Z]{16}` (AWS Key) | critical |
| `token = "..."` | warning |

### Step 5: 输出报告

```json
{
  "passed": false,
  "violations": [
    { "file": ".env", "type": "filename_match", "severity": "critical", "suggestion": "Add to .gitignore" }
  ],
  "auto_fixable": true,
  "gitignore_suggestions": [".env", "*.pem"]
}
```

**critical/error 级别违规将阻止提交流程。**

## 用户任务

$ARGUMENTS

---

请扫描暂存区文件，检测敏感文件和内容，输出检测报告。如发现违规，提供修复建议。
