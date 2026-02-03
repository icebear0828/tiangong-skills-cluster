---
name: security-audit
description: >
  安全审计 Skill。检查代码安全漏洞，包括 OWASP Top 10，提供修复建议。
---

# Security Audit — 安全审计

> 详细文档: [_architecture/L2-execution/extended/security-audit/SKILL.md](_architecture/L2-execution/extended/security-audit/SKILL.md)

## OWASP Top 10

- 注入 (SQL/命令/LDAP)
- 认证缺陷
- 敏感数据泄露
- XSS 跨站脚本
- 访问控制缺失

## 风险级别

- **Critical**: 可被远程利用
- **High**: 需要条件利用
- **Medium**: 潜在风险

## 待审计代码

$ARGUMENTS

---

请进行安全审计并按风险级别报告漏洞。
