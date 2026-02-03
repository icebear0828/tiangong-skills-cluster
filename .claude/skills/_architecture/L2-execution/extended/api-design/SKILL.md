---
name: api-design
description: >
  API 设计 Skill。设计 RESTful 或 GraphQL API 接口。当需要：(1) 设计新 API，
  (2) 优化现有 API，(3) 生成 API 规范文档时触发。输出 OpenAPI/Swagger 规范或
  GraphQL Schema。作为扩展 Skill，具有标准契约。
---

# API Design — API 设计

## 触发条件

- 需求包含"API"、"接口"等关键词
- 由 code-orchestrator 在功能开发前调度
- 新服务/微服务设计

## 输入契约 (Standard)

```json
{
  "type": "object",
  "required": ["requirements"],
  "properties": {
    "requirements": {
      "type": "string",
      "description": "API 需求描述"
    },
    "api_type": {
      "type": "string",
      "enum": ["rest", "graphql"],
      "default": "rest"
    },
    "existing_api": {
      "type": "object",
      "description": "现有 API 规范（如需扩展）"
    },
    "constraints": {
      "type": "object",
      "properties": {
        "versioning": { "type": "string" },
        "authentication": { "type": "string" },
        "rate_limiting": { "type": "boolean" }
      }
    }
  }
}
```

## 输出契约 (Standard)

```json
{
  "type": "object",
  "required": ["api_spec"],
  "properties": {
    "api_spec": {
      "type": "object",
      "description": "OpenAPI 3.0 规范或 GraphQL Schema"
    },
    "endpoints": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "method": { "type": "string" },
          "path": { "type": "string" },
          "description": { "type": "string" }
        }
      }
    },
    "models": {
      "type": "array",
      "description": "数据模型定义"
    }
  }
}
```

## 设计原则

参考 `references/api-guidelines.md`：

### RESTful 设计
- 资源导向
- 正确使用 HTTP 方法
- 一致的命名规范
- 适当的状态码
- HATEOAS（可选）

### GraphQL 设计
- 清晰的类型定义
- 合理的查询深度
- N+1 问题处理
- 分页策略

## 脚本

- `scripts/design_api.py` - API 设计主脚本
