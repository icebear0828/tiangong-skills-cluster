---
name: security-audit
description: >
  安全审计 Skill。对代码进行安全审查，识别潜在漏洞。当需要：(1) 安全审计，
  (2) 漏洞检测，(3) 合规检查，(4) 渗透测试准备时触发。输出安全审计报告和修复建议。
  作为扩展 Skill，具有标准契约。
---

# Security Audit — 安全审计

## 触发条件

- 安全审计需求
- 代码审查发现潜在安全问题
- 合规检查要求
- 上线前安全检查

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["code"],
  "properties": {
    "code": {
      "type": "string"
    },
    "file_paths": {
      "type": "array"
    },
    "context": {
      "type": "object",
      "properties": {
        "language": { "type": "string" },
        "framework": { "type": "string" },
        "deployment": { "type": "string" }
      }
    },
    "audit_scope": {
      "type": "array",
      "items": {
        "enum": ["injection", "auth", "crypto", "data", "config", "all"]
      }
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["vulnerabilities", "summary"],
  "properties": {
    "vulnerabilities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "severity": { "enum": ["critical", "high", "medium", "low", "info"] },
          "type": { "type": "string" },
          "location": { "type": "string" },
          "description": { "type": "string" },
          "remediation": { "type": "string" },
          "cwe_id": { "type": "string" }
        }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "total": { "type": "integer" },
        "by_severity": { "type": "object" },
        "risk_score": { "type": "number" }
      }
    },
    "recommendations": {
      "type": "array"
    }
  }
}
```

## 检查范围

参考 `references/security-checklist.md`：

### OWASP Top 10
1. 注入攻击
2. 身份认证失效
3. 敏感数据泄露
4. XML 外部实体
5. 访问控制失效
6. 安全配置错误
7. XSS
8. 不安全的反序列化
9. 使用含漏洞的组件
10. 日志和监控不足

### 代码级检查
- 硬编码凭证
- 不安全的随机数
- 路径遍历
- 命令注入
- SSRF

## 脚本

- `scripts/audit.py` - 安全审计脚本
